import cv2
import numpy as np
import pytesseract
from PIL import Image
import re
from datetime import datetime

class OCRProcessor:
    def __init__(self):
        # Configure Tesseract path for Windows
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    def preprocess_image(self, image):
        """Preprocess the image for better OCR results"""
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply thresholding to preprocess the image
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        
        # Apply dilation to connect text components
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        gray = cv2.dilate(gray, kernel, iterations=1)
        
        return gray

    def extract_text(self, image_path):
        """Extract text from the ID card image"""
        # Read the image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Could not read image")

        # Preprocess the image
        processed_image = self.preprocess_image(image)
        
        # Extract text using Tesseract
        text = pytesseract.image_to_string(processed_image)
        
        return self.parse_id_card_info(text)

    def parse_id_card_info(self, text):
        """Parse the extracted text to get relevant information"""
        info = {
            'gender': 'Unknown',
            'age': 25,  # Default age if not found
            'height': 170,  # Default height if not found
            'postal_code': 'Unknown',
            'age_group': '25-49'  # Default age group
        }
        
        try:
            # Extract gender (M/F)
            gender_match = re.search(r'[MF]', text)
            if gender_match:
                info['gender'] = gender_match.group()

            # Extract age (assuming format: DOB: YYYY-MM-DD)
            dob_match = re.search(r'DOB:\s*(\d{4})-(\d{2})-(\d{2})', text)
            if dob_match:
                try:
                    dob = datetime(int(dob_match.group(1)), int(dob_match.group(2)), int(dob_match.group(3)))
                    today = datetime.now()
                    info['age'] = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                    info['age_group'] = self.get_age_group(info['age'])
                except (ValueError, TypeError):
                    # Keep default age if date is invalid
                    pass

            # Extract height (assuming format: Height: XXX cm)
            height_match = re.search(r'Height:\s*(\d{3})\s*cm', text)
            if height_match:
                try:
                    height = int(height_match.group(1))
                    if 100 <= height <= 250:  # Reasonable height range
                        info['height'] = height
                except (ValueError, TypeError):
                    # Keep default height if parsing fails
                    pass

            # Extract postal code (assuming format: XXX XXX)
            postal_match = re.search(r'[A-Z]\d[A-Z]\s*\d[A-Z]\d', text)
            if postal_match:
                info['postal_code'] = postal_match.group()

        except Exception as e:
            print(f"Error parsing ID card info: {str(e)}")
            # Return default values if parsing fails
            pass

        return info

    def get_age_group(self, age):
        """Categorize age into three groups"""
        try:
            age = int(age)
            if age < 25:
                return "18-24"
            elif age < 50:
                return "25-49"
            else:
                return "50+"
        except (ValueError, TypeError):
            return "25-49"  # Default age group if age is invalid 