# Sales Forecasting Platform

A machine learning platform that predicts Rossmann store sales using an XGBoost model. It has a Flask REST API backend and a plain HTML/CSS/JS frontend — no frameworks, no build step.

---

## Project Structure

```
sales-forecasting-platform/
├── backend/
│   ├── app.py               # Flask app entry point
│   ├── config.py            # App configuration
│   ├── requirements.txt     # Python dependencies
│   ├── test_api.py          # API test script
│   ├── routes/
│   │   ├── predict.py       # POST /api/predict
│   │   ├── upload.py        # POST /api/upload/predict
│   │   └── insights.py      # GET  /api/insights/*
│   └── services/
│       ├── model_loader.py  # Loads model.pkl and columns.pkl
│       ├── preprocess.py    # Feature engineering pipeline
│       └── services.py      # Shared prediction helpers
├── frontend/
│   ├── index.html           # Main UI
│   ├── style.css            # Styles
│   └── app.js               # JS logic
├── ml/
│   ├── artifacts/
│   │   ├── model.pkl        # Trained XGBoost model
│   │   └── columns.pkl      # Expected feature columns
│   └── notebooks/           # EDA, training, evaluation notebooks
└── docs/
    ├── api.md
    ├── architecture.md
    └── deployment.md
```

---

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/your-username/sales-forecasting-platform.git
cd sales-forecasting-platform
```

### 2. Set up the backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

pip install -r requirements.txt
```

### 3. Run the Flask server

```bash
cd backend
python app.py
```

The API will be available at `http://localhost:5000`.

### 4. Open the frontend

Just open `frontend/index.html` in your browser. No build step needed.

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API info and available routes |
| GET | `/health` | Health check — verifies model loads OK |
| POST | `/api/predict` | Single store prediction |
| POST | `/api/upload/predict` | Batch prediction via CSV upload |
| GET | `/api/upload/template` | Download a sample CSV template |
| GET | `/api/insights/model-info` | Model type, estimators, depth |
| GET | `/api/insights/fields` | Input field descriptions |
| GET | `/api/insights/features` | Full feature list used by the model |

### Single prediction — example request

```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Store": 1,
    "Date": "2024-07-15",
    "DayOfWeek": 2,
    "Promo": 1,
    "SchoolHoliday": 0,
    "StateHoliday": "0",
    "StoreType": "b",
    "Assortment": "b",
    "CompetitionDistance": 500.0,
    "Promo2": 0
  }'
```

### Example response

```json
{
  "success": true,
  "prediction": 7842.51,
  "store": 1,
  "date": "2024-07-15"
}
```

---

## Input Fields

| Field | Type | Description |
|-------|------|-------------|
| `Store` | int | Store ID (1–1115) |
| `Date` | string | Date in `YYYY-MM-DD` format |
| `DayOfWeek` | int | 1 = Monday … 7 = Sunday |
| `Promo` | int | 1 if a promo is running, else 0 |
| `Promo2` | int | 1 if Promo2 is active, else 0 |
| `SchoolHoliday` | int | 1 if school holiday, else 0 |
| `StateHoliday` | string | `0`, `a`, `b`, or `c` |
| `StoreType` | string | `a`, `b`, `c`, or `d` |
| `Assortment` | string | `a` (basic), `b` (extra), `c` (extended) |
| `CompetitionDistance` | float | Distance to nearest competitor in metres |

---

## Running the test script

Make sure the Flask server is running, then:

```bash
cd backend
python test_api.py
```

---

## ML Model

The model was trained on the [Rossmann Store Sales](https://www.kaggle.com/c/rossmann-store-sales) dataset using XGBoost with log-transformed sales as the target. The trained artifacts live in `ml/artifacts/`.

The notebooks in `ml/notebooks/` cover the full pipeline:
- `01_eda.ipynb` — Exploratory data analysis
- `02_data_cleaning.ipynb` — Cleaning and null handling
- `03_feature_engineering.ipynb` — Date features, one-hot encoding
- `04_model_training.ipynb` — XGBoost training
- `05_model_evaluation.ipynb` — RMSPE and cross-validation
- `06_prediction_testing.ipynb` — End-to-end prediction checks

---

## Tech Stack

- **Backend** — Python, Flask, scikit-learn, XGBoost, pandas
- **Frontend** — HTML, CSS, vanilla JavaScript
- **ML** — XGBoost, Jupyter notebooks
