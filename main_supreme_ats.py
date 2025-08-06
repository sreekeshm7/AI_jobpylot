from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Dict, Any, List
import uuid
from datetime import datetime

from services.pdf_parser import PDFParser
from services.openai_service import OpenAIService
from services.supreme_ats_engine import SupremeATSEngine
from models.schemas import (
    ResumeResponse, SummaryEvaluation,
    QuantifiableImpactEvaluation, DateFormatEvaluation, WeakVerbsEvaluation,
    TeamworkCollaborationEvaluation, BuzzwordsEvaluation, UnnecessarySectionsEvaluation,
    ContactDetailsEvaluation, GrammarSpellingEvaluation, FormattingLayoutEvaluation,
    ATSKeywordsEvaluation, SkillsRelevanceEvaluation, AchievementsVsResponsibilitiesEvaluation,
    EducationClarityEvaluation
)

app = FastAPI(
    title="AI JobPylot - Supreme ATS Engine",
    description="The most advanced ATS-powered resume analysis and optimization system",
    version="3.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
pdf_parser = PDFParser()
openai_service = OpenAIService()
supreme_ats_engine = SupremeATSEngine()

@app.get("/")
async def root():
    return {
        "message": "AI JobPylot - Supreme ATS Engine",
        "version": "3.0.0",
        "status": "running",
        "features": [
            "Supreme Resume Analysis",
            "Advanced AI-Powered Scoring",
            "Multi-dimensional Evaluation",
            "Intelligent Optimization",
            "Market Analysis",
            "Improvement Predictions"
        ],
        "power_level": "SUPREME"
    }

@app.post("/analyze-resume-supreme", response_model=Dict[str, Any])
async def analyze_resume_supreme(file: UploadFile = File(...)):
    """
    Supreme resume analysis with advanced AI capabilities and optimization
    """
    try:
        # Validate file
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
        # Parse PDF
        resume_text = await pdf_parser.parse_pdf(file)
        if not resume_text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from PDF")
        
        # Parse to JSON
        resume_data = openai_service.parse_resume_to_json(resume_text)
        
        # Supreme ATS analysis
        supreme_analysis = supreme_ats_engine.analyze_resume_supreme(resume_data)
        
        # Generate comprehensive response
        response = {
            "resume_id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "filename": file.filename,
            "parsed_data": resume_data,
            "supreme_analysis": supreme_analysis,
            "summary": {
                "supreme_score": supreme_analysis["supreme_ats_score"],
                "section_breakdown": supreme_analysis["section_scores"],
                "market_competitiveness": supreme_analysis["market_analysis"]["market_competitiveness"],
                "keyword_match": supreme_analysis["market_analysis"]["keyword_match_percentage"]
            },
            "detailed_analysis": supreme_analysis["detailed_analysis"],
            "advanced_insights": supreme_analysis["advanced_insights"],
            "optimization_recommendations": supreme_analysis["optimization_recommendations"],
            "improvement_predictions": supreme_analysis["improvement_predictions"],
            "market_analysis": supreme_analysis["market_analysis"]
        }
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Supreme analysis failed: {str(e)}")

@app.post("/optimize-resume-supreme", response_model=Dict[str, Any])
async def optimize_resume_supreme(file: UploadFile = File(...)):
    """
    Generate supreme optimized version of resume with advanced improvements
    """
    try:
        # Validate file
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
        # Parse PDF
        resume_text = await pdf_parser.parse_pdf(file)
        if not resume_text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from PDF")
        
        # Parse to JSON
        resume_data = openai_service.parse_resume_to_json(resume_text)
        
        # Get supreme analysis
        supreme_analysis = supreme_ats_engine.analyze_resume_supreme(resume_data)
        
        # Generate optimized versions
        summary_analysis = supreme_analysis["detailed_analysis"]["summary"]
        optimized_summaries = summary_analysis.get("improved_versions", [])
        
        # Generate skill suggestions
        skill_suggestions = openai_service.suggest_relevant_skills(resume_data)
        
        return {
            "original_analysis": supreme_analysis,
            "optimized_summaries": optimized_summaries,
            "skill_suggestions": skill_suggestions,
            "optimization_score": {
                "before": supreme_analysis["supreme_ats_score"],
                "potential_after": min(10, supreme_analysis["supreme_ats_score"] + 3),
                "improvement_potential": supreme_analysis["improvement_predictions"]
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Supreme optimization failed: {str(e)}")

@app.post("/compare-resumes-supreme", response_model=Dict[str, Any])
async def compare_resumes_supreme(
    file1: UploadFile = File(...),
    file2: UploadFile = File(...)
):
    """
    Compare two resumes with supreme analysis and detailed comparison
    """
    try:
        # Validate files
        for file in [file1, file2]:
            if not file.filename.lower().endswith('.pdf'):
                raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
        # Parse both resumes
        resume1_text = await pdf_parser.parse_pdf(file1)
        resume2_text = await pdf_parser.parse_pdf(file2)
        
        resume1_data = openai_service.parse_resume_to_json(resume1_text)
        resume2_data = openai_service.parse_resume_to_json(resume2_text)
        
        # Analyze both resumes with supreme engine
        analysis1 = supreme_ats_engine.analyze_resume_supreme(resume1_data)
        analysis2 = supreme_ats_engine.analyze_resume_supreme(resume2_data)
        
        # Generate supreme comparison
        comparison = {
            "resume1": {
                "filename": file1.filename,
                "supreme_score": analysis1["supreme_ats_score"],
                "section_scores": analysis1["section_scores"],
                "market_competitiveness": analysis1["market_analysis"]["market_competitiveness"]
            },
            "resume2": {
                "filename": file2.filename,
                "supreme_score": analysis2["supreme_ats_score"],
                "section_scores": analysis2["section_scores"],
                "market_competitiveness": analysis2["market_analysis"]["market_competitiveness"]
            },
            "supreme_comparison": {
                "score_difference": analysis1["supreme_ats_score"] - analysis2["supreme_ats_score"],
                "better_resume": file1.filename if analysis1["supreme_ats_score"] > analysis2["supreme_ats_score"] else file2.filename,
                "strengths_resume1": analysis1["detailed_analysis"]["summary"].get("strengths", []),
                "strengths_resume2": analysis2["detailed_analysis"]["summary"].get("strengths", []),
                "weaknesses_resume1": analysis1["detailed_analysis"]["summary"].get("weaknesses", []),
                "weaknesses_resume2": analysis2["detailed_analysis"]["summary"].get("weaknesses", []),
                "market_advantage": "resume1" if analysis1["market_analysis"]["keyword_match_percentage"] > analysis2["market_analysis"]["keyword_match_percentage"] else "resume2"
            },
            "timestamp": datetime.now().isoformat()
        }
        
        return comparison
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Supreme comparison failed: {str(e)}")

@app.get("/supreme-benchmarks", response_model=Dict[str, Any])
async def get_supreme_benchmarks():
    """
    Get supreme ATS scoring benchmarks and industry standards
    """
    return {
        "supreme_scoring_standards": {
            "supreme": {"range": "9.0-10.0", "description": "Supreme optimization - executive-level positioning"},
            "excellent": {"range": "8.0-8.9", "description": "Excellent optimization - top-tier performance"},
            "good": {"range": "7.0-7.9", "description": "Good optimization - competitive positioning"},
            "average": {"range": "5.0-6.9", "description": "Average - needs optimization"},
            "poor": {"range": "0.0-4.9", "description": "Poor - requires significant improvement"}
        },
        "supreme_section_weights": {
            "summary": "30% - Most critical for supreme positioning",
            "experience": "25% - Essential for role matching",
            "skills": "20% - Critical for keyword optimization",
            "education": "15% - Important for qualification",
            "keywords": "7% - Affects search ranking",
            "formatting": "3% - Ensures ATS compatibility"
        },
        "supreme_optimization_tips": [
            "Transform summary into compelling executive statement with quantifiable achievements",
            "Enhance experience descriptions with leadership impact and strategic outcomes",
            "Optimize skills section with industry-leading technologies and emerging trends",
            "Use supreme action verbs and quantifiable metrics throughout",
            "Ensure perfect ATS compatibility with standard formatting",
            "Include industry-specific keywords naturally and strategically"
        ],
        "supreme_boost_factors": {
            "leadership_boost": "2.2x - For leadership indicators",
            "quantifiable_boost": "2.5x - For measurable achievements",
            "keyword_boost": "2.0x - For industry keywords",
            "action_verb_boost": "1.8x - For strong action verbs",
            "experience_boost": "1.9x - For relevant experience",
            "supreme_optimization_boost": "1.15x - Final supreme adjustment"
        }
    }

@app.get("/supreme-health")
async def supreme_health_check():
    """Supreme health check endpoint"""
    return {
        "status": "SUPREME",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "pdf_parser": "operational",
            "openai_service": "operational",
            "supreme_ats_engine": "SUPREME"
        },
        "power_level": "MAXIMUM",
        "optimization_capability": "UNLIMITED"
    }

@app.post("/analyze-resume-section-supreme", response_model=Dict[str, Any])
async def analyze_resume_section_supreme(
    file: UploadFile = File(...),
    section: str = "summary"
):
    """
    Analyze specific resume section with supreme precision
    """
    try:
        # Validate file
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
        # Parse PDF
        resume_text = await pdf_parser.parse_pdf(file)
        if not resume_text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from PDF")
        
        # Parse to JSON
        resume_data = openai_service.parse_resume_to_json(resume_text)
        
        # Analyze specific section with supreme precision
        if section == "summary":
            analysis = openai_service.evaluate_summary(resume_data)
        else:
            analysis = openai_service.evaluate_section(resume_data, section)
        
        return {
            "section": section,
            "supreme_analysis": analysis,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Supreme section analysis failed: {str(e)}")

@app.get("/supreme-performance")
async def get_supreme_performance():
    """
    Get supreme performance metrics and system status
    """
    return {
        "supreme_metrics": {
            "processing_speed": "SUPREME",
            "accuracy_level": "MAXIMUM",
            "optimization_power": "UNLIMITED",
            "ai_intelligence": "SUPREME"
        },
        "system_status": {
            "ats_engine": "SUPREME",
            "scoring_algorithm": "ADVANCED",
            "keyword_analysis": "COMPREHENSIVE",
            "optimization_capability": "MAXIMUM"
        },
        "power_level": "SUPREME",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 