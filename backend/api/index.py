# backend/api/index.py

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pandas as pd
import joblib
import os

app = Flask(__name__)
CORS(app)  # 모든 도메인에서 접근 가능하게 설정
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# db = SQLAlchemy(app)

# class Prediction(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     performanceCode = db.Column(db.String(50))
#     seatCount = db.Column(db.Integer)
#     eventCode = db.Column(db.String(50))
#     eventDate = db.Column(db.String(50))
#     discountAmount = db.Column(db.Float)
#     pricePerTicket = db.Column(db.Float)
#     gender = db.Column(db.String(10))
#     age = db.Column(db.Integer)
#     genre = db.Column(db.String(50))

# # 메시지 반환 엔드포인트
# @app.route('/api/message', methods=['GET'])
# def get_message():
#     current_date = datetime.now().strftime('%Y-%m-%d')  # 현재 날짜를 YYYY-MM-DD 형식으로 가져옴
#     return jsonify({"message": f"{current_date}"})

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

@app.route('/static/images/<filename>')
def get_image(filename):
    directory = os.path.join(app.root_path, '../static/images')
    return send_from_directory(directory, filename)

if __name__ == '__main__':
    # with app.app_context():
    #     db.create_all() 
    app.run(debug=True)