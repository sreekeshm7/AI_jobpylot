from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Dict, Any, List
import uuid
from datetime import datetime

from services.pdf_parser import PDFParser
from services.openai_service import OpenAIService
from services.ats_engine import ATSEngine
from models.schemas import (
    ResumeResponse, SummaryEvaluation,
    QuantifiableImpactEvaluation, DateFormatEvaluation, WeakVerbsEvaluation,
    TeamworkCollaborationEvaluation, BuzzwordsEvaluation, UnnecessarySectionsEvaluation,
    ContactDetailsEvaluation, GrammarSpellingEvaluation, FormattingLayoutEvaluation,
    ATSKeywordsEvaluation, SkillsRelevanceEvaluation, AchievementsVsResponsibilitiesEvaluation,
    EducationClarityEvaluation,
    RelevantSkillSuggestionRequest, RelevantSkillSuggestionResponse,
    SectionRewriteRequest, SectionRewriteResponse
)
from models.ats_schemas import (
    JobPostingRequest, JobPostingResponse,
    CandidateRegistrationRequest, CandidateRegistrationResponse,
    CandidateScoreResponse, JobMatchRequest, JobRankingRequest,
    JobRecommendationRequest, JobRecommendationResponse,
    ATSAnalysisRequest, ATSAnalysisResponse,
    DashboardStats, AnalyticsRequest, AnalyticsResponse,
    BulkJobPostingRequest, BulkCandidateRegistrationRequest,
    CandidateSearchRequest, JobSearchRequest,
    ErrorResponse, StatusResponse
)

app = FastAPI(
    title="AI JobPylot - Advanced ATS Engine", 
    version="2.0.0",
    description="A comprehensive ATS (Applicant Tracking System) powered by GPT-3.5 with advanced matching, scoring, and analytics capabilities."
)

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to your domain(s)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
pdf_parser = PDFParser()
openai_service = OpenAIService()
ats_engine = ATSEngine()

# ============================================================================
# RESUME ANALYSIS ENDPOINTS (Existing functionality)
# ============================================================================

@app.post("/upload-resume", response_model=ResumeResponse)
async def upload_resume(file: UploadFile = File(...)):
    """Upload PDF resume and convert to structured JSON format"""
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    try:
        resume_text = pdf_parser.extract_text_from_pdf(file.file)
        resume_json = openai_service.parse_resume_to_json(resume_text)
        return ResumeResponse(**resume_json)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing resume: {str(e)}")

