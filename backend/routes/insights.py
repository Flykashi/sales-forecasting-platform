from flask import Blueprint, jsonify
from services.services import get_model_info, get_fields
from services.model_loader import get_columns

insights_bp = Blueprint('insights', __name__, url_prefix='/api')


@insights_bp.route('/insights/model-info', methods=['GET'])
def model_info():
    try:
        result = get_model_info()
        status = 200 if result.get('success') else 500
        return jsonify(result), status
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@insights_bp.route('/insights/fields', methods=['GET'])
def fields():
    try:
        result = get_fields()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@insights_bp.route('/insights/features', methods=['GET'])
def model_features():
    try:
        columns = get_columns()
        return jsonify({
            'success': True,
            'total': len(columns),
            'features': list(columns)
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

