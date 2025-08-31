# 🚀 Social Media Content Analyzer

A powerful full-stack application that analyzes social media posts and suggests engagement improvements. Upload PDFs or images, extract text using OCR, and get AI-powered insights optimized for Twitter, Instagram, Facebook, and LinkedIn.

## ✨ Features

- 📄 **Multi-format Support**: Upload PDF and image files for analysis
- 🔍 **Smart Text Extraction**: Direct PDF text extraction and OCR for scanned documents
- 🤖 **AI-Powered Analysis**: Google Gemini integration for intelligent content suggestions
- 📊 **Comprehensive Metrics**: Readability scores, engagement analysis, and platform optimization
- 🎯 **Platform-Specific Insights**: Tailored recommendations for different social media platforms
- 🏷️ **Social Elements Detection**: Automatic hashtag, mention, emoji, and CTA analysis

## 🛠️ Tech Stack

### Backend
- **Framework**: Python (Flask)
- **AI Integration**: Google Gemini API
- **Text Processing**: PyPDF2, pytesseract, Pillow, textstat, nltk
- **OCR Engine**: Tesseract OCR

### Frontend
- **Framework**: React.js 18
- **Build Tool**: Vite
- **Styling**: Modern CSS with responsive design
- **Features**: Drag-and-drop interface, real-time validation

## 📁 Project Structure

```
SOCIAL_MEDIA/
│
├── backend/                         # Flask backend
│   ├── __pycache__/                # Python cache files
│   ├── uploads/                     # Uploaded files directory
│   ├── utils/                       # Helper functions
│   │   ├── analyzer.py             # Content analysis logic
│   │   ├── ocr_processor.py        # OCR processing
│   │   └── pdf_processor.py        # PDF text extraction
│   ├── venv/                        # Virtual environment
│   ├── .dockerignore               # Docker ignore rules
│   ├── app.py                       # Main Flask application
│   ├── config.py                    # Configuration management
│   ├── Dockerfile                   # Docker container config
│   ├── Profile                      # Deployment profile
│   ├── requirements.txt             # Python dependencies
│   └── .env                         # Environment variables
│
├── frontend/                        # React frontend
│   ├── dist/                        # Build output directory
│   ├── node_modules/                # Node.js dependencies
│   ├── public/                      # Static assets
│   ├── src/                         # Source code
│   │   ├── components/              # React components
│   │   │   └── SocialMediaA...      # Main analyzer component
│   │   ├── App.jsx                  # Main app component
│   │   └── index.css                # Global styles
│   ├── .headers                     # HTTP headers config
│   ├── .env                         # Frontend environment variables
│   ├── eslint.config.js             # ESLint configuration
│   ├── index.html                   # HTML template
│   ├── netlify.toml                 # Netlify deployment config
│   ├── package-lock.json            # Dependency lock file
│   ├── package.json                 # Node dependencies
│   └── vite.config.js               # Vite configuration
│
├── .gitignore                       # Git ignore rules
└── README.md                        # Project documentation
```

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- Tesseract OCR

### 1. Clone the Repository
```bash
git clone https://github.com/vivekbajpai82/Social-Media-Content-Analyzer.git
cd Social-Media-Content-Analyzer
```

### 2. Backend Setup
```bash
# Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the `backend/` directory:
```env
API_KEY=your_google_gemini_api_key_here
TESSERACT_PATH=C:\Program Files\Tesseract-OCR\tesseract.exe
```

> **Note**: Update the Tesseract path in `backend/utils/ocr_processor.py` if installed in a different directory.

### 4. Frontend Setup
```bash
cd frontend
npm install
```

### 5. Running the Application

#### Start Backend
```bash
cd backend
python app.py
```
Backend runs on: `http://127.0.0.1:5000`

#### Start Frontend
```bash
cd frontend
npm run dev
```
Frontend runs on: `http://localhost:5173`

## 🎯 Usage

1. **Upload Content**: Drag and drop or select PDF/image files
2. **Automatic Processing**: Text extraction via OCR or direct PDF parsing
3. **AI Analysis**: Get intelligent engagement suggestions powered by Google Gemini
4. **Platform Insights**: View optimized recommendations for different social media platforms
5. **Export Results**: Download or print your analysis results

## 🏗️ Technical Architecture & Approach

### Architecture Overview
Full-stack application with **Python Flask backend** and **React frontend**, designed for extracting and analyzing social media content from documents and images.

### Backend Approach (Python)

#### Core Components
- **Flask API** with CORS configuration for cross-origin requests
- **Multi-format processing pipeline** supporting PDF and image files
- **Modular processor architecture** with dedicated classes for OCR, PDF, and content analysis

#### Text Extraction Strategy
- **OCR Processing**: Tesseract engine via pytesseract for image-to-text conversion with confidence scoring
- **PDF Processing**: PyPDF2 for direct text extraction from PDF documents
- **File validation and security** with secure filename handling and automatic cleanup

#### AI-Powered Analysis Engine
- **Google Gemini API integration** for intelligent content suggestions
- **Multi-dimensional analysis framework**:
  - Basic metrics (word count, readability scores via textstat)
  - Social elements detection (hashtags, mentions, emojis, CTAs)
  - Platform-specific optimization for Twitter, Instagram, Facebook, LinkedIn
  - Rule-based suggestion engine with priority levels

#### Robust Error Handling
- Graceful degradation with fallback processors
- Comprehensive logging and health check endpoints
- Service availability monitoring

### Frontend Approach (React)

#### User Experience Design
- **Modern React 18** with hooks (useState, useEffect, useRef)
- **Drag-and-drop interface** with real-time file validation
- **Progressive loading states** with animated feedback
- **Responsive grid layouts** for multi-platform results display

#### Results Visualization
- **Comprehensive analytics dashboard** showing content metrics, readability scores, and social elements
- **Platform suitability analysis** with visual indicators and recommendations
- **Priority-coded suggestions** with actionable improvement tips
- **Interactive features** including keyboard shortcuts and print functionality

#### Technical Implementation
**Key Technologies:**
- **Backend**: Flask, Google Generative AI, Tesseract OCR, PyPDF2, textstat
- **Frontend**: React 18, Vite build system, modern ES6+ features
- **Deployment**: Environment-based configuration with production readiness

## 🌟 Innovation Points

- **Multi-format content extraction** combining OCR and PDF processing
- **AI-enhanced suggestions** using Google Gemini for contextual recommendations
- **Real-time platform optimization** analysis across major social media platforms
- **Comprehensive readability assessment** with multiple scoring algorithms

## 🚀 Live Demo & Repository

**🌐 Live Application**: [https://social-content-analyzer.netlify.app/](https://social-content-analyzer.netlify.app/)

**📂 GitHub Repository**: [https://github.com/vivekbajpai82/Social-Media-Content-Analyzer](https://github.com/vivekbajpai82/Social-Media-Content-Analyzer)

## 📧 Contact

**Developer**: Vivek Bajpai  
**GitHub**: [@vivekbajpai82](https://github.com/vivekbajpai82)  
**Repository**: [Social-Media-Content-Analyzer](https://github.com/vivekbajpai82/Social-Media-Content-Analyzer)

---

⭐ **If you found this project helpful, please give it a star!** ⭐