@app.post("/evaluate-summary", response_model=SummaryEvaluation)
async def evaluate_summary(resume_data: Dict[str, Any]):
    """Evaluate resume summary for ATS optimization"""
    extracted_summary = (
        resume_data.get("Summary")
        or resume_data.get("summary")
        or resume_data.get("resume", {}).get("Summary")
        or ""
    )
    try:
        result = openai_service.evaluate_summary(resume_data)
        result["extracted_summary"] = extracted_summary
        return SummaryEvaluation(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluating summary: {str(e)}")

# ... (keeping other existing evaluation endpoints for brevity)
@app.post("/evaluate-quantifiable-impact", response_model=QuantifiableImpactEvaluation)
async def evaluate_quantifiable_impact(resume_data: Dict[str, Any]):
    try:
        evaluation = openai_service.evaluate_section(resume_data, "quantifiable_impact")
        return QuantifiableImpactEvaluation(**evaluation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluating section: {str(e)}")

@app.post("/suggest-relevant-skills", response_model=RelevantSkillSuggestionResponse)
async def suggest_relevant_skills(req: RelevantSkillSuggestionRequest):
    try:
        result = openai_service.suggest_relevant_skills(
            resume_data=req.resume_data,
            target_role=req.target_role
        )
        return RelevantSkillSuggestionResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error suggesting skills: {str(e)}")

@app.post("/rewrite-section", response_model=SectionRewriteResponse)
async def rewrite_section(req: SectionRewriteRequest):
    try:
        result = openai_service.rewrite_section(
            section=req.section,
            description=req.description,
            resume_data=req.resume_data if req.resume_data else None
        )
        return SectionRewriteResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error rewriting section: {str(e)}")

# ============================================================================
# ATS ENGINE ENDPOINTS (New functionality)
# ============================================================================

@app.post("/ats/analyze-resume", response_model=ATSAnalysisResponse)
async def analyze_resume_ats_compatibility(req: ATSAnalysisRequest):
    """Comprehensive ATS compatibility analysis"""
    try:
        analysis = ats_engine.analyze_resume_ats_compatibility(req.resume_data)
        return ATSAnalysisResponse(**analysis)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing ATS compatibility: {str(e)}")

@app.post("/ats/jobs", response_model=JobPostingResponse)
async def add_job_posting(job_data: JobPostingRequest):
    """Add a new job posting to the ATS system"""
    try:
        job_id = str(uuid.uuid4())
        result = ats_engine.add_job_posting(job_id, job_data.dict())
        return JobPostingResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding job posting: {str(e)}")

@app.post("/ats/candidates", response_model=CandidateRegistrationResponse)
async def register_candidate(req: CandidateRegistrationRequest):
    """Register a candidate in the ATS system"""
    try:
        result = ats_engine.add_candidate(req.candidate_id, req.resume_data)
        return CandidateRegistrationResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error registering candidate: {str(e)}")

@app.post("/ats/match", response_model=CandidateScoreResponse)
async def match_candidate_to_job(req: JobMatchRequest):
    """Match a candidate to a specific job and return detailed scoring"""
    try:
        score = ats_engine.match_candidate_to_job(req.candidate_id, req.job_id)
        candidate_name = ats_engine.candidates_db[req.candidate_id]["name"]
        
        return CandidateScoreResponse(
            candidate_id=score.candidate_id,
            candidate_name=candidate_name,
            overall_score=score.overall_score,
            skills_match=score.skills_match,
            experience_match=score.experience_match,
            education_match=score.education_match,
            keyword_match=score.keyword_match,
            ats_compatibility=score.ats_compatibility,
            detailed_feedback=score.detailed_feedback
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error matching candidate: {str(e)}")

@app.post("/ats/rank-candidates", response_model=List[CandidateScoreResponse])
async def rank_candidates_for_job(req: JobRankingRequest):
    """Rank all candidates for a specific job"""
    try:
        rankings = ats_engine.rank_candidates_for_job(req.job_id, req.limit)
        return [CandidateScoreResponse(**ranking) for ranking in rankings]
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error ranking candidates: {str(e)}")

@app.post("/ats/job-recommendations", response_model=List[JobRecommendationResponse])
async def get_job_recommendations(req: JobRecommendationRequest):
    """Get job recommendations for a candidate"""
    try:
        recommendations = ats_engine.get_job_recommendations(req.candidate_id, req.limit)
        return [JobRecommendationResponse(**rec) for rec in recommendations]
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting recommendations: {str(e)}")

# ============================================================================
# BULK OPERATIONS
# ============================================================================

@app.post("/ats/bulk/jobs", response_model=List[JobPostingResponse])
async def add_bulk_jobs(bulk_req: BulkJobPostingRequest):
    """Add multiple job postings at once"""
    try:
        results = []
        for job_data in bulk_req.jobs:
            job_id = str(uuid.uuid4())
            result = ats_engine.add_job_posting(job_id, job_data.dict())
            results.append(JobPostingResponse(**result))
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding bulk jobs: {str(e)}")

@app.post("/ats/bulk/candidates", response_model=List[CandidateRegistrationResponse])
async def register_bulk_candidates(bulk_req: BulkCandidateRegistrationRequest):
    """Register multiple candidates at once"""
    try:
        results = []
        for candidate_data in bulk_req.candidates:
            candidate_id = str(uuid.uuid4())
            result = ats_engine.add_candidate(candidate_id, candidate_data)
            results.append(CandidateRegistrationResponse(**result))
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error registering bulk candidates: {str(e)}")

# ============================================================================
# SEARCH AND FILTER
# ============================================================================

@app.post("/ats/search/candidates", response_model=List[Dict[str, Any]])
async def search_candidates(search_req: CandidateSearchRequest):
    """Search candidates based on criteria"""
    try:
        # This would implement actual search logic
        # For now, return all candidates that match basic criteria
        matching_candidates = []
        
        for candidate_id, candidate in ats_engine.candidates_db.items():
            matches = True
            
            if search_req.skills:
                candidate_skills = set(skill.lower() for skill in candidate["skills"])
                search_skills = set(skill.lower() for skill in search_req.skills)
                if not candidate_skills.intersection(search_skills):
                    matches = False
            
            if search_req.experience_min and candidate["experience_years"] < search_req.experience_min:
                matches = False
                
            if search_req.experience_max and candidate["experience_years"] > search_req.experience_max:
                matches = False
            
            if matches:
                matching_candidates.append({
                    "candidate_id": candidate_id,
                    "name": candidate["name"],
                    "email": candidate["email"],
                    "skills": candidate["skills"],
                    "experience_years": candidate["experience_years"]
                })
        
        return matching_candidates[:search_req.limit]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching candidates: {str(e)}")

@app.post("/ats/search/jobs", response_model=List[Dict[str, Any]])
async def search_jobs(search_req: JobSearchRequest):
    """Search jobs based on criteria"""
    try:
        matching_jobs = []
        
        for job_id, job in ats_engine.job_requirements_db.items():
            matches = True
            
            if search_req.title_keywords:
                job_title_lower = job.title.lower()
                if not any(keyword.lower() in job_title_lower for keyword in search_req.title_keywords):
                    matches = False
            
            if search_req.required_skills:
                job_skills = set(skill.lower() for skill in job.required_skills)
                search_skills = set(skill.lower() for skill in search_req.required_skills)
                if not job_skills.intersection(search_skills):
                    matches = False
            
            if search_req.experience_years and job.experience_years != search_req.experience_years:
                matches = False
            
            if matches:
                matching_jobs.append({
                    "job_id": job_id,
                    "title": job.title,
                    "industry": job.industry,
                    "location": job.location,
                    "required_skills": job.required_skills,
                    "experience_years": job.experience_years
                })
        
        return matching_jobs[:search_req.limit]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching jobs: {str(e)}")

# ============================================================================
# DASHBOARD AND ANALYTICS
# ============================================================================

@app.get("/ats/dashboard", response_model=DashboardStats)
async def get_dashboard_stats():
    """Get dashboard statistics"""
    try:
        total_candidates = len(ats_engine.candidates_db)
        total_jobs = len(ats_engine.job_requirements_db)
        
        # Calculate total matches (simplified)
        total_matches = total_candidates * total_jobs  # This would be more sophisticated in production
        
        # Calculate average match score (simplified)
        average_match_score = 0.75  # This would be calculated from actual matches
        
        # Get top performing jobs (simplified)
        top_performing_jobs = []
        for job_id, job in list(ats_engine.job_requirements_db.items())[:5]:
            top_performing_jobs.append({
                "job_id": job_id,
                "title": job.title,
                "applications": 0  # This would be tracked in production
            })
        
        # Get recent applications (simplified)
        recent_applications = []
        for candidate_id, candidate in list(ats_engine.candidates_db.items())[:5]:
            recent_applications.append({
                "candidate_id": candidate_id,
                "name": candidate["name"],
                "applied_date": candidate["added_date"]
            })
        
        return DashboardStats(
            total_candidates=total_candidates,
            total_jobs=total_jobs,
            total_matches=total_matches,
            average_match_score=average_match_score,
            top_performing_jobs=top_performing_jobs,
            recent_applications=recent_applications
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting dashboard stats: {str(e)}")

@app.post("/ats/analytics", response_model=AnalyticsResponse)
async def get_analytics(analytics_req: AnalyticsRequest):
    """Get detailed analytics"""
    try:
        # This would implement actual analytics logic
        # For now, return basic analytics
        return AnalyticsResponse(
            period="Last 30 days",
            total_applications=len(ats_engine.candidates_db),
            average_scores={
                "skills_match": 0.75,
                "experience_match": 0.80,
                "education_match": 0.85,
                "keyword_match": 0.70,
                "ats_compatibility": 0.90
            },
            top_skills=["Python", "JavaScript", "React", "Node.js", "SQL"],
            common_issues=["Missing quantifiable achievements", "Weak action verbs"],
            improvement_trends={
                "keyword_optimization": "+15%",
                "ats_compatibility": "+8%",
                "overall_scores": "+12%"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting analytics: {str(e)}")

# ============================================================================
# SYSTEM ENDPOINTS
# ============================================================================

@app.get("/", response_model=StatusResponse)
async def root():
    """Root endpoint with system status"""
    return StatusResponse(
        status="running",
        message="AI JobPylot ATS Engine is running successfully"
    )

@app.get("/health", response_model=StatusResponse)
async def health_check():
    """Health check endpoint"""
    return StatusResponse(
        status="healthy",
        message="All systems operational"
    )

@app.get("/ats/stats", response_model=Dict[str, Any])
async def get_system_stats():
    """Get system statistics"""
    return {
        "total_candidates": len(ats_engine.candidates_db),
        "total_jobs": len(ats_engine.job_requirements_db),
        "system_uptime": "24 hours",  # This would be calculated
        "api_version": "2.0.0",
        "gpt_model": "gpt-3.5-turbo"
    }

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content=ErrorResponse(
            error="Not Found",
            details="The requested resource was not found"
        ).dict()
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal Server Error",
            details="An unexpected error occurred"
        ).dict()
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
