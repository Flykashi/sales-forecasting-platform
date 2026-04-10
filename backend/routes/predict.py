from flask import Blueprint, request, jsonify
from services.model_loader import get_model, get_columns
from services.preprocess import preprocess, prepare_dataframe, inverse_transform_prediction

predict_bp = Blueprint('predict', __name__, url_prefix='/api')


@predict_bp.route('/predict', methods=['POST'])
def predict():
    """
    Prediction endpoint supporting:
    - Single object: {"Store": 1, "Month": 3, ...}
    - List of objects: [{"Store": 1, ...}, {"Store": 2, ...}]
    - Wrapped format: {"data": [{"Store": 1, ...}, ...]}
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No JSON data provided'}), 400

        # Normalize input to list of dicts
        items = []
        if isinstance(data, dict):
            if 'data' in data and isinstance(data['data'], list):
                items = data['data']
            else:
                items = [data]
        elif isinstance(data, list):
            items = data
        else:
            return jsonify({'success': False, 'error': 'Invalid input format'}), 400

        if not items:
            return jsonify({'success': False, 'error': 'No prediction data provided'}), 400

        # Load model and columns
        try:
            model = get_model()
            columns = get_columns()
        except FileNotFoundError as e:
            return jsonify({'success': False, 'error': f'Model loading failed: {str(e)}'}), 503

        # Single vs batch
        if len(items) == 1:
            return _single_prediction(items[0], model, columns)
        else:
            return _batch_prediction(items, model, columns)

    except Exception as e:
        return jsonify({'success': False, 'error': f'Internal server error: {str(e)}'}), 500


def _single_prediction(item, model, columns):
    """Handle single prediction request."""
    try:
        preprocessed = preprocess(item)
        df = prepare_dataframe(preprocessed, columns)
        pred_log = model.predict(df)[0]
        pred = inverse_transform_prediction(pred_log)
        pred = max(0, pred)

        return jsonify({
            'success': True,
            'prediction': round(pred, 2),
            'store': int(preprocessed.get('Store', 0)),
            'date': f"{int(preprocessed.get('Year'))}-{int(preprocessed.get('Month')):02d}-{int(preprocessed.get('Day')):02d}"
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': f'Prediction failed: {str(e)}'}), 400


def _batch_prediction(items, model, columns):
    """Handle batch prediction request."""
    predictions = []
    errors = []

    for idx, item in enumerate(items):
        try:
            preprocessed = preprocess(item)
            df = prepare_dataframe(preprocessed, columns)
            pred_log = model.predict(df)[0]
            pred = inverse_transform_prediction(pred_log)
            pred = max(0, pred)

            predictions.append({
                'index': idx,
                'prediction': round(pred, 2),
                'store': int(preprocessed.get('Store', 0)),
                'date': f"{int(preprocessed.get('Year'))}-{int(preprocessed.get('Month')):02d}-{int(preprocessed.get('Day')):02d}"
            })
        except Exception as e:
            errors.append({'index': idx, 'error': str(e)})

    if not predictions:
        return jsonify({'success': False, 'error': 'All predictions failed', 'errors': errors}), 400

    response = {
        'success': True,
        'total': len(items),
        'successful': len(predictions),
        'failed': len(errors),
        'predictions': predictions
    }

    if predictions:
        preds_values = [p['prediction'] for p in predictions]
        response.update({
            'average': round(float(sum(preds_values) / len(preds_values)), 2),
            'min': round(float(min(preds_values)), 2),
            'max': round(float(max(preds_values)), 2)
        })

    if errors:
        response['errors'] = errors

    return jsonify(response), 200


@predict_bp.route('/model-info', methods=['GET'])
def model_info():
    """Get metadata about the loaded model."""
    try:
        model = get_model()
        columns = get_columns()
        
        # Extract model info based on type
        model_type = type(model).__name__
        model_info = {
            'type': model_type,
            'n_features': len(columns),
            'features': list(columns)
        }
        
        # Add model-specific attributes if available
        if hasattr(model, 'n_estimators'):
            model_info['n_estimators'] = model.n_estimators
        if hasattr(model, 'max_depth'):
            model_info['max_depth'] = model.max_depth
        if hasattr(model, 'learning_rate'):
            model_info['learning_rate'] = model.learning_rate
        
        return jsonify({
            'success': True,
            'model': model_info
        }), 200
    
    except FileNotFoundError as e:
        return jsonify({
            'success': False,
            'error': f'Model not available: {str(e)}'
        }), 503
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error retrieving model info: {str(e)}'
        }), 500

