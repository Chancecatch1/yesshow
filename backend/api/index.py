# backend/api/index.py

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import pandas as pd
from lifelines import KaplanMeierFitter
import joblib
import os
import numpy as np

app = Flask(__name__)
CORS(app)

model_paths = {
    'PF343804': {
        'cancellation_model': 'models/RF_343804_c.joblib',
        'cancellation_mms': 'models/mms_343804_c.joblib',
        'remaining_seats_model': 'models/RF_343804_r.joblib',
        'remaining_seats_mms': 'models/mms_343804_r.joblib',
        'csv_file': 'data/df_343804_t.csv'
    },
    'PF352013': {
        'cancellation_model': 'models/XB_352013_c.joblib',
        'cancellation_mms': 'models/mms_352013_c.joblib',
        'remaining_seats_model': 'models/XB_352013_r.joblib',
        'remaining_seats_mms': 'models/mms_352013_r.joblib',
        'csv_file': 'data/df_352013_t.csv'
    },
    'PF392163': {
        'cancellation_model': 'models/RF_392163_c.joblib',
        'cancellation_mms': 'models/mms_392163_c.joblib',
        'remaining_seats_model': 'models/RF_392163_r.joblib',
        'remaining_seats_mms': 'models/mms_392163_r.joblib',
        'csv_file': 'data/df_392163_t.csv'
    }
}

models = {}
for event_code, paths in model_paths.items():
    models[event_code] = {
        'cancellation_model': joblib.load(os.path.join(os.path.dirname(__file__), paths['cancellation_model'])),
        'cancellation_mms': joblib.load(os.path.join(os.path.dirname(__file__), paths['cancellation_mms'])),
        'remaining_seats_model': joblib.load(os.path.join(os.path.dirname(__file__), paths['remaining_seats_model'])),
        'remaining_seats_mms': joblib.load(os.path.join(os.path.dirname(__file__), paths['remaining_seats_mms'])),
        'csv_file': paths['csv_file']
    }

def load_csv_for_event(event_code):
    csv_file_path = os.path.join(os.path.dirname(__file__), models[event_code]['csv_file'])
    try:
        df = pd.read_csv(csv_file_path)
        return df
    except FileNotFoundError:
        print(f"Error: CSV file not found at {csv_file_path}")
        return None
    except pd.errors.EmptyDataError:
        print(f"Error: CSV file is empty at {csv_file_path}")
        return None
    
@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.json
    print("Received JSON data:", data)

    event_code = data['eventCode']
    model_set = models.get(event_code)

    if not model_set:
        return jsonify({"error": "Invalid event code"}), 400

    date_part, time_part = data['eventDate'].split('T')
    year, month, day = map(int, date_part.split('-'))
    hour, minute = map(int, time_part.split(':'))
    weekday = datetime(year, month, day).weekday()

    # 공통 피처
    features = {
        'Year': [year],
        'Month': [month],
        'Day': [day],
        'Hour': [hour],
        'Minute': [minute],
        'Weekday': [weekday],
        'Avg_Discount': [data['discountAmount']],
        'Avg_Price': [data['pricePerTicket']],
        'Avg_Age': [data['age']],
        'Gender_0_Count': [data['gender']['gender_0']],
        'Gender_1_Count': [data['gender']['gender_1']],
        'Gender_2_Count': [data['gender']['gender_2']],
        'Payment_Method_Card': [data['paymentDetails']['cardPayment']],
        'Payment_Method_Other': [data['paymentDetails']['otherPayment']],
        'Payment_Method_Bank': [data['paymentDetails']['bankTransfer']],
        'Payment_Method_Multi': [data['paymentDetails']['multiplePayments']],
        'Payment_Method_Cash': [data['paymentDetails']['cashPayment']],
        'Discount_Type_InHouse': [data['discountDetails']['selfDiscount']],
        'Discount_Type_Other': [data['discountDetails']['otherDiscount']]
    }

    if event_code == 'PF392163':
        features['Payment_Method_Certificate'] = [data['paymentDetails'].get('voucherPayment', 0)]

    features_df = pd.DataFrame(features)

    if event_code == 'PF392163':
        feature_order = [
            'Year', 'Month', 'Day', 'Hour', 'Minute', 'Weekday',
            'Avg_Discount', 'Avg_Price', 'Avg_Age',
            'Gender_0_Count', 'Gender_1_Count', 'Gender_2_Count',
            'Payment_Method_Card', 'Payment_Method_Other', 'Payment_Method_Bank', 
            'Payment_Method_Multi', 'Payment_Method_Cash', 'Payment_Method_Certificate',
            'Discount_Type_Other', 'Discount_Type_InHouse'
        ]
    else:
        feature_order = [
            'Year', 'Month', 'Day', 'Hour', 'Minute', 'Weekday',
            'Avg_Discount', 'Avg_Price', 'Avg_Age',
            'Gender_0_Count', 'Gender_1_Count', 'Gender_2_Count',
            'Payment_Method_Card', 'Payment_Method_Other', 'Payment_Method_Bank', 
            'Payment_Method_Multi', 'Payment_Method_Cash',
            'Discount_Type_Other', 'Discount_Type_InHouse'
        ]

    features_df = features_df[feature_order]

    cancellation_features_scaled = model_set['cancellation_mms'].transform(features_df)
    predicted_count = round(float(model_set['cancellation_model'].predict(cancellation_features_scaled)[0]), 2)

    remaining_seats_features_scaled = model_set['remaining_seats_mms'].transform(features_df)
    predicted_remaining_seats = round(float(model_set['remaining_seats_model'].predict(remaining_seats_features_scaled)[0]), 2)

    return jsonify({
        "predictedCancellationCount": predicted_count,
        "predictedRemainingSeats": predicted_remaining_seats
    })

@app.route('/api/cancellation-data', methods=['GET'])
def get_cancellation_data():
    event_code = request.args.get('eventCode')

    if not event_code or event_code not in models:
        return jsonify({"error": "Invalid event code"}), 400

    df = load_csv_for_event(event_code)

    if df is None:
        return jsonify({"error": "Data not available"}), 500

    T = df['Cancellation_Time']
    E = [1] * len(T)

    kmf = KaplanMeierFitter()
    kmf.fit(T, event_observed=E, timeline=np.linspace(0, T.max(), 100))

    data = [{'time': t, 'probability': 1 - p} for t, p in zip(kmf.timeline, kmf.survival_function_['KM_estimate'])]

    time_points = {
        't20': kmf.percentile(0.8),
        't50': kmf.percentile(0.5),
        't90': kmf.percentile(0.1)
    }

    return jsonify({
        'data': data,
        'timePoints': time_points
    })

if __name__ == "__main__":
    app.run(port=5001, debug=True)