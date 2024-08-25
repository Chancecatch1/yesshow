from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import pandas as pd
import joblib
import os

app = Flask(__name__)
CORS(app)  # 모든 도메인에서 접근 가능하게 설정

# 모델 경로 설정
model_path = os.path.join(os.path.dirname(__file__), 'models/xgb_model.joblib')
mms_path = os.path.join(os.path.dirname(__file__), 'models/mms.joblib')
model = joblib.load(model_path)
mms = joblib.load(mms_path)

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
        'Gender_0_Count': [data['gender']['otherCount']],
        'Gender_1_Count': [data['gender']['maleCount']],
        'Gender_2_Count': [data['gender']['femaleCount']]
    })

    # 스케일링 적용
    features_scaled = mms.transform(features)

    # 모델을 사용해 예측
    predicted_count = float(model.predict(features_scaled)[0])

    return jsonify({"predictedCancellationCount": predicted_count})

if __name__ == '__main__':
    app.run(debug=True)