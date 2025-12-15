# Yesshow - Performance Ticket Cancellation Predictor

> A service that predicts ticket cancellation availability using KOPIS data and ML

## Overview

Yesshow predicts how many cancellation tickets will become available on the day of a performance. It uses machine learning models trained on KOPIS (Korea Performing Arts Information System) data to help users find tickets for sold-out shows.

## Key Features

- **Cancellation Prediction**: Random Forest and XGBoost models for ticket prediction
- **Remaining Seats Forecast**: Predicts available seats before show time
- **Survival Analysis**: Kaplan-Meier analysis for cancellation timing patterns
- **Real-time API**: Flask-based REST API for predictions

## Architecture

```
yesshow/
├── frontend/          # SvelteKit web frontend
│   └── src/
│       ├── routes/    # Page routing
│       └── lib/       # Shared components
├── backend/           # Flask ML prediction server
│   └── api/
│       ├── index.py   # Main API server
│       ├── models/    # Trained ML models (.joblib)
│       └── data/      # Training data
└── notebook/          # Jupyter analysis notebooks
```

## Tech Stack

| Category | Technologies |
|----------|-------------|
| Frontend | SvelteKit, TailwindCSS, TypeScript |
| Backend | Flask, Flask-CORS |
| ML/Data | pandas, scikit-learn, XGBoost, lifelines |
| Deployment | Vercel |

## Getting Started

```bash
# Frontend
cd frontend && npm install && npm run dev

# Backend
cd backend && pip install -r requirements.txt && python api/index.py
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/predict` | Predict cancellations and remaining seats |
| GET | `/api/cancellation-data` | Get cancellation time distribution |
