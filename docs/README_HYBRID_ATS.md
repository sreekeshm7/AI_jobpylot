# AI JobPylot - Hybrid ATS Checker - Detailed Documentation

## 📋 Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [API Reference](#api-reference)
6. [Scoring System](#scoring-system)
7. [Usage Examples](#usage-examples)
8. [Development](#development)
9. [Troubleshooting](#troubleshooting)
10. [Contributing](#contributing)

## 🎯 Overview

AI JobPylot is a comprehensive **Applicant Tracking System (ATS) checker** that combines deterministic rule-based scoring with GPT-3.5 turbo content generation. This hybrid approach provides both reliable, reproducible results and intelligent, detailed feedback for resume optimization.

### Key Features

- **🔢 Deterministic Scoring**: Rule-based, reproducible ATS evaluation
- **🤖 GPT-3.5 Turbo Integration**: AI-powered content generation and detailed feedback
- **📊 100-Point Overall Scoring**: Comprehensive evaluation with letter grades
- **📋 Section-by-Section Analysis**: 13 different resume aspects analyzed
- **📝 Line-by-Line Analysis**: Detailed examination of each resume line
- **✨ Magic Write**: AI-generated content for resume sections
- **🌍 Multi-Language Support**: UK and Indian English grammar/spelling checks

## 🏗️ Architecture

### System Components

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
    └── README_HYBRID_ATS.md       # This documentation
```

### Core Components

1. **DeterministicATSEngine**: Rule-based scoring system
2. **EnhancedOpenAIService**: GPT-3.5 turbo integration
3. **PDFParser**: PDF text extraction service
4. **HybridATSChecker**: Main orchestrator
5. **FastAPI Application**: Web API endpoints

## 🚀 Installation

### Prerequisites

- Python 3.8+
- OpenAI API key
- pip package manager

### Step-by-Step Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/ai-jobpylot.git
cd ai-jobpylot

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp env.example .env
# Edit .env with your OpenAI API key

# 5. Run the application
python main.py
```

### Docker Installation

```bash
# Build and run with Docker
docker-compose up -d

# Or build manually
docker build -t ai-jobpylot .
docker run -p 8001:8001 -e OPENAI_API_KEY=your-key ai-jobpylot
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# OpenAI API Configuration
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_MAX_TOKENS=2000
OPENAI_TEMPERATURE=0.7

# Application Configuration
APP_NAME=AI JobPylot
APP_VERSION=2.0.0
DEBUG=True
LOG_LEVEL=INFO

# Server Configuration
HOST=0.0.0.0
PORT=8001
RELOAD=True
```

### Scoring Configuration

The system uses a dual scoring approach:

- **Overall Score**: 0-100 points with letter grades
- **Section Scores**: 0-10 points for individual sections

## 📚 API Reference

### Base URL
```
http://localhost:8001
```

### Authentication
Currently, no authentication is required. For production use, implement proper authentication.

### Endpoints

#### Hybrid ATS Checker Endpoints

##### 1. Comprehensive Analysis
```http
POST /hybrid/analyze-all-sections
Content-Type: multipart/form-data

file: resume.pdf
```

**Response:**
```json
{
  "filename": "resume.pdf",
  "overall_score": {
    "score": 85.5,
    "percentage": 85.5,
    "max_score": 100.0,
    "grade": "A (Very Good)"
  },
  "section_analyses": {
    "summary": { ... },
    "dates": { ... },
    "weak_verbs": { ... }
  },
  "timestamp": "2024-01-15T10:30:00"
}
```

##### 2. Individual Section Analysis
```http
POST /hybrid/analyze-summary
POST /hybrid/analyze-dates
POST /hybrid/analyze-weak-verbs
POST /hybrid/analyze-quantity-impact
POST /hybrid/analyze-teamwork
POST /hybrid/analyze-buzzwords
POST /hybrid/analyze-contact-details
POST /hybrid/analyze-line-by-line
POST /hybrid/analyze-grammar-spelling
POST /hybrid/analyze-formatting-layout
POST /hybrid/analyze-ats-keywords
POST /hybrid/analyze-skills-relevance
POST /hybrid/analyze-achievements-vs-responsibilities
```

##### 3. Magic Write Content Generation
```http
POST /hybrid/magic-write-section
Content-Type: multipart/form-data

section: summary
description: Professional software engineer with 5 years experience
file: resume.pdf (optional)
```

#### Utility Endpoints

##### 1. Health Check
```http
GET /health
```

##### 2. Scoring Information
```http
GET /scoring-info
```

##### 3. API Information
```http
GET /api-info
```

## 📊 Scoring System

### Overall Score (100-point system)

| Score Range | Grade | Description |
|-------------|-------|-------------|
| 90-100 | A+ | Excellent |
| 80-89 | A | Very Good |
| 70-79 | B+ | Good |
| 60-69 | B | Above Average |
| 50-59 | C | Average |
| 40-49 | D | Below Average |
| 0-39 | F | Poor |

### Section Scores (0-10 scale)

| Score Range | Description |
|-------------|-------------|
| 9-10 | Excellent |
| 7-8 | Good |
| 5-6 | Average |
| 3-4 | Below Average |
| 0-2 | Poor |

### Scoring Factors

- **Strong Verbs**: +0.5 per strong verb
- **Quantifiable Achievements**: +1.0 per metric
- **Buzzwords**: -0.5 per buzzword
- **ATS Keywords**: +1.5 per keyword match
- **Contact Completeness**: +2.0 per required field
- **Grammar Errors**: -0.1 per error

## 💡 Usage Examples

### Python Client Example

```python
import requests

# Comprehensive analysis
with open('resume.pdf', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:8001/hybrid/analyze-all-sections', files=files)
    analysis = response.json()
    
    print(f"Overall Score: {analysis['overall_score']['score']}/100")
    print(f"Grade: {analysis['overall_score']['grade']}")
    
    for section, data in analysis['section_analyses'].items():
        score = data['deterministic_score']['score']
        print(f"{section}: {score}/10")

# Magic write content generation
data = {
    'section': 'summary',
    'description': 'Experienced software engineer with expertise in Python and FastAPI'
}
response = requests.post('http://localhost:8001/hybrid/magic-write-section', data=data)
content = response.json()
print(f"Generated content: {content['generated_content']}")
```

### cURL Examples

```bash
# Comprehensive analysis
curl -X POST "http://localhost:8001/hybrid/analyze-all-sections" \
  -F "file=@resume.pdf"

# Individual section analysis
curl -X POST "http://localhost:8001/hybrid/analyze-summary" \
  -F "file=@resume.pdf"

# Magic write with job keywords
curl -X POST "http://localhost:8001/hybrid/analyze-ats-keywords" \
  -F "file=@resume.pdf" \
  -F "job_keywords=python,fastapi,postgresql"

# Health check
curl "http://localhost:8001/health"
```

### JavaScript/Node.js Example

```javascript
const FormData = require('form-data');
const fs = require('fs');

async function analyzeResume() {
    const form = new FormData();
    form.append('file', fs.createReadStream('resume.pdf'));
    
    const response = await fetch('http://localhost:8001/hybrid/analyze-all-sections', {
        method: 'POST',
        body: form
    });
    
    const analysis = await response.json();
    console.log(`Overall Score: ${analysis.overall_score.score}/100`);
    console.log(`Grade: ${analysis.overall_score.grade}`);
}

analyzeResume();
```

## 🛠️ Development

### Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python test_hybrid_ats.py

# Run with coverage
python -m pytest tests/ --cov=. --cov-report=html
```

### Code Quality

```bash
# Linting
make lint

# Formatting
make format

# Clean cache
make clean
```

### Development Server

```bash
# Run with auto-reload
make dev

# Or manually
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

### Docker Development

```bash
# Build and run
make docker-build
make docker-run

# View logs
make docker-logs

# Stop containers
make docker-stop
```

## 🔧 Troubleshooting

### Common Issues

#### 1. OpenAI API Key Error
```
Error: OpenAI API key not found
```
**Solution**: Set your OpenAI API key in the `.env` file:
```env
OPENAI_API_KEY=your-actual-api-key-here
```

#### 2. PDF Parsing Issues
```
Error: Could not extract text from PDF
```
**Solution**: Ensure the PDF is not password-protected and contains extractable text.

#### 3. Memory Issues
```
Error: Out of memory
```
**Solution**: Increase system memory or use smaller PDF files.

#### 4. Port Already in Use
```
Error: Address already in use
```
**Solution**: Change the port in `.env` or kill the existing process:
```bash
lsof -ti:8001 | xargs kill -9
```

### Debug Mode

Enable debug mode for detailed logging:

```env
DEBUG=True
LOG_LEVEL=DEBUG
```

### Health Check

Check if all services are running:

```bash
curl http://localhost:8001/health
```

## 🤝 Contributing

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Set up development environment:
   ```bash
   make setup
   ```
4. Make your changes
5. Run tests:
   ```bash
   make test
   ```
6. Submit a pull request

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Add docstrings for functions
- Write tests for new features

### Testing

- Write unit tests for new functionality
- Ensure all tests pass before submitting PR
- Add integration tests for API endpoints

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/ai-jobpylot/issues)
- **Documentation**: This file and [main README](../README.md)
- **API Docs**: [Interactive Docs](http://localhost:8001/docs)

---

**AI JobPylot** - Your intelligent ATS optimization companion! 🚀 