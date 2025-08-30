import pytesseract
from PIL import Image
from io import BytesIO
import os
import platform

class OCRProcessor:
    def __init__(self, tesseract_config='--oem 3 --psm 6'):
        self.config = tesseract_config
        
        # Set tesseract path based on operating system
        system = platform.system()
        if system == "Windows":
            # Windows paths
            possible_paths = [
                r'C:\Program Files\Tesseract-OCR\tesseract.exe',
                r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
                r'C:\Users\{}\AppData\Local\Tesseract-OCR\tesseract.exe'.format(os.getenv('USERNAME', ''))
            ]
            
            tesseract_path = None
            for path in possible_paths:
                if os.path.exists(path):
                    tesseract_path = path
                    break
            
            if tesseract_path:
                pytesseract.pytesseract.tesseract_cmd = tesseract_path
            else:
                print("⚠️ Tesseract not found in common Windows locations")
                
        elif system == "Linux":
            # Linux/Ubuntu paths (for Render deployment)
            possible_paths = [
                '/usr/bin/tesseract',
                '/usr/local/bin/tesseract',
                '/app/.apt/usr/bin/tesseract'  # Render buildpack path
            ]
            
            tesseract_path = None
            for path in possible_paths:
                if os.path.exists(path):
                    tesseract_path = path
                    break
            
            if tesseract_path:
                pytesseract.pytesseract.tesseract_cmd = tesseract_path
                print(f"✅ Tesseract found at: {tesseract_path}")
            else:
                print("⚠️ Tesseract not found in common Linux locations")
                # Don't set path, let pytesseract use system PATH
                
        elif system == "Darwin":  # macOS
            # macOS paths
            possible_paths = [
                '/usr/local/bin/tesseract',
                '/opt/homebrew/bin/tesseract'
            ]
            
            tesseract_path = None
            for path in possible_paths:
                if os.path.exists(path):
                    tesseract_path = path
                    break
            
            if tesseract_path:
                pytesseract.pytesseract.tesseract_cmd = tesseract_path
        
        print(f"🔧 OCR Processor initialized on {system}")

    def extract_text(self, image_data):
        """Extract text from image using OCR"""
        try:
            # Open image from bytes
            image = Image.open(BytesIO(image_data))
            
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            print(f"📸 Processing image: {image.size} pixels")
            
            # Extract text using pytesseract
            text = pytesseract.image_to_string(image, config=self.config)
            
            # Get confidence scores
            try:
                data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
                confidences = [int(conf) for conf in data['conf'] if int(conf) > 0]
                avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            except Exception as conf_error:
                print(f"⚠️ Confidence calculation failed: {conf_error}")
                avg_confidence = 0
            
            extracted_text = text.strip()
            print(f"✅ OCR completed: {len(extracted_text)} characters extracted")
            
            return {
                'success': True,
                'text': extracted_text,
                'confidence': round(avg_confidence, 2),
                'image_size': image.size,
                'processing_method': 'OCR'
            }
            
        except Exception as e:
            print(f"❌ OCR processing error: {e}")
            return {
                'success': False,
                'error': f"OCR processing error: {str(e)}",
                'text': ''
            }

    def test_installation(self):
        """Test if Tesseract is properly installed"""
        try:
            # Create a simple test image
            test_image = Image.new('RGB', (200, 50), color='white')
            test_text = pytesseract.image_to_string(test_image)
            return {
                'success': True,
                'message': 'Tesseract is working properly',
                'version': pytesseract.get_tesseract_version()
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Tesseract installation issue'
            }