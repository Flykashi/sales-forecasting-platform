import numpy as np
from .model_loader import get_model, get_columns
from .preprocess import preprocess, prepare_dataframe, inverse_transform_prediction


def predict_single(data):
    try:
        model = get_model()
        columns = get_columns()
        
        processed = preprocess(data)
        df = prepare_dataframe(processed, columns)
        
        pred_log = model.predict(df)[0]
        pred = inverse_transform_prediction(pred_log)
        pred = max(0, pred)
        
        return {
            'success': True,
            'prediction': round(pred, 2),
            'store': int(processed.get('Store', 0)),
            'date': f"{int(processed.get('Year'))}-{int(processed.get('Month')):02d}-{int(processed.get('Day')):02d}"
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}


def predict_batch(batch):
    try:
        if not batch:
            return {'success': False, 'error': 'empty batch'}
        
        model = get_model()
        columns = get_columns()
        
        predictions = []
        for i, item in enumerate(batch):
            processed = preprocess(item)
            df = prepare_dataframe(processed, columns)
            pred_log = model.predict(df)[0]
            pred = max(0, inverse_transform_prediction(pred_log))
            
            predictions.append({
                'index': i,
                'prediction': round(pred, 2),
                'store': int(processed.get('Store', 0)),
                'date': f"{int(processed.get('Year'))}-{int(processed.get('Month')):02d}-{int(processed.get('Day')):02d}"
            })
        
        preds = [p['prediction'] for p in predictions]
        return {
            'success': True,
            'count': len(predictions),
            'predictions': predictions,
            'avg': round(np.mean(preds), 2),
            'min': round(np.min(preds), 2),
            'max': round(np.max(preds), 2)
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}


def get_model_info():
    try:
        model = get_model()
        columns = get_columns()
        
        return {
            'success': True,
            'type': type(model).__name__,
            'features': len(columns),
            'n_estimators': getattr(model, 'n_estimators', 'N/A'),
            'max_depth': getattr(model, 'max_depth', 'N/A')
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}


def get_fields():
    return {
        'success': True,
        'fields': {
            'store': {'type': 'int', 'required': True},
            'day_of_week': {'type': 'int'},
            'date': {'type': 'string'},
            'promo': {'type': 'int', 'default': 0},
            'school_holiday': {'type': 'int', 'default': 0},
            'state_holiday': {'type': 'string', 'default': '0'},
            'store_type': {'type': 'string', 'default': 'a'},
            'assortment': {'type': 'string', 'default': 'a'},
            'competition_distance': {'type': 'float', 'default': 0},
            'promo2': {'type': 'int', 'default': 0}
        }
    }
