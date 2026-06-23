# Technical Interview Preparation Guide: Sales Forecasting Platform

This document provides a deep dive into the technical architecture, design decisions, and core logic of the Sales Forecasting Platform. Use this to explain the project confidently during interviews.

---

## 1. Project Overview (The "Elevator Pitch")
**"I built a full-stack Sales Forecasting Platform that predicts daily sales for over 1,100 Rossmann stores. It uses an XGBoost machine learning model on the backend, served via a Flask REST API, with a responsive Vanilla JavaScript frontend. The project handles real-time single-store predictions and asynchronous batch processing via CSV uploads."**

## 2. Technical Stack & Why?
| Component | Technology | Rationale |
| :--- | :--- | :--- |
| **Backend** | **Python / Flask** | Flask is a lightweight micro-framework that allows for rapid development and seamless integration with Python's data science ecosystem (Pandas, Scikit-Learn). |
| **ML Model** | **XGBoost** | The industry standard for tabular data. It handles missing values, captures non-linear relationships, and is highly efficient via gradient boosting. |
| **Data Handling** | **Pandas / NumPy** | Used for high-performance data manipulation and feature engineering before passing data to the model. |
| **Frontend** | **Vanilla JS / HTML / CSS** | I chose a "no-framework" approach to minimize bundle size, ensure maximum performance, and demonstrate a strong grasp of core Web APIs (Fetch, DOM manipulation). |
| **Persistence** | **Joblib** | Used for serializing high-performance Python objects (the model and feature column list). |

---

## 3. The Prediction Pipeline (How it Works)

### Step A: Data Ingestion
The frontend collects user inputs (Date, Promo, Store Type, etc.) and sends a JSON POST request to the `/api/predict` endpoint.

### Step B: Feature Engineering (The "Secret Sauce")
Raw data cannot be fed directly into a gradient boosting model. The `preprocess.py` module performs several critical transformations:
1.  **Date Decomposition**: Converts the date string into `Year`, `Month`, `Day`, `WeekOfYear`, and `DayOfWeek`. This helps the model capture seasonality (e.g., weekend spikes, Christmas rush).
2.  **Categorical Encoding**: Uses **One-Hot Encoding** for variables like `StoreType` and `Assortment`. This converts text labels into binary columns (0/1) that the model can understand mathematically.
3.  **Store Data Enrichment**: If available, it merges static store info (like `CompetitionDistance`) based on the `StoreID`.

### Step C: The Log-Scale Strategy
**Crucial Point:** During training, the target variable (Sales) was log-transformed ($y = \ln(1 + \text{sales})$). 
*   **Why?** Sales data is often skewed. Log transformation normalizes the distribution and focuses the model on percentage errors rather than absolute errors, which is critical for the RMSPE (Root Mean Square Percentage Error) metric used in this competition.
*   **The Inverse**: The model outputs a log-scaled value. My backend applies `np.expm1()` (exclusive-plus-1) to transform the prediction back into actual currency values before sending it to the frontend.

---

## 4. Key Technical Challenges & Solutions

### Q: How did you ensure data consistency between training and production?
**A:** "I implemented a `columns.pkl` artifact. During training, I saved the exact list of features the model was trained on. In production, the `prepare_dataframe` function uses this list to reorder incoming data and fill any missing columns with zeros, ensuring the feature vector always matches the model's expectations."

### Q: How do you handle missing data?
**A:** "I used a multi-layered approach. XGBoost natively handles missing values by learning directionality for them, but I also implemented sensible defaults in `preprocess.py` (e.g., assuming a store is 'Open' or 'Basic Assortment' if not specified) to maintain UI stability."

### Q: What is the benefit of the 'Health Check' endpoint?
**A:** "The `/health` endpoint doesn't just check if the server is up; it actively attempts to load the model and feature artifacts from disk. This ensures that the system is only marked 'Online' if it is actually capable of making predictions."

---

## 5. Architectural Highlights
- **Decoupled Architecture**: The frontend is served as a static bundle, making it easy to migrate to a CDN (like Vercel or S3) in the future while keeping the API on a dedicated compute instance.
- **RESTful Design**: Standard HTTP methods and status codes are used (200 for OK, 400 for bad input, 500 for model failures).
- **Environment Agnostic**: The `Path` library in Python is used to resolve file paths relative to the script location, allowing the project to run on Windows, Linux, or in a Docker container without path changes.

---

## 6. Future Roadmap (What would you add next?)
1.  **Caching**: Implement Redis to cache predictions for frequently hit Store/Date combinations.
2.  **Authentication**: Add JWT-based auth to protect the API from unauthorized batch uploads.
3.  **CI/CD**: Set up a GitHub Action to retrain the model automatically when new data is uploaded to a data bucket.
