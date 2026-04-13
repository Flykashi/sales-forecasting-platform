from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from routes.predict import predict_bp
from routes.upload import upload_bp
from routes.insights import insights_bp
import os

# Point Flask's static folder at the frontend directory
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), '..', 'frontend')

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path='')
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

CORS(app)
app.register_blueprint(predict_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(insights_bp)


# Serve the frontend
@app.route('/')
def index():
    return send_from_directory(FRONTEND_DIR, 'index.html')

@app.route("/")
def home():
    return "Backend is running "


@app.route('/health', methods=['GET'])
def health_check():
    try:
        from services.model_loader import get_model, get_columns
        get_model()
        get_columns()
        return jsonify({'status': 'healthy'}), 200
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500


@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad Request'}), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not Found'}), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal Server Error'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
