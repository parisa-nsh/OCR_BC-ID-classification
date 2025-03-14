from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename
from ocr_processor import OCRProcessor
from data_storage import DataStorage
from analytics import Analytics

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('static', exist_ok=True)

# Initialize components
ocr_processor = OCRProcessor()
data_storage = DataStorage()
analytics = Analytics(data_storage)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    try:
        # Generate initial visualizations if they don't exist
        if not os.path.exists('static/gender_distribution.png'):
            analytics.generate_all_visualizations()
    except Exception as e:
        print(f"Error generating initial visualizations: {str(e)}")
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Process the image
            id_card_info = ocr_processor.extract_text(filepath)
            
            # Add age group
            id_card_info['age_group'] = ocr_processor.get_age_group(id_card_info['age'])
            
            # Save to storage
            data_storage.add_record(id_card_info)
            
            # Generate new visualizations
            analytics.generate_all_visualizations()
            
            return jsonify({
                'success': True,
                'message': 'File processed successfully',
                'data': id_card_info
            })
            
        except Exception as e:
            print(f"Error processing file: {str(e)}")
            return jsonify({'error': str(e)}), 500
        finally:
            # Clean up the uploaded file
            if os.path.exists(filepath):
                os.remove(filepath)
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/statistics')
def get_statistics():
    try:
        stats = data_storage.get_statistics()
        return jsonify({
            'success': True,
            'data': stats
        })
    except Exception as e:
        print(f"Error getting statistics: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    try:
        # Create initial visualizations
        analytics.generate_all_visualizations()
    except Exception as e:
        print(f"Error generating initial visualizations: {str(e)}")
    
    # Run the Flask app
    app.run(host='127.0.0.1', port=5000, debug=True) 