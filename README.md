# AI JobPylot - Advanced ATS Engine

A comprehensive Applicant Tracking System (ATS) powered by GPT-3.5-turbo with advanced matching, scoring, and analytics capabilities.

## 🚀 Features

### Core ATS Functionality
- **Resume Parsing & Analysis**: Convert PDF resumes to structured JSON with AI-powered parsing
- **Job-Candidate Matching**: Intelligent matching algorithm with multiple scoring criteria
- **ATS Compatibility Analysis**: Comprehensive resume optimization for ATS systems
- **Candidate Ranking**: Rank candidates for specific job positions
- **Job Recommendations**: Suggest relevant jobs for candidates

### Advanced Analytics
- **Multi-dimensional Scoring**: Skills, experience, education, keywords, and ATS compatibility
- **Detailed Feedback**: AI-generated feedback and improvement recommendations
- **Dashboard Analytics**: Real-time statistics and performance metrics
- **Trend Analysis**: Track improvements and identify patterns

### Resume Optimization
- **Summary Evaluation**: Analyze and improve resume summaries
- **Section-by-Section Analysis**: Detailed evaluation of each resume section
- **Keyword Optimization**: Identify missing keywords and suggest improvements
- **Content Rewriting**: AI-powered content improvement suggestions

## 🏗️ Architecture

```
AI JobPylot/
├── main_ats.py              # Main FastAPI application with ATS endpoints
├── main.py                  # Original resume analysis API
├── services/
│   ├── ats_engine.py        # Core ATS matching and scoring engine
│   ├── openai_service.py    # GPT-3.5 integration for analysis
│   └── pdf_parser.py        # PDF text extraction
├── models/
│   ├── schemas.py           # Original resume analysis schemas
│   └── ats_schemas.py       # ATS-specific data models
└── requirements.txt         # Python dependencies
```

## 🛠️ Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd AI_jobpylot
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

4. **Run the application**
```bash
# For the enhanced ATS system
python main_ats.py

# For the original resume analysis only
python main.py
```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

Once running, visit `http://localhost:8000/docs` for interactive API documentation.

## 🔧 Core Endpoints

### Resume Analysis (Original Features)
- `POST /upload-resume` - Upload and parse PDF resume
- `POST /evaluate-summary` - Evaluate resume summary
- `POST /suggest-relevant-skills` - Get skill suggestions
- `POST /rewrite-section` - Rewrite resume sections

### ATS Engine (New Features)

#### Job Management
```http
POST /ats/jobs
{
  "title": "Senior Python Developer",
  "required_skills": ["Python", "Django", "PostgreSQL"],
  "preferred_skills": ["React", "AWS", "Docker"],
  "experience_years": 5,
  "education_level": "Bachelor",
  "industry": "Technology",
  "location": "Remote",
  "description": "We are looking for an experienced Python developer..."
}
```

#### Candidate Registration
```http
POST /ats/candidates
{
  "candidate_id": "candidate_123",
  "resume_data": {
    "resume": {
      "Name": "John Doe",
      "Email": "john@example.com",
      "Skills": {...},
      "WorkExperience": [...],
      "Education": [...]
    }
  }
}
```

#### Matching & Scoring
```http
POST /ats/match
{
  "candidate_id": "candidate_123",
  "job_id": "job_456"
}
```

#### Candidate Ranking
```http
POST /ats/rank-candidates
{
  "job_id": "job_456",
  "limit": 10
}
```

#### Job Recommendations
```http
POST /ats/job-recommendations
{
  "candidate_id": "candidate_123",
  "limit": 5
}
```

#### ATS Compatibility Analysis
```http
POST /ats/analyze-resume
{
  "resume_data": {...}
}
```

## 🎯 Scoring Algorithm

The ATS engine uses a weighted scoring system:

- **Skills Match (30%)**: Required and preferred skills alignment
- **Experience Match (25%)**: Years of experience comparison
- **Keyword Match (20%)**: AI-powered keyword analysis
- **Education Match (15%)**: Education level requirements
- **ATS Compatibility (10%)**: Resume format and structure

### Score Calculation Example
```python
overall_score = (
    skills_match * 0.3 +
    experience_match * 0.25 +
    keyword_match * 0.2 +
    education_match * 0.15 +
    ats_compatibility * 0.1
)
```

## 📊 Analytics & Dashboard

### Dashboard Statistics
```http
GET /ats/dashboard
```

Returns:
- Total candidates and jobs
- Average match scores
- Top performing jobs
- Recent applications

### Detailed Analytics
```http
POST /ats/analytics
{
  "start_date": "2024-01-01",
  "end_date": "2024-01-31"
}
```

## 🔍 Search & Filter

