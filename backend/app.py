from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import uuid
from datetime import datetime
import logging

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# CORS configuration for development and production
CORS(app, origins=[
    "http://localhost:5173",  # Vite dev server default
    "http://localhost:3000",  # React dev server alternative
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
    # Add your production frontend URLs here
    # "https://your-app.vercel.app",
    # "https://your-app.netlify.app"
])

# Configuration
class Config:
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}

app.config.from_object(Config)

# Create upload directory
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Import processors with error handling
try:
    from utils.pdf_processor import PDFProcessor
    from utils.ocr_processor import OCRProcessor
    from utils.analyzer import SocialMediaAnalyzer
    
    # Initialize processors
    pdf_processor = PDFProcessor()
    ocr_processor = OCRProcessor()
    analyzer = SocialMediaAnalyzer()
    
    processors_loaded = True
    logger.info("All processors loaded successfully")
    
except ImportError as e:
    logger.error(f"Failed to import processors: {e}")
    processors_loaded = False
    
    # Fallback processors
    class FallbackProcessor:
        def extract_text(self, file_data):
            return {
                'success': False,
                'error': 'Processor not available',
                'text': ''
            }
        
        def analyze_content(self, text):
            return {
                'success': False,
                'error': 'Analyzer not available',
                'suggestions': []
            }
    
    pdf_processor = FallbackProcessor()
    ocr_processor = FallbackProcessor()
    analyzer = FallbackProcessor()

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Remove the static file serving routes - React dev server handles this
@app.route('/')
def index():
    """API status endpoint"""
    return jsonify({
        'message': 'Social Media Content Analyzer API',
        'status': 'running',
        'version': '1.0.0',
        'endpoints': {
            'upload': '/api/upload',
            'analyze': '/api/analyze', 
            'health': '/api/health'
        },
        'frontend_info': 'React frontend should be served separately on port 5173 (Vite dev server)'
    })

# React frontend will be served separately on different platform
# No static file serving needed - pure API backend

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle file upload and processing"""
    try:
        # Check if processors are available
        if not processors_loaded:
            return jsonify({
                'error': 'Service temporarily unavailable. Please check server configuration.',
                'details': 'Text processing modules not loaded'
            }), 503

        # Validate request
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            allowed_types = ', '.join(app.config['ALLOWED_EXTENSIONS'])
            return jsonify({
                'error': f'File type not supported. Allowed types: {allowed_types}'
            }), 400
        
        # Generate unique filename
        original_filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{original_filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        # Save and read file
        file.save(filepath)
        
        try:
            with open(filepath, 'rb') as f:
                file_data = f.read()
            
            file_size = len(file_data)
            logger.info(f"Processing file: {original_filename}, Size: {file_size} bytes")
            
        except Exception as e:
            logger.error(f"Error reading file {filepath}: {e}")
            return jsonify({'error': 'Failed to read uploaded file'}), 500
        
        finally:
            # Clean up uploaded file
            try:
                if os.path.exists(filepath):
                    os.remove(filepath)
            except Exception as e:
                logger.warning(f"Failed to cleanup file {filepath}: {e}")
        
        # Process file based on type
        file_extension = original_filename.rsplit('.', 1)[1].lower()
        
        try:
            if file_extension == 'pdf':
                result = pdf_processor.extract_text(file_data)
                processing_method = 'PDF'
            else:
                result = ocr_processor.extract_text(file_data)
                processing_method = 'OCR'
                
        except Exception as e:
            logger.error(f"Error during text extraction: {e}")
            return jsonify({
                'error': 'Text extraction failed',
                'details': str(e)
            }), 500
        
        if not result.get('success', False):
            return jsonify({
                'error': result.get('error', 'Text extraction failed'),
                'processing_method': processing_method
            }), 500
        
        extracted_text = result.get('text', '')
        
        if not extracted_text or len(extracted_text.strip()) < 10:
            return jsonify({
                'error': 'No readable text found in the document',
                'extracted_text': extracted_text,
                'processing_method': processing_method
            }), 400
        
        # Analyze extracted text
        try:
            analysis = analyzer.analyze_content(extracted_text)
        except Exception as e:
            logger.error(f"Error during content analysis: {e}")
            analysis = {
                'error': 'Analysis failed',
                'details': str(e),
                'suggestions': []
            }
        
        # Prepare response
        response_data = {
            'success': True,
            'extracted_text': extracted_text,
            'file_info': {
                'filename': original_filename,
                'size': file_size,
                'type': file_extension,
                'pages': result.get('pages', 1) if file_extension == 'pdf' else 1
            },
            'analysis': analysis,
            'processing_info': {
                'timestamp': datetime.now().isoformat(),
                'method': processing_method,
                'text_length': len(extracted_text),
                'word_count': len(extracted_text.split())
            }
        }
        
        # Add OCR-specific info
        if processing_method == 'OCR' and 'confidence' in result:
            response_data['processing_info']['ocr_confidence'] = result['confidence']
        
        logger.info(f"Successfully processed {original_filename}")
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"Unexpected error in upload_file: {e}")
        return jsonify({
            'error': 'Internal server error occurred during file processing',
            'details': str(e)
        }), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_text():
    """Analyze provided text for social media optimization"""
    try:
        if not processors_loaded:
            return jsonify({
                'error': 'Analysis service temporarily unavailable'
            }), 503

        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
        
        text = data['text'].strip()
        
        if not text:
            return jsonify({'error': 'Empty text provided'}), 400
        
        if len(text) < 10:
            return jsonify({'error': 'Text too short for meaningful analysis'}), 400
        
        try:
            analysis = analyzer.analyze_content(text)
        except Exception as e:
            logger.error(f"Error during text analysis: {e}")
            return jsonify({
                'error': 'Analysis failed',
                'details': str(e)
            }), 500
        
        return jsonify({
            'success': True,
            'analysis': analysis,
            'text_info': {
                'length': len(text),
                'word_count': len(text.split()),
                'character_count': len(text)
            },
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Unexpected error in analyze_text: {e}")
        return jsonify({
            'error': 'Internal server error during text analysis',
            'details': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'processors_loaded': processors_loaded,
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0',
        'upload_folder_exists': os.path.exists(app.config['UPLOAD_FOLDER']),
        'gemini_api_configured': bool(os.getenv('GEMINI_API_KEY')),
        'cors_origins': [
            "http://localhost:5173",
            "http://localhost:3000", 
            "http://127.0.0.1:5173",
            "http://127.0.0.1:3000"
        ]
    })

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    return jsonify({
        'error': 'File too large',
        'max_size': f"{app.config['MAX_CONTENT_LENGTH'] // (1024*1024)}MB"
    }), 413

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle internal server errors"""
    logger.error(f"Internal server error: {e}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    logger.info("Starting Social Media Content Analyzer API Server...")
    logger.info(f"Upload folder: {app.config['UPLOAD_FOLDER']}")
    logger.info(f"Processors loaded: {processors_loaded}")
    logger.info(f"Gemini API configured: {bool(os.getenv('GEMINI_API_KEY'))}")
    logger.info("Backend API running on: http://localhost:5000")
    logger.info("Frontend should run on: http://localhost:5173 (Vite dev server)")
    
    # Production vs Development
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    
    app.run(debug=debug_mode, host='0.0.0.0', port=port)