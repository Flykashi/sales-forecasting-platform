from datetime import datetime

from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import pandas as pd
import os
from db import insert_record
from services.services import predict_batch

upload_bp = Blueprint('upload', __name__, url_prefix='/api')


def _get_field(item, *keys):
    for key in keys:
        if key in item:
            return item[key]
    return None


def _build_upload_record(item, prediction):
    return {
        'source': 'upload_predict',
        'store': _get_field(item, 'Store', 'store'),
        'date': _get_field(item, 'Date', 'date'),
        'Promo': _get_field(item, 'Promo', 'promo'),
        'StateHoliday': _get_field(item, 'StateHoliday', 'state_holiday'),
        'StoreType': _get_field(item, 'StoreType', 'store_type'),
        'Assortment': _get_field(item, 'Assortment', 'assortment'),
        'CompetitionDistance': _get_field(item, 'CompetitionDistance', 'competition_distance'),
        'Promo2': _get_field(item, 'Promo2', 'promo2'),
        'prediction': round(prediction, 2),
        'created_at': datetime.utcnow().isoformat()
    }

ALLOWED_EXTENSIONS = {'csv'}
MAX_FILE_SIZE = 50 * 1024 * 1024
UPLOAD_FOLDER = 'uploads'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@upload_bp.route('/upload/predict', methods=['POST'])
def upload_predict():
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '' or not allowed_file(file.filename):
            return jsonify({'success': False, 'error': 'Invalid file'}), 400
        
        file.seek(0, os.SEEK_END)
        if file.tell() > MAX_FILE_SIZE:
            return jsonify({'success': False, 'error': 'File too large'}), 400
        file.seek(0)
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        try:
            df = pd.read_csv(filepath)
            batch_data = df.to_dict('records')
            
            if len(batch_data) == 0:
                return jsonify({'success': False, 'error': 'CSV is empty'}), 400
            
            result = predict_batch(batch_data)
            result['file'] = filename
            result['rows'] = len(batch_data)

            if result.get('success') and 'predictions' in result:
                for prediction in result['predictions']:
                    try:
                        idx = prediction.get('index')
                        if idx is None or idx >= len(batch_data):
                            continue
                        insert_record(_build_upload_record(batch_data[idx], prediction.get('prediction', 0)))
                    except Exception:
                        pass
            
            return jsonify(result), (200 if result.get('success') else 400)
            
        finally:
            if os.path.exists(filepath):
                try:
                    os.remove(filepath)
                except:
                    pass
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@upload_bp.route('/upload/template', methods=['GET'])
def template():
    try:
        data = {
            'Store': [1, 2, 3],
            'DayOfWeek': [2, 3, 4],
            'Date': ['2024-07-15', '2024-07-16', '2024-07-17'],
            'Promo': [1, 0, 1],
            'SchoolHoliday': [0, 0, 0],
            'StateHoliday': ['0', '0', 'a'],
            'StoreType': ['b', 'c', 'd'],
            'Assortment': ['b', 'c', 'a'],
            'CompetitionDistance': [500.0, 1000.0, 250.5],
            'Promo2': [0, 1, 0]
        }
        
        df = pd.DataFrame(data)
        return {
            'success': True,
            'template': df.to_csv(index=False),
            'columns': list(df.columns)
        }, 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

