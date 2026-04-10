import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
STORE_DATA_PATH = PROJECT_ROOT / "ml" / "data" / "raw" / "store.csv"


def load_store_data():
    """Load store data if available for merging."""
    if STORE_DATA_PATH.exists():
        return pd.read_csv(STORE_DATA_PATH)
    return None


def merge_store_info(data_dict, store_data=None):
    """Merge store information from store.csv if available and store_id provided."""
    if store_data is None or 'Store' not in data_dict:
        return data_dict
    
    store_id = data_dict.get('Store')
    store_row = store_data[store_data['Store'] == store_id]
    
    if not store_row.empty:
        # Merge store attributes, keeping original values if present
        for col in store_row.columns:
            if col not in data_dict or pd.isna(data_dict.get(col)):
                data_dict[col] = store_row[col].values[0]
    
    return data_dict


def extract_date_features(data_dict):
    """Extract date features from Date field or use current date."""
    date = datetime.now()

    if 'Date' in data_dict and isinstance(data_dict['Date'], str):
        try:
            date = pd.to_datetime(data_dict['Date'])
        except (ValueError, TypeError):
            pass
    
    # Extract date features
    data_dict['Year'] = data_dict.get('Year', date.year)
    data_dict['Month'] = data_dict.get('Month', date.month)
    data_dict['Day'] = data_dict.get('Day', date.day)
    data_dict['WeekOfYear'] = data_dict.get('WeekOfYear', date.isocalendar()[1])
    data_dict['DayOfWeekNum'] = data_dict.get('DayOfWeekNum', date.weekday())
    data_dict['IsWeekend'] = data_dict.get('IsWeekend', 1 if date.weekday() >= 5 else 0)
    data_dict['IsMonthStart'] = data_dict.get('IsMonthStart', 1 if date.day == 1 else 0)
    data_dict['IsMonthEnd'] = data_dict.get('IsMonthEnd', 1 if date.day >= 28 else 0)
    
    return data_dict


def handle_missing_values(data_dict):
    """Fill missing values with sensible defaults."""
    defaults = {
        'Store': 1,
        'Open': 1,
        'DayOfWeek': 1,
        'Promo': 0,
        'SchoolHoliday': 0,
        'CompetitionDistance': 0.0,
        'Promo2': 0,
        'CompetitionOpenSinceMonth': 1,
        'CompetitionOpenSinceYear': 2020,
        'Promo2SinceMonth': 1,
        'Promo2SinceYear': 2010,
        'StateHoliday': '0',
        'StoreType': 'a',
        'Assortment': 'a'
    }
    
    for field, default_val in defaults.items():
        if field not in data_dict or data_dict[field] is None:
            data_dict[field] = default_val
    
    return data_dict


def apply_one_hot_encoding(data_dict):
    """Apply one-hot encoding for categorical variables."""
    # StateHoliday: 0, a, b, c
    state_holiday = str(data_dict.get('StateHoliday', '0')).lower().strip()
    data_dict['StateHoliday_a'] = 1 if state_holiday == 'a' else 0
    data_dict['StateHoliday_b'] = 1 if state_holiday == 'b' else 0
    data_dict['StateHoliday_c'] = 1 if state_holiday == 'c' else 0
    
    # StoreType: a, b, c, d
    store_type = str(data_dict.get('StoreType', 'a')).lower().strip()
    data_dict['StoreType_b'] = 1 if store_type == 'b' else 0
    data_dict['StoreType_c'] = 1 if store_type == 'c' else 0
    data_dict['StoreType_d'] = 1 if store_type == 'd' else 0
    
    # Assortment: a, b, c
    assortment = str(data_dict.get('Assortment', 'a')).lower().strip()
    data_dict['Assortment_b'] = 1 if assortment == 'b' else 0
    data_dict['Assortment_c'] = 1 if assortment == 'c' else 0
    
    return data_dict


def normalize_numeric_values(data_dict):
    """Ensure numeric fields are properly typed."""
    numeric_fields = [
        'Store', 'Open', 'DayOfWeek', 'Promo', 'SchoolHoliday', 'Year', 'Month', 'Day',
        'WeekOfYear', 'DayOfWeekNum', 'IsWeekend', 'IsMonthStart', 'IsMonthEnd',
        'CompetitionDistance', 'Promo2', 'CompetitionOpenSinceMonth', 
        'CompetitionOpenSinceYear', 'Promo2SinceMonth', 'Promo2SinceYear',
        'StateHoliday_a', 'StateHoliday_b', 'StateHoliday_c',
        'StoreType_b', 'StoreType_c', 'StoreType_d',
        'Assortment_b', 'Assortment_c'
    ]
    
    for field in numeric_fields:
        if field in data_dict:
            try:
                data_dict[field] = float(data_dict[field]) if field not in ['Store'] else int(data_dict[field])
            except (ValueError, TypeError):
                data_dict[field] = 0
    
    return data_dict


def preprocess(data):
    """
    Preprocess input data for model prediction.
    Supports dict input with optional store.csv merge and all feature engineering.
    """
    # Ensure we have a dict copy
    if isinstance(data, dict):
        result = data.copy()
    else:
        result = {}
    
    # Load store data for optional merging
    store_data = load_store_data()
    
    # Merge store info if available
    result = merge_store_info(result, store_data)
    
    # Extract date features
    result = extract_date_features(result)
    
    # Handle missing values
    result = handle_missing_values(result)
    
    # Apply one-hot encoding
    result = apply_one_hot_encoding(result)
    
    # Normalize numeric values
    result = normalize_numeric_values(result)
    
    return result


def prepare_dataframe(data_dict, expected_columns):
    """Convert preprocessed dict to DataFrame with expected columns in correct order."""
    # Build dict with all expected columns, filling missing with 0
    df_dict = {}
    for col in expected_columns:
        val = data_dict.get(col, 0)
        try:
            df_dict[col] = float(val)
        except (ValueError, TypeError):
            df_dict[col] = 0.0
    
    # Create DataFrame with correct column order
    df = pd.DataFrame([df_dict])[expected_columns]
    return df


def inverse_transform_prediction(log_prediction):
    """Inverse transform log-scaled prediction back to original scale."""
    return float(np.expm1(log_prediction))
