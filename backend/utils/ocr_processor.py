import easyocr
import numpy as np
from PIL import Image
from io import BytesIO
import logging

# Set up logging
logger = logging.getLogger(__name__)

class OCRProcessor:
    def __init__(self, languages=['en']):
        """
        Initialize EasyOCR processor
        
        Args:
            languages (list): List of languages to support. Default is ['en'] for English
        """
        try:
            self.languages = languages
            self.reader = easyocr.Reader(languages, gpu=False)  # Set gpu=True if you have CUDA
            logger.info(f"✅ EasyOCR initialized successfully with languages: {languages}")
            print(f"🔧 OCR Processor initialized with EasyOCR (Languages: {', '.join(languages)})")
        except Exception as e:
            logger.error(f"Failed to initialize EasyOCR: {e}")
            print(f"❌ EasyOCR initialization failed: {e}")
            raise

    def extract_text(self, image_data):
        """Extract text from image using EasyOCR"""
        try:
            # Open image from bytes
            image = Image.open(BytesIO(image_data))
            
            # Convert PIL Image to numpy array for EasyOCR
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            img_array = np.array(image)
            
            print(f"📸 Processing image: {image.size} pixels")
            logger.info(f"Processing image of size: {image.size}")
            
            # Extract text using EasyOCR
            results = self.reader.readtext(img_array, detail=1)  # detail=1 gives bounding box, text, confidence
            
            # Process results
            extracted_texts = []
            confidences = []
            bounding_boxes = []
            
            for (bbox, text, confidence) in results:
                if confidence > 0.1:  # Filter out very low confidence detections
                    extracted_texts.append(text)
                    confidences.append(confidence)
                    bounding_boxes.append(bbox)
            
            # Combine all detected text
            full_text = ' '.join(extracted_texts).strip()
            
            # Calculate average confidence
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0
            
            print(f"✅ OCR completed: {len(full_text)} characters extracted from {len(results)} detections")
            logger.info(f"OCR completed: {len(full_text)} characters, {len(results)} detections, avg confidence: {avg_confidence:.2f}")
            
            return {
                'success': True,
                'text': full_text if full_text else "No text detected in image",
                'confidence': round(avg_confidence * 100, 2),  # Convert to percentage
                'detections': len(results),
                'filtered_detections': len(extracted_texts),
                'image_size': image.size,
                'processing_method': 'EasyOCR',
                'languages': self.languages,
                'bounding_boxes': bounding_boxes[:10] if bounding_boxes else []  # Limit to first 10 for response size
            }
            
        except Exception as e:
            error_msg = f"EasyOCR processing error: {str(e)}"
            print(f"❌ {error_msg}")
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg,
                'text': '',
                'processing_method': 'EasyOCR'
            }

    def extract_text_with_coordinates(self, image_data):
        """Extract text with bounding box coordinates"""
        try:
            # Open image from bytes
            image = Image.open(BytesIO(image_data))
            
            # Convert PIL Image to numpy array
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            img_array = np.array(image)
            
            # Extract text with detailed information
            results = self.reader.readtext(img_array, detail=1)
            
            formatted_results = []
            for (bbox, text, confidence) in results:
                if confidence > 0.1:  # Filter low confidence
                    formatted_results.append({
                        'text': text,
                        'confidence': round(confidence * 100, 2),
                        'bounding_box': {
                            'top_left': [int(bbox[0][0]), int(bbox[0][1])],
                            'top_right': [int(bbox[1][0]), int(bbox[1][1])],
                            'bottom_right': [int(bbox[2][0]), int(bbox[2][1])],
                            'bottom_left': [int(bbox[3][0]), int(bbox[3][1])]
                        }
                    })
            
            return {
                'success': True,
                'results': formatted_results,
                'total_detections': len(formatted_results),
                'image_size': image.size,
                'processing_method': 'EasyOCR_Detailed'
            }
            
        except Exception as e:
            error_msg = f"EasyOCR detailed processing error: {str(e)}"
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg,
                'results': []
            }

    def test_installation(self):
        """Test if EasyOCR is properly installed and working"""
        try:
            # Create a simple test image with text
            test_image = Image.new('RGB', (200, 50), color='white')
            
            # Convert to numpy array
            img_array = np.array(test_image)
            
            # Test EasyOCR
            test_results = self.reader.readtext(img_array)
            
            return {
                'success': True,
                'message': 'EasyOCR is working properly',
                'languages_supported': self.languages,
                'gpu_enabled': self.reader.detector.device.type == 'cuda' if hasattr(self.reader.detector, 'device') else False,
                'test_results_count': len(test_results)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'EasyOCR installation or configuration issue'
            }

    def add_language(self, language_code):
        """Add support for additional language"""
        try:
            if language_code not in self.languages:
                new_languages = self.languages + [language_code]
                self.reader = easyocr.Reader(new_languages, gpu=False)
                self.languages = new_languages
                logger.info(f"Added language support: {language_code}")
                return {
                    'success': True,
                    'message': f'Language {language_code} added successfully',
                    'current_languages': self.languages
                }
            else:
                return {
                    'success': True,
                    'message': f'Language {language_code} already supported',
                    'current_languages': self.languages
                }
        except Exception as e:
            error_msg = f"Failed to add language {language_code}: {str(e)}"
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg
            }

    def get_supported_languages(self):
        """Get list of currently supported languages"""
        return {
            'current_languages': self.languages,
            'available_languages': [
                'en', 'hi', 'ar', 'zh', 'ja', 'ko', 'th', 'vi', 
                'fr', 'de', 'es', 'pt', 'ru', 'it', 'nl', 'pl'
            ]  # Common languages supported by EasyOCR
        }