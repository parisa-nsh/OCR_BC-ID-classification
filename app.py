import os
from flask import Flask, request, render_template, jsonify, send_file
from werkzeug.utils import secure_filename
import cv2
import numpy as np
from ocr_processor import OCRProcessor
from data_storage import DataStorage
from analytics import Analytics, generate_visualizations
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure required directories exist
os.makedirs('static', exist_ok=True)
os.makedirs('uploads', exist_ok=True)

ocr_processor = OCRProcessor()
data_storage = DataStorage()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}

@app.route('/')
def index():
    # Create initial visualizations if they don't exist
    if not os.path.exists('static/gender_distribution.png'):
        try:
            generate_visualizations(data_storage)
        except Exception as e:
            print(f"Error generating initial visualizations: {e}")
            # Create empty visualizations to prevent errors
            for viz in ['gender_distribution', 'age_group_distribution', 'height_distribution', 'postal_code_distribution']:
                if not os.path.exists(f'static/{viz}.png'):
                    plt.figure()
                    plt.text(0.5, 0.5, 'No data available', ha='center', va='center')
                    plt.savefig(f'static/{viz}.png')
                    plt.close()
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' in request.files:
        # Single file upload from drag-and-drop
        file = request.files['file']
        if file and allowed_file(file.filename):
            try:
                result = process_file(file)
                return jsonify(result)
            except Exception as e:
                return jsonify({'success': False, 'error': str(e)}), 400
    elif 'files[]' in request.files:
        # Multiple files upload from form
        files = request.files.getlist('files[]')
        results = []
        
        for file in files:
            if file and allowed_file(file.filename):
                try:
                    result = process_file(file)
                    results.append({
                        'filename': file.filename,
                        'success': result['success'],
                        'data': result.get('data', {}),
                        'error': result.get('error', None)
                    })
                except Exception as e:
                    results.append({
                        'filename': file.filename,
                        'success': False,
                        'error': str(e)
                    })
        
        try:
            generate_visualizations(data_storage)
        except Exception as e:
            print(f"Error generating visualizations: {e}")
        
        return jsonify({'results': results})
    
    return jsonify({'error': 'No file part'}), 400

def process_file(file):
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    try:
        file.save(filepath)
        image = cv2.imread(filepath)
        
        if image is None:
            raise ValueError("Failed to read image")
        
        # Extract information
        info = ocr_processor.parse_id_card_info(image)
        info['filename'] = filename
        
        # Store the results
        data_storage.add_record(info)
        
        return {
            'success': True,
            'data': info
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }
        
    finally:
        # Clean up uploaded file
        if os.path.exists(filepath):
            os.remove(filepath)

@app.route('/export')
def export_csv():
    try:
        # Convert data to DataFrame
        df = pd.DataFrame(data_storage.data)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'id_card_data_{timestamp}.csv'
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Save to CSV
        df.to_csv(filepath, index=False)
        
        # Send file to user and then delete it
        return_data = send_file(
            filepath,
            mimetype='text/csv',
            as_attachment=True,
            download_name=filename
        )
        
        @return_data.call_on_close
        def cleanup():
            if os.path.exists(filepath):
                os.remove(filepath)
        
        return return_data
        
    except Exception as e:
        return str(e), 500

@app.route('/statistics')
def get_statistics():
    return jsonify(data_storage.get_statistics())

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)