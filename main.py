#!/usr/bin/env python3
"""
AI JobPylot - Unified ATS Checker
Combines original ATS functionality with hybrid deterministic + GPT-3.5 turbo analysis
"""

from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Dict, Any, List, Optional
import uuid
from datetime import datetime
import re
import json
import logging
from dataclasses import dataclass
from enum import Enum

# Import existing services
from services.pdf_parser import PDFParser
from enhanced_openai_service import EnhancedOpenAIService
from models.schemas import *
from deterministic_ats_engine import DeterministicATSEngine, DeterministicScore

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AnalysisSection(Enum):
    PDF_TO_JSON = "pdf_to_json"
    SUMMARY = "summary"
    DATES = "dates"
    WEAK_VERBS = "weak_verbs"
    QUANTITY_IMPACT = "quantity_impact"
    TEAMWORK = "teamwork"
    BUZZWORDS = "buzzwords"
    UNNECESSARY_SECTIONS = "unnecessary_sections"
    CONTACT_DETAILS = "contact_details"
    LINE_BY_LINE = "line_by_line"
    MAGIC_WRITE = "magic_write"
    GRAMMAR_SPELLING = "grammar_spelling"
    FORMATTING_LAYOUT = "formatting_layout"
    ATS_KEYWORDS = "ats_keywords"
    SKILLS_RELEVANCE = "skills_relevance"
    ACHIEVEMENTS_VS_RESPONSIBILITIES = "achievements_vs_responsibilities"

