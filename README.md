# AI JobPylot - Unified ATS Checker

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A comprehensive **Applicant Tracking System (ATS) checker** that combines deterministic rule-based scoring with GPT-3.5 turbo content generation for optimal resume analysis and optimization.

## 🚀 Features

### **Hybrid ATS Analysis (100-point scoring)**
- **Deterministic Scoring**: Rule-based, reproducible ATS evaluation
- **GPT-3.5 Turbo Integration**: AI-powered content generation and detailed feedback
- **Section-by-Section Analysis**: 13 different resume aspects analyzed
- **Line-by-Line Analysis**: Detailed examination of each resume line
- **Magic Write**: AI-generated content for resume sections

### **Analysis Sections**
- 📄 **PDF to JSON Parser**: Convert PDF resumes to structured data
- 📝 **Summary Analysis**: Professional summary optimization
- 📅 **Date Formatting**: Consistent date presentation
- 💪 **Weak Verbs Detection**: Identify and replace weak action verbs
- 📊 **Quantity Impact**: Quantifiable achievements analysis
- 👥 **Teamwork Indicators**: Collaboration and teamwork assessment
- 🎯 **Buzzwords Detection**: Identify and replace clichés
- 📞 **Contact Details**: Professional contact information
- 📋 **Line-by-Line Analysis**: Detailed resume examination
- ✨ **Magic Write**: AI-generated content for sections
- 📚 **Grammar & Spelling**: UK and Indian English standards
- 🎨 **Formatting & Layout**: ATS compatibility assessment
- 🔍 **ATS Keywords**: Keyword optimization analysis
- 🛠️ **Skills Relevance**: Skills section assessment
- ⚖️ **Achievements vs Responsibilities**: Balance analysis

## 🏗️ Architecture

```
AI_jobpylot/
├── main.py                          # Unified FastAPI application
├── deterministic_ats_engine.py      # Rule-based scoring engine
├── enhanced_openai_service.py       # GPT-3.5 turbo integration
├── services/
│   └── pdf_parser.py               # PDF text extraction
├── models/
│   └── schemas.py                  # Pydantic data models
├── tests/
│   └── test_hybrid_ats.py         # Test suite
└── docs/
    └── README_HYBRID_ATS.md       # Detailed documentation
```

## 🚀 Quick Start

### **Installation**

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-jobpylot.git
cd ai-jobpylot

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your OpenAI API key
```

### **Running the Application**

```bash
# Start the server
python main.py

# Or using uvicorn directly
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

### **API Usage**

```bash
# Comprehensive analysis (100-point scoring)
curl -X POST "http://localhost:8001/hybrid/analyze-all-sections" \
  -F "file=@resume.pdf"

# Individual section analysis
curl -X POST "http://localhost:8001/hybrid/analyze-summary" \
  -F "file=@resume.pdf"

# Magic write content generation
curl -X POST "http://localhost:8001/hybrid/magic-write-section" \
  -F "section=summary" \
  -F "description=Professional software engineer with 5 years experience"
```

## 📊 Scoring System

### **Overall Score (100-point system)**
- **90-100**: A+ (Excellent)
- **80-89**: A (Very Good)
- **70-79**: B+ (Good)
- **60-69**: B (Above Average)
- **50-59**: C (Average)
- **40-49**: D (Below Average)
- **0-39**: F (Poor)

### **Section Scores (0-10 scale)**
- **9-10**: Excellent
- **7-8**: Good
- **5-6**: Average
- **3-4**: Below Average
- **0-2**: Poor

## 🔧 API Endpoints

### **Hybrid ATS Checker**
- `POST /hybrid/analyze-all-sections` - Comprehensive analysis
- `POST /hybrid/analyze-summary` - Summary analysis
- `POST /hybrid/analyze-dates` - Date formatting
- `POST /hybrid/analyze-weak-verbs` - Weak verbs detection
- `POST /hybrid/analyze-quantity-impact` - Quantifiable achievements
- `POST /hybrid/analyze-teamwork` - Teamwork indicators
- `POST /hybrid/analyze-buzzwords` - Buzzwords detection
- `POST /hybrid/analyze-contact-details` - Contact information
- `POST /hybrid/analyze-line-by-line` - Line-by-line analysis
- `POST /hybrid/magic-write-section` - Content generation
- `POST /hybrid/analyze-grammar-spelling` - Grammar/spelling check
- `POST /hybrid/analyze-formatting-layout` - Formatting analysis
- `POST /hybrid/analyze-ats-keywords` - Keyword optimization
- `POST /hybrid/analyze-skills-relevance` - Skills relevance
- `POST /hybrid/analyze-achievements-vs-responsibilities` - Balance analysis

### **Utility Endpoints**
- `GET /` - System information
- `GET /health` - Health check
- `GET /scoring-info` - Scoring system details
- `GET /api-info` - Complete API documentation

## 🧪 Testing

```bash
# Run tests
python -m pytest tests/

# Run specific test
python test_hybrid_ats.py
```

## 📚 Documentation

- **[Detailed Documentation](docs/README_HYBRID_ATS.md)** - Comprehensive guide
- **[API Reference](http://localhost:8001/docs)** - Interactive API docs
- **[Scoring System](http://localhost:8001/scoring-info)** - Scoring details

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/ai-jobpylot/issues)
- **Documentation**: [Detailed Guide](docs/README_HYBRID_ATS.md)
- **API Docs**: [Interactive Docs](http://localhost:8001/docs)

---

**AI JobPylot** - Your intelligent ATS optimization companion! 🚀 