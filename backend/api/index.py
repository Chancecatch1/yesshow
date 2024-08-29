# backend/api/index.py

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import pandas as pd
import joblib
import os

app = Flask(__name__)
CORS(app)  # 모든 도메인에서 접근 가능하게 설정

# 모델 경로 설정
cancellation_model_path = os.path.join(os.path.dirname(__file__), 'models/xgb_model.joblib')
cancellation_mms_path = os.path.join(os.path.dirname(__file__), 'models/mms.joblib')

remaining_seats_model_path = os.path.join(os.path.dirname(__file__), 'models/xgb_model_r.joblib')
remaining_seats_mms_path = os.path.join(os.path.dirname(__file__), 'models/mms_r.joblib')

# 모델과 스케일러 로드
cancellation_model = joblib.load(cancellation_model_path)
cancellation_mms = joblib.load(cancellation_mms_path)

remaining_seats_model = joblib.load(remaining_seats_model_path)
remaining_seats_mms = joblib.load(remaining_seats_mms_path)

# 예측 처리 엔드포인트
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
        'Gender_2_Count': [data['gender']['gender_2']]
    })

    # 취소표 예측을 위한 스케일링 및 예측
    cancellation_features_scaled = cancellation_mms.transform(features)
    predicted_count = round(float(cancellation_model.predict(cancellation_features_scaled)[0]), 2)

    # 남은 좌석수 예측을 위한 스케일링 및 예측
    remaining_seats_features_scaled = remaining_seats_mms.transform(features)
    predicted_remaining_seats = round(float(remaining_seats_model.predict(remaining_seats_features_scaled)[0]), 2)

    return jsonify({
        "predictedCancellationCount": predicted_count,
        "predictedRemainingSeats": predicted_remaining_seats
    })

if __name__ == '__main__':
    app.run(debug=True)