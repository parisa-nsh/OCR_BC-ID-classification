# OCR BC ID Classification System

A web-based application for extracting and analyzing information from British Columbia ID cards using Optical Character Recognition (OCR). The system provides visual analytics for demographic data including gender distribution, age groups, height distribution, and geographical distribution of postal codes.

## Features

- 📷 Image Upload & OCR Processing
- 📊 Real-time Data Visualization
- 🗺️ Interactive Postal Code Map
- 📈 Statistical Analysis
- 💾 Local Data Storage
- 🌐 Web-based Interface

## Installation

1. Clone the repository:
```bash
git clone https://github.com/parisa-nsh/OCR_BC-ID-classification.git
cd OCR_BC-ID-classification
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create required directories:
```bash
mkdir -m static uploads data
```

## Usage

1. Start the Flask application:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

3. Upload an ID card image using the web interface:
   - Drag and drop an image or click to select
   - Wait for processing
   - View extracted information and updated visualizations

## Project Structure

```
OCR_BC-ID-classification/
├── app.py              # Main Flask application
├── analytics.py        # Data visualization and analysis
├── data_storage.py     # Data management
├── ocr_processor.py    # OCR processing
├── templates/          # HTML templates
│   └── index.html     # Main web interface
├── static/            # Static files and generated visualizations
├── uploads/           # Temporary storage for uploaded images
└── data/             # Persistent data storage
```

## Dependencies

- Python 3.8+
- Flask
- Tesseract OCR
- OpenCV
- Matplotlib
- Pandas
- Folium
- Geopy

## Development

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 