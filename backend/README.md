# Sales Forecasting Platform - Backend API

Complete Flask REST API for the Sales Forecasting Platform. This backend serves predictions from a trained XGBoost model that forecasts store sales.

## Features

- ✅ Single and batch predictions
- ✅ CSV file upload for bulk predictions
- ✅ Model metrics and metadata endpoints
- ✅ Data preprocessing and validation
- ✅ CORS support for frontend integration
- ✅ Comprehensive error handling
- ✅ Input field schema documentation

## Project Structure

```
backend/
├── app.py                 # Main Flask application
├── config.py             # Configuration management
├── requirements.txt      # Python dependencies
│
├── routes/               # API endpoints
│   ├── predict.py       # Single & batch predictions
│   ├── upload.py        # File upload handling
│   └── insights.py      # Model information
│
├── services/            # Business logic
│   ├── model_loader.py  # Model loading & caching
│   ├── preprocess.py    # Data preprocessing
│   └── services.py      # Prediction & validation services
│
├── uploads/             # Temporary upload directory
└── README.md           # This file
```

## API Endpoints

### Prediction Endpoints

#### 1. Single Prediction
```
POST /api/predict

Request:
{
    "store": 1,
    "day_of_week": 2,
    "date": "2024-07-15",
    "promo": 1,
    "school_holiday": 0,
    "state_holiday": "0",
    "store_type": "b",
    "assortment": "b",
    "competition_distance": 500.0,
    "promo2": 0,
    "competition_open_years": 5,
    "promo2_running_years": 0
}

Response:
{
    "success": true,
    "prediction": 6229.64,
    "prediction_log": 8.7346,
    "store": 1,
    "date": "2024-07-15",
    "message": "Prediction successful"
}
```

#### 2. Batch Predictions
```
POST /api/predict/batch

Request:
{
    "predictions": [
        {
            "store": 1,
            "day_of_week": 2,
            "date": "2024-07-15",
            ...
        },
        ...
    ]
}

Response:
{
    "success": true,
    "total_predictions": 3,
    "predictions": [...],
    "average_prediction": 6229.64,
    "min_prediction": 5000.00,
    "max_prediction": 7500.00,
    "message": "Successfully made 3 predictions"
}
```

#### 3. File Upload for Predictions
```
POST /api/upload/predict

Form Data:
- file: CSV file with prediction columns

Response:
{
    "success": true,
    "file_name": "predictions.csv",
    "rows_processed": 100,
    "total_predictions": 100,
    "predictions": [...],
    "message": "Successfully made 100 predictions"
}
```

#### 4. Upload Template
```
GET /api/upload/template

Response:
{
    "success": true,
    "template": "[CSV content]",
    "columns": [list of columns],
    "message": "Template created successfully"
}
```

### Information Endpoints

#### 5. Model Information
```
GET /api/insights/model-info

Response:
{
    "success": true,
    "model_type": "XGBRegressor",
    "n_features": 25,
    "n_estimators": 1200,
    "max_depth": 10,
    "learning_rate": 0.03,
    "metrics": {...},
    "message": "Model information retrieved successfully"
}
```

#### 6. Required Input Fields
```
GET /api/insights/required-fields

Response:
{
    "success": true,
    "required_fields": {
        "store": {
            "type": "integer",
            "description": "Store ID",
            "required": true
        },
        ...
    },
    "message": "Input field requirements retrieved successfully"
}
```

#### 7. Example Prediction
```
GET /api/insights/example

Response:
{
    "success": true,
    "example_input": {...},
    "example_output": {...},
    "message": "Example request and response"
}
```

#### 8. Model Features
```
GET /api/insights/features

Response:
{
    "success": true,
    "total_features": 25,
    "features": [list of all features],
    "message": "Model features retrieved successfully"
}
```

### System Endpoints

#### 9. Health Check
```
GET /health

Response:
{
    "status": "healthy",
    "message": "API and model are ready",
    "timestamp": "2024-07-15T10:30:00.000000"
}
```

#### 10. Root / Documentation
```
GET /
GET /docs

Response:
API information and available endpoints
```

