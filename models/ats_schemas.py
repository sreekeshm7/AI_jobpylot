from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

# --- Job Posting Models ---

class JobPostingRequest(BaseModel):
    title: str = Field(..., description="Job title")
    required_skills: List[str] = Field(default=[], description="Required skills for the position")
    preferred_skills: List[str] = Field(default=[], description="Preferred skills for the position")
    experience_years: int = Field(default=0, description="Required years of experience")
    education_level: str = Field(default="", description="Required education level")
    industry: str = Field(default="", description="Industry or company")
    location: str = Field(default="", description="Job location")
    description: str = Field(default="", description="Job description")

class JobPostingResponse(BaseModel):
    job_id: str
    status: str
    requirements: Dict[str, Any]
    created_at: datetime = Field(default_factory=datetime.now)

# --- Candidate Management Models ---

class CandidateRegistrationRequest(BaseModel):
    candidate_id: str = Field(..., description="Unique candidate identifier")
    resume_data: Dict[str, Any] = Field(..., description="Parsed resume data")

class CandidateRegistrationResponse(BaseModel):
    candidate_id: str
    status: str
    candidate_info: Dict[str, Any]
    registered_at: datetime = Field(default_factory=datetime.now)

# --- Matching and Scoring Models ---

class CandidateScoreResponse(BaseModel):
    candidate_id: str
    candidate_name: str
    overall_score: float = Field(..., ge=0, le=1, description="Overall match score (0-1)")
    skills_match: float = Field(..., ge=0, le=1, description="Skills match score (0-1)")
    experience_match: float = Field(..., ge=0, le=1, description="Experience match score (0-1)")
    education_match: float = Field(..., ge=0, le=1, description="Education match score (0-1)")
    keyword_match: float = Field(..., ge=0, le=1, description="Keyword match score (0-1)")
    ats_compatibility: float = Field(..., ge=0, le=1, description="ATS compatibility score (0-1)")
    detailed_feedback: Dict[str, Any] = Field(..., description="Detailed feedback and recommendations")

class JobMatchRequest(BaseModel):
    candidate_id: str = Field(..., description="Candidate ID to match")
    job_id: str = Field(..., description="Job ID to match against")

class JobRankingRequest(BaseModel):
    job_id: str = Field(..., description="Job ID to rank candidates for")
    limit: int = Field(default=10, ge=1, le=100, description="Maximum number of candidates to return")

class JobRecommendationRequest(BaseModel):
    candidate_id: str = Field(..., description="Candidate ID to get recommendations for")
    limit: int = Field(default=5, ge=1, le=50, description="Maximum number of job recommendations")

class JobRecommendationResponse(BaseModel):
    job_id: str
    job_title: str
    company: str
    location: str
    overall_score: float
    skills_match: float
    experience_match: float
    education_match: float
    keyword_match: float
    ats_compatibility: float

# --- ATS Analysis Models ---

class ATSAnalysisRequest(BaseModel):
    resume_data: Dict[str, Any] = Field(..., description="Resume data to analyze")

class ATSAnalysisResponse(BaseModel):
    overall_ats_score: int = Field(..., ge=0, le=100, description="Overall ATS compatibility score")
    parsing_confidence: int = Field(..., ge=0, le=100, description="Confidence in parsing the resume")
    keyword_optimization: int = Field(..., ge=0, le=100, description="Keyword optimization score")
    format_compatibility: int = Field(..., ge=0, le=100, description="Format compatibility score")
    content_quality: int = Field(..., ge=0, le=100, description="Content quality score")
    detailed_analysis: Dict[str, Any] = Field(..., description="Detailed analysis results")
    keyword_analysis: Dict[str, Any] = Field(..., description="Keyword analysis results")
    format_analysis: Dict[str, Any] = Field(..., description="Format analysis results")
    content_analysis: Dict[str, Any] = Field(..., description="Content analysis results")

# --- Dashboard and Analytics Models ---

class DashboardStats(BaseModel):
    total_candidates: int
    total_jobs: int
    total_matches: int
    average_match_score: float
    top_performing_jobs: List[Dict[str, Any]]
    recent_applications: List[Dict[str, Any]]

class AnalyticsRequest(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    job_id: Optional[str] = None
    candidate_id: Optional[str] = None

class AnalyticsResponse(BaseModel):
    period: str
    total_applications: int
    average_scores: Dict[str, float]
    top_skills: List[str]
    common_issues: List[str]
    improvement_trends: Dict[str, Any]

# --- Bulk Operations Models ---

class BulkJobPostingRequest(BaseModel):
    jobs: List[JobPostingRequest] = Field(..., description="List of job postings to add")

class BulkCandidateRegistrationRequest(BaseModel):
    candidates: List[Dict[str, Any]] = Field(..., description="List of candidates with resume data")

class BulkMatchRequest(BaseModel):
    job_id: str = Field(..., description="Job ID to match all candidates against")
    candidate_ids: Optional[List[str]] = None  # If None, match all candidates

# --- Error and Status Models ---

class ErrorResponse(BaseModel):
    error: str
    details: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)

class StatusResponse(BaseModel):
    status: str
    message: str
    timestamp: datetime = Field(default_factory=datetime.now)

# --- Search and Filter Models ---

class CandidateSearchRequest(BaseModel):
    skills: Optional[List[str]] = None
    experience_min: Optional[int] = None
    experience_max: Optional[int] = None
    education_level: Optional[str] = None
    location: Optional[str] = None
    limit: int = Field(default=20, ge=1, le=100)

class JobSearchRequest(BaseModel):
    title_keywords: Optional[List[str]] = None
    required_skills: Optional[List[str]] = None
    experience_years: Optional[int] = None
    education_level: Optional[str] = None
    industry: Optional[str] = None
    location: Optional[str] = None
    limit: int = Field(default=20, ge=1, le=100)

# --- Notification Models ---

class NotificationRequest(BaseModel):
    candidate_id: str
    job_id: str
    notification_type: str = Field(..., description="Type of notification (match, application, etc.)")
    message: str = Field(..., description="Notification message")

class NotificationResponse(BaseModel):
    notification_id: str
    status: str
    sent_at: datetime = Field(default_factory=datetime.now) 