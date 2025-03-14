# BC ID Card OCR Application

This application extracts text from BC ID cards using OCR technology and stores the data in a Neo4j graph database. It provides analytics and visualization of the extracted information.

## Features

- OCR text extraction from BC ID cards
- Data storage in Neo4j graph database
- Analytics on gender distribution
- Age group analysis (3 groups)
- Height distribution analysis
- Postal code grouping and analysis
- Graph visualization reports

## Setup Instructions

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Install Tesseract OCR:
- Windows: Download and install from https://github.com/UB-Mannheim/tesseract/wiki
- Linux: `sudo apt-get install tesseract-ocr`
- Mac: `brew install tesseract`

3. Set up Neo4j:
- Download and install Neo4j Desktop
- Create a new database
- Set up credentials in .env file

4. Configure environment variables:
Create a .env file with:
```
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
```

5. Run the application:
```bash
python app.py
```

## Project Structure

- `app.py`: Main Flask application
- `ocr_processor.py`: OCR processing module
- `neo4j_handler.py`: Neo4j database operations
- `analytics.py`: Data analysis and visualization
- `templates/`: HTML templates
- `static/`: Static files (CSS, JS, images)
- `uploads/`: Directory for uploaded ID card images 