## Installation

### Prerequisites
- Python 3.8+
- pip or conda

### Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment** (optional but recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify model artifacts exist**
   ```
   - ml/artifacts/model.pkl
   - ml/artifacts/columns.pkl
   ```

## Running the API

### Development Server

```bash
python app.py
```

The API will start at `http://127.0.0.1:5000`

### Production with Gunicorn

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker

```bash
docker build -t sales-forecasting-api .
docker run -p 5000:5000 sales-forecasting-api
```

## Configuration

Create a `.env` file in the backend directory:

```
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here
API_HOST=0.0.0.0
API_PORT=5000
```

## Input Fields Reference

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| store | integer | Yes | - | Store ID |
| day_of_week | integer | No | Current | Day of week (1-7) |
| date | string | No | Today | Date (YYYY-MM-DD) |
| promo | integer | No | 0 | Promotion flag (0/1) |
| school_holiday | integer | No | 0 | School holiday flag (0/1) |
| state_holiday | string | No | 0 | State holiday type (0/a/b/c) |
| store_type | string | No | a | Store type (a/b/c/d) |
| assortment | string | No | a | Assortment type (a/b/c) |
| competition_distance | float | No | 0 | Distance to competitor (m) |
| promo2 | integer | No | 0 | Promo2 participation (0/1) |
| competition_open_years | integer | No | 0 | Years since competitor opened |
| promo2_running_years | integer | No | 0 | Years running Promo2 |

## Error Handling

All endpoints return consistent error responses:

```json
{
    "success": false,
    "error": "Error description",
    "message": "User-friendly message"
}
```

HTTP Status Codes:
- `200` - Success
- `400` - Bad Request (validation error)
- `404` - Not Found
- `405` - Method Not Allowed
- `500` - Internal Server Error

## Testing Example with cURL

### Single Prediction
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "store": 1,
    "day_of_week": 2,
    "promo": 1,
    "competition_distance": 500
  }'
```

### Get Model Info
```bash
curl http://localhost:5000/api/insights/model-info
```

### Get Example
```bash
curl http://localhost:5000/api/insights/example
```

## Performance Considerations

- **Single Prediction**: ~10-50ms
- **Batch Prediction**: 100 items ~100-200ms
- **File Upload**: Depends on file size, up to 50MB supported

## Dependencies

See `requirements.txt` for complete list:
- Flask 3.0.3 - Web framework
- Flask-CORS 4.0.1 - CORS support
- pandas 2.2.2 - Data processing
- numpy 1.26.4 - Numerical computing
- scikit-learn 1.5.1 - ML utilities
- xgboost 2.1.1 - Gradient boosting
- joblib 1.4.2 - Model serialization
- gunicorn 22.0.0 - Production server

## Troubleshooting

### Model not found error
- Verify ML artifacts exist at `ml/artifacts/`
- Check file paths in `services/model_loader.py`

### Port already in use
```bash
# Change port in app.py or use:
python app.py # Then modify the port parameter
```

### CORS errors
- CORS is enabled for all origins in development
- Configure in `app.py` for production

### Import errors
- Ensure you're in the correct directory
- Check virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

## Development

### Adding new endpoints
1. Create new route file in `routes/`
2. Create blueprint and register in `app.py`
3. Add business logic to `services/`

### Testing
```bash
# Run with test configuration
FLASK_ENV=testing python -m pytest tests/
```

## Production Deployment

1. Set `FLASK_ENV=production`
2. Use strong `SECRET_KEY`
3. Run behind Nginx/Apache reverse proxy
4. Enable HTTPS
5. Use production WSGI server (gunicorn)
6. Set up logging and monitoring
7. Use environment variables for configuration

## API Response Format

All responses follow this format:
```json
{
    "success": boolean,
    "data": {...} or null,
    "error": string or null,
    "message": string,
    "timestamp": "ISO-8601"
}
```

## Support

For issues or questions:
1. Check the `/docs` endpoint
2. Review example predictions at `/api/insights/example`
3. Check input field requirements at `/api/insights/required-fields`
