import os
import pytest
from ocr_processor import OCRProcessor
from PIL import Image
import numpy as np

@pytest.fixture
def ocr_processor():
    return OCRProcessor()

@pytest.fixture
def sample_image():
    # Create a blank test image
    img = Image.new('RGB', (300, 200), color='white')
    return np.array(img)

def test_ocr_processor_initialization(ocr_processor):
    assert ocr_processor is not None

def test_preprocess_image(ocr_processor, sample_image):
    processed_image = ocr_processor.preprocess_image(sample_image)
    assert processed_image is not None
    assert isinstance(processed_image, np.ndarray)

def test_parse_id_card_info_empty_image(ocr_processor, sample_image):
    result = ocr_processor.parse_id_card_info(sample_image)
    assert isinstance(result, dict)
    assert 'gender' in result
    assert 'age' in result
    assert 'height' in result
    assert 'postal_code' in result

def test_get_age_group():
    processor = OCRProcessor()
    
    assert processor.get_age_group(18) == '18-24'
    assert processor.get_age_group(24) == '18-24'
    assert processor.get_age_group(25) == '25-49'
    assert processor.get_age_group(49) == '25-49'
    assert processor.get_age_group(50) == '50+'
    assert processor.get_age_group(65) == '50+'

def test_validate_postal_code():
    processor = OCRProcessor()
    
    # Valid postal codes
    assert processor.validate_postal_code('V6B 4N8')
    assert processor.validate_postal_code('M5V 2H1')
    
    # Invalid postal codes
    assert not processor.validate_postal_code('12345')
    assert not processor.validate_postal_code('ABC DEF')
    assert not processor.validate_postal_code('')

def test_validate_height():
    processor = OCRProcessor()
    
    # Valid heights
    assert processor.validate_height(170)
    assert processor.validate_height(150)
    assert processor.validate_height(190)
    
    # Invalid heights
    assert not processor.validate_height(50)  # Too short
    assert not processor.validate_height(250)  # Too tall
    assert not processor.validate_height(-170)  # Negative 