# System Architecture

The Sales Forecasting Platform is built with a decoupled architecture focusing on simplicity, performance, and data science integration.

## 1. Context Diagram
The user interacts with a browser-based UI, which communicates with a centralized Python API. The API interfaces with pre-trained machine learning models and local data storage.

## 2. Component Design

### Frontend (Static Assets)
- **Tech**: HTML5, CSS3 (Vanilla), JavaScript (ES6).
- **Responsibility**: UI rendering, input validation, API communication via `fetch`.
- **Serving**: Served by Flask in development; can be served by Nginx or CDN in production.

### Backend (REST API)
- **Tech**: Flask (Python).
- **Core Modules**:
  - `routes/`: Endpoint definitions for predictions and discovery.
  - `services/preprocess.py`: The pipeline for feature engineering and data normalization.
  - `services/model_loader.py`: Singleton-pattern loader for the XGBoost model.

### Machine Learning Layer
- **Tech**: XGBoost, Scikit-Learn.
- **Artifacts**: `model.pkl` (Model weights), `columns.pkl` (Feature registry).

## 3. Data Flow (Single Prediction)
1. **User Input**: `Date`, `Store`, `Promo`, etc.
2. **REST request**: `POST /api/predict`.
3. **Preprocessing**: 
   - Date decomposition (Year, Month, etc.).
   - One-hot encoding for categorical strings.
   - Handling of missing descriptors.
4. **Model Inference**: Input vector passed to XGBoost.
5. **Inverse Transformation**: Log-scaled output converted back to currency.
6. **JSON Response**: Returned to UI for visualization.

---
For more details on how to explain this in an interview, see [INTERVIEW_PREP.md](../INTERVIEW_PREP.md).

