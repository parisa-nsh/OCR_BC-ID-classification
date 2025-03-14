import os
import pytest
from app import app
from PIL import Image
import io

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['UPLOAD_FOLDER'] = 'test_uploads'
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    with app.test_client() as client:
        yield client
    
    # Cleanup
    for file in os.listdir(app.config['UPLOAD_FOLDER']):
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file))
    os.rmdir(app.config['UPLOAD_FOLDER'])

@pytest.fixture
def sample_image():
    # Create a test image
    img = Image.new('RGB', (300, 200), color='white')
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return img_io

def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'BC ID Card OCR' in response.data

def test_upload_without_file(client):
    response = client.post('/upload', data={})
    assert response.status_code == 400
    assert b'No file part' in response.data

def test_upload_with_invalid_file(client):
    data = {'file': (io.BytesIO(b'not an image'), 'test.txt')}
    response = client.post('/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 400
    assert b'Invalid file type' in response.data

def test_upload_with_valid_image(client, sample_image):
    data = {'file': (sample_image, 'test.png')}
    response = client.post('/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    assert b'Results' in response.data

def test_get_statistics(client):
    response = client.get('/statistics')
    assert response.status_code == 200
    data = response.get_json()
    assert 'gender_distribution' in data
    assert 'age_group_distribution' in data
    assert 'height_distribution' in data
    assert 'postal_code_distribution' in data 