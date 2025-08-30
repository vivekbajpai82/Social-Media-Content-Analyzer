import pytesseract
from PIL import Image
from io import BytesIO
import os

class OCRProcessor:
    def __init__(self, tesseract_config='--oem 3 --psm 6'):
        self.config = tesseract_config
        # Set tesseract path according to your system
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    
    def extract_text(self, image_data):
        """Extract text from image using OCR"""
        try:
            image = Image.open(BytesIO(image_data))
            
            # Convert to RGB 
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Extract text using pytesseract
            text = pytesseract.image_to_string(image, config=self.config)
            
            # Get confidence scores
            data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
            confidences = [int(conf) for conf in data['conf'] if int(conf) > 0]
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            return {
                'success': True,
                'text': text.strip(),
                'confidence': round(avg_confidence, 2),
                'image_size': image.size
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"OCR processing error: {str(e)}"
            }