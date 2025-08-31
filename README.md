------------------------------------------------------------------------------------------------------------
-->Social Media Content Analyzer

   This project analyzes social media posts and suggests engagement improvements.
   It supports PDFs and scanned images (OCR), extracts text, and provides insights for platforms like Twitter, Instagram, Facebook, and LinkedIn.
------------------------------------------------------------------------------------------------------------
-->Features

   Upload PDF and image files for analysis.
   Text extraction from PDFs.
   OCR for scanned documents and images (using Tesseract).
   AI-powered content analysis for engagement insights.
   Suggestions for readability, hashtags, calls-to-action, and platform suitability.
------------------------------------------------------------------------------------------------------------
🛠️ Tech Stack

   Backend: Python (Flask)
   Frontend:  React.js (JavaScript, HTML, CSS)  
   Libraries/Tools: PyPDF2, pytesseract, Pillow, textstat, nltk, React Router
   OCR Engine: Tesseract OCR

------------------------------------------------------------------------------------------------------------
--> Social Media Content Analyzer - Technical Approach

   ## Architecture Overview
   Full-stack application with **Python Flask backend** and **React frontend**, designed for extracting and analyzing social media content from documents and images.


   ## Backend Approach (Python)
   ### Core Components
   - **Flask API** with CORS configuration for cross-origin requests
   - **Multi-format processing pipeline** supporting PDF and image files
   - **Modular processor architecture** with dedicated classes for OCR, PDF, and content analysis

   ### Text Extraction Strategy
   - **OCR Processing**: Tesseract engine via pytesseract for image-to-text conversion with confidence scoring
   - **PDF Processing**: PyPDF2 for direct text extraction from PDF documents
   - **File validation and security** with secure filename handling and automatic cleanup

   ### AI-Powered Analysis Engine
   - **Google Gemini API integration** for intelligent content suggestions
   - **Multi-dimensional analysis framework**:
   - Basic metrics (word count, readability scores via textstat)
   - Social elements detection (hashtags, mentions, emojis, CTAs)
   - Platform-specific optimization for Twitter, Instagram, Facebook, LinkedIn
   - Rule-based suggestion engine with priority levels

   ### Robust Error Handling
   - Graceful degradation with fallback processors
   - Comprehensive logging and health check endpoints
   - Service availability monitoring


   ## Frontend Approach (React)
   ### User Experience Design
   - **Modern React 18** with hooks (useState, useEffect, useRef)
   - **Drag-and-drop interface** with real-time file validation
   - **Progressive loading states** with animated feedback
   - **Responsive grid layouts** for multi-platform results display

   ### Results Visualization
   - **Comprehensive analytics dashboard** showing content metrics, readability scores, and social elements
   - **Platform suitability analysis** with visual indicators and recommendations
   - **Priority-coded suggestions** with actionable improvement tips
   - **Interactive features** including keyboard shortcuts and print functionality

   ## Technical Implementation

   ### Key Technologies
   - **Backend**: Flask, Google Generative AI, Tesseract OCR, PyPDF2, textstat
   - **Frontend**: React 18, Vite build system, modern ES6+ features
   - **Deployment**: Environment-based configuration with production readiness

   ### Innovation Points
   - **Multi-format content extraction** combining OCR and PDF processing
   - **AI-enhanced suggestions** using Google Gemini for contextual recommendations
   - **Real-time platform optimization** analysis across major social media platforms
   - **Comprehensive readability assessment** with multiple scoring algorithms
------------------------------------------------------------------------------------------------------------   
-->Installation & Setup

   1. Clone the repository
      git clone <repo-url>
      cd SOCIAL_MEDIA

   2. Create and activate virtual environment
      python -m venv venv
      Windows: venv\Scripts\activate
      Mac/Linux: source venv/bin/activate

   3. Install dependencies
      pip install -r backend/requirements.txt

   4. Set up Environment Variables
      Create a .env file inside the backend folder and add:
      API_KEY=your_api_key_here

   5. Update The Tesseract Path
      TESSERACT_PATH=C:\Program Files\Tesseract-OCR\tesseract.exe
      Note:
      Currently, the Tesseract path is hardcoded in backend/utils/ocr_processor.py.
      If you install Tesseract in a different directory, update that path accordingly, otherwise OCR will not work.

   6. Running the Application
      ->Start the Backend
        cd backend
        python app.py
        The backend will run on http://127.0.0.1:5000

      ->start the frontend
        cd frontend
        npm install (domnload node_modules)
        npm run dev
        now the frontend and backend is connected
        open browser and type
        http://localhost:5173
   
        Simply Use The Project

------------------------------------------------------------------------------------------------------------
-->Project Structure
       
     SOCIAL_MEDIA/
      │
      ├── backend/                         # Flask / FastAPI backend
      │   ├── app.py                       # Main entry
      │   ├── config.py                    # Configurations (read from .env)
      │   ├── utils/                       # Helper functions (e.g. OCR, NLP)
      │   ├── uploads/                     # Uploaded files (ignored in git)
      │   ├── requirements.txt             # Backend dependencies
      │   ├── Procfile                     # For Render/Heroku: web: gunicorn app:app
      │   ├── apt.txt                      # System dependencies (tesseract, poppler etc.)
      │   └── .env                         # SECRET keys (ignored in git)
      │
      ├── frontend/                        # React + Vite frontend
      │   ├── public/                      # Static assets
      │   ├── src/
      │   │   ├── components/              # React components
      │   │   ├── App.jsx
      │   │   ├── index.css
      │   │   └── main.jsx
      │   ├── package.json                 # Frontend dependencies
      │   ├── vite.config.js               # Vite configuration
      │   ├── .env                         # API url (VITE_API_URL=https://...)
      │   └── ...
      │
      ├── .gitignore                       # Single root ignore (frontend + backend)
      └── README.md                        # Project setup & instructions

-----------------------------------------------------------------------------------------------------------
-->Usage
    1. Upload a PDF or image file
    2. Extract text automatically
    3. Get AI-powered engagement suggestions
    4. View insights for different social platforms
-----------------------------------------------------------------------------------------------------------
--> Live Link 
    https://social-content-analyzer.netlify.app/
--> github repository link
    https://github.com/vivekbajpai82/Social-Media-Content-Analyzer
