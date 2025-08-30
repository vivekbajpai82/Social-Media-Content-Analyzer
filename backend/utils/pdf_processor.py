import PyPDF2
from io import BytesIO

class PDFProcessor:
    @staticmethod
    def extract_text(file_data):
        """Extract text from PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(BytesIO(file_data))
            text = ""
            
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return {
                'success': True,
                'text': text.strip(),
                'pages': len(pdf_reader.pages),
                'metadata': pdf_reader.metadata
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"PDF processing error: {str(e)}"
            }