class HybridATSChecker:
    """Hybrid ATS checker combining deterministic scoring with GPT-3.5 turbo generation"""
    
    def __init__(self):
        self.deterministic_engine = DeterministicATSEngine()
        self.openai_service = EnhancedOpenAIService()
        self.pdf_parser = PDFParser()
    
    async def analyze_section(self, section: AnalysisSection, resume_data: Dict[str, Any], 
                            resume_text: str = None, job_keywords: List[str] = None) -> Dict[str, Any]:
        """Analyze a specific section using hybrid approach"""
        
        # Get deterministic score
        deterministic_score = self._get_deterministic_score(section, resume_data, job_keywords)
        
        # Get GPT-3.5 turbo analysis for detailed feedback
        gpt_analysis = await self._get_gpt_analysis(section, resume_data, resume_text)
        
        return {
            "section": section.value,
            "deterministic_score": {
                "score": deterministic_score.score,
                "percentage": deterministic_score.get_percentage(),
                "max_score": deterministic_score.max_score
            },
            "gpt_analysis": gpt_analysis,
            "timestamp": datetime.now().isoformat()
        }
    
    def _get_deterministic_score(self, section: AnalysisSection, resume_data: Dict[str, Any], 
                                job_keywords: List[str] = None) -> DeterministicScore:
        """Get deterministic score for a section"""
        
        if section == AnalysisSection.SUMMARY:
            return self.deterministic_engine.score_summary(resume_data.get('Summary', ''))
        elif section == AnalysisSection.DATES:
            return self.deterministic_engine.score_dates(resume_data)
        elif section == AnalysisSection.WEAK_VERBS:
            return self.deterministic_engine.score_weak_verbs(resume_data)
        elif section == AnalysisSection.QUANTITY_IMPACT:
            return self.deterministic_engine.score_quantity_impact(resume_data)
        elif section == AnalysisSection.TEAMWORK:
            return self.deterministic_engine.score_teamwork(resume_data)
        elif section == AnalysisSection.BUZZWORDS:
            return self.deterministic_engine.score_buzzwords(resume_data)
        elif section == AnalysisSection.CONTACT_DETAILS:
            return self.deterministic_engine.score_contact_details(resume_data)
        elif section == AnalysisSection.GRAMMAR_SPELLING:
            return self.deterministic_engine.score_grammar_spelling(resume_data)
        elif section == AnalysisSection.FORMATTING_LAYOUT:
            return self.deterministic_engine.score_formatting_layout(resume_data)
        elif section == AnalysisSection.ATS_KEYWORDS:
            return self.deterministic_engine.score_ats_keywords(resume_data, job_keywords)
        elif section == AnalysisSection.SKILLS_RELEVANCE:
            return self.deterministic_engine.score_skills_relevance(resume_data)
        elif section == AnalysisSection.ACHIEVEMENTS_VS_RESPONSIBILITIES:
            return self.deterministic_engine.score_achievements_vs_responsibilities(resume_data)
        elif section == AnalysisSection.UNNECESSARY_SECTIONS:
            return self.deterministic_engine.score_unnecessary_sections(resume_data)
        else:
            return DeterministicScore(0.0)
    
    async def _get_gpt_analysis(self, section: AnalysisSection, resume_data: Dict[str, Any], 
                               resume_text: str = None) -> Dict[str, Any]:
        """Get GPT-3.5 turbo analysis for detailed feedback"""
        
        section_prompts = {
            AnalysisSection.SUMMARY: "Analyze the resume summary for ATS optimization. Focus on clarity, impact, and keyword optimization.",
            AnalysisSection.DATES: "Review date formatting throughout the resume for consistency and ATS compatibility.",
            AnalysisSection.WEAK_VERBS: "Identify weak verbs and suggest stronger action verbs for better impact.",
            AnalysisSection.QUANTITY_IMPACT: "Analyze quantifiable achievements and suggest improvements for measurable impact.",
            AnalysisSection.TEAMWORK: "Evaluate teamwork and collaboration indicators in the resume.",
            AnalysisSection.BUZZWORDS: "Identify buzzwords and clichés that should be replaced with specific achievements.",
            AnalysisSection.CONTACT_DETAILS: "Review contact information completeness and professional presentation.",
            AnalysisSection.GRAMMAR_SPELLING: "Check grammar and spelling, focusing on UK and Indian English standards.",
            AnalysisSection.FORMATTING_LAYOUT: "Analyze formatting and layout for ATS compatibility and professional appearance.",
            AnalysisSection.ATS_KEYWORDS: "Evaluate keyword optimization for ATS systems and suggest relevant keywords.",
            AnalysisSection.SKILLS_RELEVANCE: "Assess skills section relevance and suggest improvements.",
            AnalysisSection.ACHIEVEMENTS_VS_RESPONSIBILITIES: "Analyze the balance between achievements and responsibilities.",
            AnalysisSection.UNNECESSARY_SECTIONS: "Identify unnecessary sections and suggest improvements."
        }
        
        prompt = section_prompts.get(section, "Analyze this resume section for ATS optimization.")
        
        try:
            # Use GPT-3.5 turbo for detailed analysis
            analysis = await self.openai_service.analyze_section_with_gpt(
                section.value, resume_data, prompt
            )
            return analysis
        except Exception as e:
            logger.error(f"GPT analysis failed for section {section.value}: {str(e)}")
            return {"error": f"GPT analysis failed: {str(e)}"}
    
    async def magic_write_section(self, section: str, description: str, 
                                resume_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate content for a specific section using GPT-3.5 turbo"""
        
        try:
            # Use GPT-3.5 turbo for content generation
            generated_content = await self.openai_service.generate_section_content(
                section, description, resume_data
            )
            
            return {
                "section": section,
                "original_description": description,
                "generated_content": generated_content,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Magic write failed for section {section}: {str(e)}")
            return {"error": f"Magic write failed: {str(e)}"}
    
    async def line_by_line_analysis(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform line-by-line analysis of the resume"""
        
        try:
            # Convert resume data to text for line-by-line analysis
            resume_text = json.dumps(resume_data, default=str, indent=2)
            lines = resume_text.split('\n')
            
            line_analysis = []
            for i, line in enumerate(lines):
                if line.strip():
                    # Analyze each non-empty line
                    line_score = self.deterministic_engine.analyze_line(line)
                    line_analysis.append({
                        "line_number": i + 1,
                        "content": line.strip(),
                        "score": line_score.score,
                        "feedback": line_score.get_percentage()
                    })
            
            return {
                "total_lines": len(lines),
                "analyzed_lines": len(line_analysis),
                "line_analysis": line_analysis,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Line-by-line analysis failed: {str(e)}")
            return {"error": f"Line-by-line analysis failed: {str(e)}"}

# Create FastAPI app
app = FastAPI(
    title="AI JobPylot - Unified ATS Checker",
    description="Comprehensive ATS analysis with deterministic scoring and GPT-3.5 turbo generation",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the hybrid ATS checker
hybrid_checker = HybridATSChecker()

def get_grade(score: float) -> str:
    """Get letter grade based on 100-point score"""
    if score >= 90:
        return "A+ (Excellent)"
    elif score >= 80:
        return "A (Very Good)"
    elif score >= 70:
        return "B+ (Good)"
    elif score >= 60:
        return "B (Above Average)"
    elif score >= 50:
        return "C (Average)"
    elif score >= 40:
        return "D (Below Average)"
    else:
        return "F (Poor)"

# ============================================================================
# HYBRID ATS CHECKER ENDPOINTS (100-point scoring system)
# ============================================================================

@app.get("/")
async def root():
    return {
        "message": "AI JobPylot - Unified ATS Checker",
        "version": "2.0.0",
        "status": "running",
        "features": [
            "Hybrid ATS Scoring (100-point system)",
            "Deterministic Rule-based Analysis",
            "GPT-3.5 Turbo Content Generation",
            "Section-by-Section Analysis",
            "Line-by-Line Analysis",
            "Magic Write Content Generation",
            "Comprehensive ATS Optimization"
        ],
        "endpoints": {
            "hybrid": "/hybrid/* - Hybrid ATS checker endpoints",
            "original": "/original/* - Original ATS checker endpoints",
            "utility": "/health, /scoring-info - Utility endpoints"
        }
    }

# Hybrid ATS Checker Endpoints
@app.post("/hybrid/analyze-pdf-to-json")
async def hybrid_analyze_pdf_to_json(file: UploadFile = File(...)):
    """Convert PDF to JSON and analyze structure"""
    try:
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
        # Parse PDF to text
        resume_text = await hybrid_checker.pdf_parser.parse_pdf(file)
        if not resume_text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from PDF")
        
        # Parse to structured JSON using OpenAI
        resume_data = hybrid_checker.pdf_parser.parse_resume_to_json(resume_text)
        
        return {
            "filename": file.filename,
            "extraction_method": "openai_gpt35_turbo",
            "parsed_data": resume_data,
            "text_length": len(resume_text),
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        logger.error(f"PDF to JSON analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"PDF to JSON analysis failed: {str(e)}")


@app.post("/hybrid/analyze-summary")
async def hybrid_analyze_summary(file: UploadFile = File(...)):
    """Analyze resume summary section"""
    try:
        resume_text = await hybrid_checker.pdf_parser.parse_pdf(file)
        resume_data = hybrid_checker.openai_service.parse_resume_to_json(resume_text)
        
        analysis = await hybrid_checker.analyze_section(AnalysisSection.SUMMARY, resume_data, resume_text)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Summary analysis failed: {str(e)}")

@app.post("/hybrid/analyze-dates")
async def hybrid_analyze_dates(file: UploadFile = File(...)):
    """Analyze date formatting throughout resume"""
    try:
        resume_text = await hybrid_checker.pdf_parser.parse_pdf(file)
        resume_data = hybrid_checker.openai_service.parse_resume_to_json(resume_text)
        
        analysis = await hybrid_checker.analyze_section(AnalysisSection.DATES, resume_data, resume_text)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Date analysis failed: {str(e)}")

@app.post("/hybrid/analyze-weak-verbs")
async def hybrid_analyze_weak_verbs(file: UploadFile = File(...)):
    """Analyze weak verb usage and suggest improvements"""
    try:
        resume_text = await hybrid_checker.pdf_parser.parse_pdf(file)
        resume_data = hybrid_checker.openai_service.parse_resume_to_json(resume_text)
        
        analysis = await hybrid_checker.analyze_section(AnalysisSection.WEAK_VERBS, resume_data, resume_text)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Weak verbs analysis failed: {str(e)}")

@app.post("/hybrid/analyze-quantity-impact")
async def hybrid_analyze_quantity_impact(file: UploadFile = File(...)):
    """Analyze quantifiable impact and achievements"""
    try:
        resume_text = await hybrid_checker.pdf_parser.parse_pdf(file)
        resume_data = hybrid_checker.openai_service.parse_resume_to_json(resume_text)
        
        analysis = await hybrid_checker.analyze_section(AnalysisSection.QUANTITY_IMPACT, resume_data, resume_text)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Quantity impact analysis failed: {str(e)}")

@app.post("/hybrid/analyze-teamwork")
async def hybrid_analyze_teamwork(file: UploadFile = File(...)):
    """Analyze teamwork and collaboration indicators"""
    try:
        resume_text = await hybrid_checker.pdf_parser.parse_pdf(file)
        resume_data = hybrid_checker.openai_service.parse_resume_to_json(resume_text)
        
        analysis = await hybrid_checker.analyze_section(AnalysisSection.TEAMWORK, resume_data, resume_text)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Teamwork analysis failed: {str(e)}")

@app.post("/hybrid/analyze-buzzwords")
async def hybrid_analyze_buzzwords(file: UploadFile = File(...)):
    """Analyze buzzwords and clichés"""
    try:
        resume_text = await hybrid_checker.pdf_parser.parse_pdf(file)
        resume_data = hybrid_checker.openai_service.parse_resume_to_json(resume_text)
        
        analysis = await hybrid_checker.analyze_section(AnalysisSection.BUZZWORDS, resume_data, resume_text)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Buzzwords analysis failed: {str(e)}")

@app.post("/hybrid/analyze-unnecessary-sections")
async def hybrid_analyze_unnecessary_sections(file: UploadFile = File(...)):
    """Analyze unnecessary sections and suggest improvements"""
    try:
        resume_text = await hybrid_checker.pdf_parser.parse_pdf(file)
        resume_data = hybrid_checker.openai_service.parse_resume_to_json(resume_text)
        
        analysis = await hybrid_checker.analyze_section(AnalysisSection.UNNECESSARY_SECTIONS, resume_data, resume_text)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unnecessary sections analysis failed: {str(e)}")

@app.post("/hybrid/analyze-contact-details")
async def hybrid_analyze_contact_details(file: UploadFile = File(...)):
    """Analyze contact details completeness and presentation"""
    try:
        resume_text = await hybrid_checker.pdf_parser.parse_pdf(file)
        resume_data = hybrid_checker.openai_service.parse_resume_to_json(resume_text)
        
        analysis = await hybrid_checker.analyze_section(AnalysisSection.CONTACT_DETAILS, resume_data, resume_text)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Contact details analysis failed: {str(e)}")

@app.post("/hybrid/analyze-line-by-line")
async def hybrid_analyze_line_by_line(file: UploadFile = File(...)):
    """Perform line-by-line analysis of the resume"""
    try:
        resume_text = await hybrid_checker.pdf_parser.parse_pdf(file)
        resume_data = hybrid_checker.openai_service.parse_resume_to_json(resume_text)
        
        analysis = await hybrid_checker.line_by_line_analysis(resume_data)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Line-by-line analysis failed: {str(e)}")

@app.post("/hybrid/magic-write-section")
async def hybrid_magic_write_section(
    section: str,
    description: str,
    file: Optional[UploadFile] = File(None)
):
    """Generate content for a specific section using GPT-3.5 turbo"""
    try:
        resume_data = None
        if file:
            resume_text = await hybrid_checker.pdf_parser.parse_pdf(file)
            resume_data = hybrid_checker.openai_service.parse_resume_to_json(resume_text)
        
        generated_content = await hybrid_checker.magic_write_section(section, description, resume_data)
        return generated_content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Magic write failed: {str(e)}")

@app.post("/hybrid/analyze-grammar-spelling")
async def hybrid_analyze_grammar_spelling(file: UploadFile = File(...)):
    """Analyze grammar and spelling with UK and Indian English standards"""
    try:
        resume_text = await hybrid_checker.pdf_parser.parse_pdf(file)
        resume_data = hybrid_checker.openai_service.parse_resume_to_json(resume_text)
        
        analysis = await hybrid_checker.analyze_section(AnalysisSection.GRAMMAR_SPELLING, resume_data, resume_text)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Grammar and spelling analysis failed: {str(e)}")

@app.post("/hybrid/analyze-formatting-layout")
async def hybrid_analyze_formatting_layout(file: UploadFile = File(...)):
    """Analyze formatting and layout for ATS compatibility"""
    try:
        resume_text = await hybrid_checker.pdf_parser.parse_pdf(file)
        resume_data = hybrid_checker.openai_service.parse_resume_to_json(resume_text)
        
        analysis = await hybrid_checker.analyze_section(AnalysisSection.FORMATTING_LAYOUT, resume_data, resume_text)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Formatting and layout analysis failed: {str(e)}")

@app.post("/hybrid/analyze-ats-keywords")
async def hybrid_analyze_ats_keywords(
    file: UploadFile = File(...),
    job_keywords: Optional[str] = None
):
    """Analyze ATS keyword optimization"""
    try:
        resume_text = await hybrid_checker.pdf_parser.parse_pdf(file)
        resume_data = hybrid_checker.openai_service.parse_resume_to_json(resume_text)
        
        keywords = None
        if job_keywords:
            keywords = [kw.strip() for kw in job_keywords.split(',')]
        
        analysis = await hybrid_checker.analyze_section(AnalysisSection.ATS_KEYWORDS, resume_data, resume_text, keywords)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ATS keywords analysis failed: {str(e)}")

@app.post("/hybrid/analyze-skills-relevance")
async def hybrid_analyze_skills_relevance(file: UploadFile = File(...)):
    """Analyze skills section relevance and suggest improvements"""
    try:
        resume_text = await hybrid_checker.pdf_parser.parse_pdf(file)
        resume_data = hybrid_checker.openai_service.parse_resume_to_json(resume_text)
        
        analysis = await hybrid_checker.analyze_section(AnalysisSection.SKILLS_RELEVANCE, resume_data, resume_text)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Skills relevance analysis failed: {str(e)}")

@app.post("/hybrid/analyze-achievements-vs-responsibilities")
async def hybrid_analyze_achievements_vs_responsibilities(file: UploadFile = File(...)):
    """Analyze balance between achievements and responsibilities"""
    try:
        resume_text = await hybrid_checker.pdf_parser.parse_pdf(file)
        resume_data = hybrid_checker.openai_service.parse_resume_to_json(resume_text)
        
        analysis = await hybrid_checker.analyze_section(AnalysisSection.ACHIEVEMENTS_VS_RESPONSIBILITIES, resume_data, resume_text)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Achievements vs responsibilities analysis failed: {str(e)}")

@app.post("/hybrid/analyze-all-sections")
async def hybrid_analyze_all_sections(file: UploadFile = File(...)):
    """Analyze all sections comprehensively with 100-point scoring"""
    try:
        resume_text = await hybrid_checker.pdf_parser.parse_pdf(file)
        resume_data = hybrid_checker.openai_service.parse_resume_to_json(resume_text)
        
        sections = [
            AnalysisSection.SUMMARY,
            AnalysisSection.DATES,
            AnalysisSection.WEAK_VERBS,
            AnalysisSection.QUANTITY_IMPACT,
            AnalysisSection.TEAMWORK,
            AnalysisSection.BUZZWORDS,
            AnalysisSection.CONTACT_DETAILS,
            AnalysisSection.GRAMMAR_SPELLING,
            AnalysisSection.FORMATTING_LAYOUT,
            AnalysisSection.ATS_KEYWORDS,
            AnalysisSection.SKILLS_RELEVANCE,
            AnalysisSection.ACHIEVEMENTS_VS_RESPONSIBILITIES,
            AnalysisSection.UNNECESSARY_SECTIONS
        ]
        
        all_analyses = {}
        for section in sections:
            analysis = await hybrid_checker.analyze_section(section, resume_data, resume_text)
            all_analyses[section.value] = analysis
        
        # Calculate overall score (100-point system)
        total_score = sum(analysis['deterministic_score']['score'] for analysis in all_analyses.values())
        overall_score_100 = (total_score / len(sections)) * 10  # Convert to 100-point scale
        
        return {
            "filename": file.filename,
            "overall_score": {
                "score": overall_score_100,
                "percentage": overall_score_100,
                "max_score": 100.0,
                "grade": get_grade(overall_score_100)
            },
            "section_analyses": all_analyses,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Comprehensive analysis failed: {str(e)}")

# ============================================================================
# ORIGINAL ATS CHECKER ENDPOINTS (Legacy support)
# ============================================================================

@app.post("/original/analyze-resume")
async def original_analyze_resume(file: UploadFile = File(...)):
    """Original ATS resume analysis endpoint"""
    try:
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
        # Parse PDF
        resume_text = await hybrid_checker.pdf_parser.parse_pdf(file)
        if not resume_text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from PDF")
        
        # Parse to JSON
        resume_data = hybrid_checker.openai_service.parse_resume_to_json(resume_text)
        
        return {
            "filename": file.filename,
            "analysis_type": "original_ats",
            "resume_data": resume_data,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Original analysis failed: {str(e)}")

@app.post("/original/optimize-resume")
async def original_optimize_resume(file: UploadFile = File(...)):
    """Original ATS resume optimization endpoint"""
    try:
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
        # Parse PDF
        resume_text = await hybrid_checker.pdf_parser.parse_pdf(file)
        if not resume_text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from PDF")
        
        # Parse to JSON
        resume_data = hybrid_checker.openai_service.parse_resume_to_json(resume_text)
        
        return {
            "filename": file.filename,
            "optimization_type": "original_ats",
            "optimized_data": resume_data,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Original optimization failed: {str(e)}")

# ============================================================================
# UTILITY ENDPOINTS
# ============================================================================

@app.get("/scoring-info")
async def get_scoring_info():
    """Get information about the scoring system"""
    return {
        "overall_scoring": {
            "scale": "0-100",
            "excellent": "90-100 (A+)",
            "very_good": "80-89 (A)",
            "good": "70-79 (B+)",
            "above_average": "60-69 (B)",
            "average": "50-59 (C)",
            "below_average": "40-49 (D)",
            "poor": "0-39 (F)"
        },
        "section_scoring": {
            "scale": "0-10",
            "excellent": "9-10",
            "good": "7-8",
            "average": "5-6",
            "below_average": "3-4",
            "poor": "0-2"
        },
        "scoring_factors": {
            "strong_verbs": "+0.5 per strong verb",
            "quantifiable_achievements": "+1.0 per metric",
            "buzzwords": "-0.5 per buzzword",
            "ats_keywords": "+1.5 per keyword match",
            "contact_completeness": "+2.0 per required field",
            "grammar_errors": "-0.1 per error"
        },
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "deterministic_engine": "operational",
            "gpt_service": "operational",
            "pdf_parser": "operational"
        },
        "version": "2.0.0"
    }

@app.get("/api-info")
async def get_api_info():
    """Get comprehensive API information"""
    return {
        "application": "AI JobPylot - Unified ATS Checker",
        "version": "2.0.0",
        "endpoints": {
            "hybrid": {
                "description": "Hybrid ATS checker with 100-point scoring",
                "endpoints": [
                    "/hybrid/analyze-all-sections",
                    "/hybrid/analyze-summary",
                    "/hybrid/analyze-dates",
                    "/hybrid/analyze-weak-verbs",
                    "/hybrid/analyze-quantity-impact",
                    "/hybrid/analyze-teamwork",
                    "/hybrid/analyze-buzzwords",
                    "/hybrid/analyze-contact-details",
                    "/hybrid/analyze-line-by-line",
                    "/hybrid/magic-write-section",
                    "/hybrid/analyze-grammar-spelling",
                    "/hybrid/analyze-formatting-layout",
                    "/hybrid/analyze-ats-keywords",
                    "/hybrid/analyze-skills-relevance",
                    "/hybrid/analyze-achievements-vs-responsibilities"
                ]
            },
            "original": {
                "description": "Original ATS checker endpoints",
                "endpoints": [
                    "/original/analyze-resume",
                    "/original/optimize-resume"
                ]
            },
            "utility": {
                "description": "Utility endpoints",
                "endpoints": [
                    "/health",
                    "/scoring-info",
                    "/api-info"
                ]
            }
        },
        "scoring_system": {
            "hybrid": "100-point overall scoring with letter grades",
            "sections": "0-10 point scoring for individual sections",
            "deterministic": "Rule-based, reproducible results",
            "gpt_integration": "GPT-3.5 turbo for content generation"
        },
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001) 