### Candidate Search
```http
POST /ats/search/candidates
{
  "skills": ["Python", "JavaScript"],
  "experience_min": 3,
  "experience_max": 8,
  "education_level": "Bachelor",
  "limit": 20
}
```

### Job Search
```http
POST /ats/search/jobs
{
  "title_keywords": ["developer", "engineer"],
  "required_skills": ["Python"],
  "experience_years": 5,
  "location": "Remote",
  "limit": 20
}
```

## 🚀 Bulk Operations

### Bulk Job Posting
```http
POST /ats/bulk/jobs
{
  "jobs": [
    {
      "title": "Frontend Developer",
      "required_skills": ["React", "JavaScript"],
      ...
    },
    {
      "title": "Backend Developer", 
      "required_skills": ["Python", "Django"],
      ...
    }
  ]
}
```

### Bulk Candidate Registration
```http
POST /ats/bulk/candidates
{
  "candidates": [
    {
      "candidate_id": "candidate_1",
      "resume_data": {...}
    },
    {
      "candidate_id": "candidate_2", 
      "resume_data": {...}
    }
  ]
}
```

## 💡 Use Cases

### For Recruiters
1. **Job Posting Management**: Add and manage job requirements
2. **Candidate Screening**: Automatically rank candidates for positions
3. **Resume Analysis**: Get detailed feedback on candidate resumes
4. **Performance Analytics**: Track hiring metrics and trends

### For Job Seekers
1. **Resume Optimization**: Get ATS-specific improvement suggestions
2. **Job Matching**: Find positions that match your profile
3. **Skill Gap Analysis**: Identify missing skills for target roles
4. **Application Tracking**: Monitor application performance

### For HR Teams
1. **Bulk Processing**: Handle large volumes of applications
2. **Compliance**: Ensure consistent evaluation criteria
3. **Reporting**: Generate detailed hiring reports
4. **Integration**: Connect with existing HR systems

## 🔧 Configuration

### Environment Variables
```env
OPENAI_API_KEY=your_openai_api_key
LOG_LEVEL=INFO
API_HOST=0.0.0.0
API_PORT=8000
```

### Custom Scoring Weights
Modify the scoring weights in `services/ats_engine.py`:
```python
overall_score = (
    skills_match * 0.3 +      # Adjust these weights
    experience_match * 0.25 + # based on your needs
    education_match * 0.15 +
    keyword_match * 0.2 +
    ats_compatibility * 0.1
)
```

## 🧪 Testing

### Sample Data
```python
# Sample job posting
sample_job = {
    "title": "Senior Software Engineer",
    "required_skills": ["Python", "JavaScript", "React", "Node.js"],
    "preferred_skills": ["AWS", "Docker", "Kubernetes"],
    "experience_years": 5,
    "education_level": "Bachelor",
    "industry": "Technology",
    "location": "San Francisco, CA",
    "description": "We are seeking a senior software engineer..."
}

# Sample candidate
sample_candidate = {
    "candidate_id": "test_candidate_001",
    "resume_data": {
        "resume": {
            "Name": "Jane Smith",
            "Email": "jane@example.com",
            "Skills": {
                "TechStack": ["Python", "JavaScript", "React"],
                "Tools": ["Git", "Docker"],
                "soft_skills": ["Leadership", "Communication"]
            },
            "WorkExperience": [
                {
                    "JobTitle": "Software Engineer",
                    "Company": "Tech Corp",
                    "Duration": "3 years",
                    "Responsibilities": ["Developed web applications", "Led team of 5 developers"]
                }
            ],
            "Education": [
                {
                    "Degree": "Bachelor of Computer Science",
                    "Institution": "University of Technology"
                }
            ]
        }
    }
}
```

## 🔒 Security Considerations

1. **API Key Management**: Store OpenAI API keys securely
2. **Input Validation**: All inputs are validated using Pydantic models
3. **Rate Limiting**: Implement rate limiting for production use
4. **CORS Configuration**: Configure CORS for your specific domains
5. **Data Privacy**: Ensure compliance with data protection regulations

## 🚀 Production Deployment

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main_ats:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Setup
```bash
# Build and run with Docker
docker build -t ai-jobpylot .
docker run -p 8000:8000 -e OPENAI_API_KEY=your_key ai-jobpylot
```

## 📈 Performance Optimization

1. **Caching**: Implement Redis caching for frequently accessed data
2. **Database**: Use PostgreSQL for persistent storage
3. **Async Processing**: Use background tasks for heavy operations
4. **Load Balancing**: Deploy multiple instances behind a load balancer

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the API documentation at `/docs`
- Review the example implementations

## 🔄 Version History

- **v2.0.0**: Enhanced ATS engine with matching, scoring, and analytics
- **v1.0.0**: Basic resume analysis functionality

---

**AI JobPylot** - Transforming recruitment with AI-powered insights! 🚀 