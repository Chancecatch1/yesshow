# backend/api/index.py

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import pandas as pd
import joblib
import os

app = Flask(__name__)
CORS(app)

cancellation_model_path = os.path.join(os.path.dirname(__file__), 'models/XB_343804_c.joblib')
cancellation_mms_path = os.path.join(os.path.dirname(__file__), 'models/mms_343804_c.joblib')

remaining_seats_model_path = os.path.join(os.path.dirname(__file__), 'models/RF_343804_r.joblib')
remaining_seats_mms_path = os.path.join(os.path.dirname(__file__), 'models/mms_343804_r.joblib')

cancellation_model = joblib.load(cancellation_model_path)
cancellation_mms = joblib.load(cancellation_mms_path)

remaining_seats_model = joblib.load(remaining_seats_model_path)
remaining_seats_mms = joblib.load(remaining_seats_mms_path)

@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.json
    print("Received JSON data:", data)

    date_part, time_part = data['eventDate'].split('T')
    year, month, day = map(int, date_part.split('-'))
    hour, minute = map(int, time_part.split(':'))
    weekday = datetime(year, month, day).weekday()

    features = pd.DataFrame({
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
    })

    feature_order = [
        'Year', 'Month', 'Day', 'Hour', 'Minute', 'Weekday',
        'Avg_Discount', 'Avg_Price', 'Avg_Age',
        'Gender_0_Count', 'Gender_1_Count', 'Gender_2_Count',
        'Payment_Method_Card', 'Payment_Method_Other', 'Payment_Method_Bank', 
        'Payment_Method_Multi', 'Payment_Method_Cash',
        'Discount_Type_Other', 'Discount_Type_InHouse'
    ]
    
    features = features[feature_order]

    cancellation_features_scaled = cancellation_mms.transform(features)
    predicted_count = round(float(cancellation_model.predict(cancellation_features_scaled)[0]), 2)

    remaining_seats_features_scaled = remaining_seats_mms.transform(features)
    predicted_remaining_seats = round(float(remaining_seats_model.predict(remaining_seats_features_scaled)[0]), 2)

    return jsonify({
        "predictedCancellationCount": predicted_count,
        "predictedRemainingSeats": predicted_remaining_seats
    })

if __name__ == '__main__':
    app.run(debug=True)