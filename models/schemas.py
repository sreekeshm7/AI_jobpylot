from pydantic import BaseModel
from typing import List, Dict, Any

class ProjectModel(BaseModel):
    Title: str = ""
    Description: str = ""
    LiveLink: str = ""
    GitHubLink: str = ""
    StartDate: str = ""
    EndDate: str = ""
    Role: str = ""
    description: str = ""
    bullets: List[str] = []
    TechStack: List[str] = []

class LinksModel(BaseModel):
    LinkedIn: str = ""
    GitHub: str = ""
    Portfolio: str = ""
    OtherLinks: List[str] = []
    Projects: List[ProjectModel] = []

class SkillsModel(BaseModel):
    Tools: List[str] = []
    soft_skills: List[str] = []
    TechStack: List[str] = []
    Languages: List[str] = []
    Others: List[str] = []

class WorkExperienceModel(BaseModel):
    JobTitle: str = ""
    Company: str = ""
    Duration: str = ""
    Location: str = ""
    Responsibilities: List[str] = []
    TechStack: List[str] = []

class EducationModel(BaseModel):
    Degree: str = ""
    Mark: str = ""
    Institution: str = ""
    Location: str = ""
    StartYear: str = ""
    EndYear: str = ""

class ResumeModel(BaseModel):
    Name: str = ""
    Email: str = ""
    Phone: str = ""
    Links: LinksModel = LinksModel()
    Summary: str = ""
    Skills: SkillsModel = SkillsModel()
    WorkExperience: List[WorkExperienceModel] = []
    Education: List[EducationModel] = []
    Certifications: List[str] = []
    Languages: List[str] = []
    Achievements: List[str] = []
    Awards: List[str] = []
    VolunteerExperience: List[str] = []
    Hobbies: List[str] = []
    Interests: List[str] = []
    References: List[str] = []

class ResumeResponse(BaseModel):
    resume: ResumeModel
    summary: str

# Summary evaluation
class SummaryEvaluation(BaseModel):
    extracted_summary: str = ""
    ats_score: int = 0
    weak_sentences: List[str] = []
    strong_sentences: List[str] = []
    score_feedback: List[str] = []
    improved_summaries: List[str] = []

# Upgraded section models (improved_content is now list of dicts)
class QuantifiableImpactEvaluation(BaseModel):
    section_name: str = "quantifiable_impact"
    ats_score: int = 0
    feedback: List[str] = []
    weak_sentences: List[str] = []
    strong_sentences: List[str] = []
    improved_content: List[Dict[str, Any]] = []
    examples: List[str] = []

class DateFormatEvaluation(BaseModel):
    section_name: str = "date_format"
    ats_score: int = 0
    feedback: List[str] = []
    date_issues: List[str] = []
    suggested_format: str = ""
    formatting_issues: List[str] = []
    corrections: List[str] = []

class WeakVerbsEvaluation(BaseModel):
    section_name: str = "weak_verbs"
    ats_score: int = 0
    feedback: List[str] = []
    weak_sentences: List[str] = []
    strong_sentences: List[str] = []
    improved_content: List[Dict[str, Any]] = []
    examples: List[str] = []

class TeamworkCollaborationEvaluation(BaseModel):
    section_name: str = "teamwork_collaboration"
    ats_score: int = 0
    feedback: List[str] = []
    weak_sentences: List[str] = []
    strong_sentences: List[str] = []
    improved_content: List[str] = []
    examples: List[str] = []

class BuzzwordsEvaluation(BaseModel):
    section_name: str = "buzzwords_cliches"
    ats_score: int = 0
    feedback: List[str] = []
    issues_found: List[str] = []
    corrections: List[str] = []
    improved_content: List[str] = []
    examples: List[str] = []

class UnnecessarySectionsEvaluation(BaseModel):
    section_name: str = "unnecessary_sections"
    ats_score: int = 0
    feedback: List[str] = []
    issues_found: List[str] = []
    missing_information: List[str] = []
    recommendations: List[str] = []

class ContactDetailsEvaluation(BaseModel):
    section_name: str = "contact_details"
    ats_score: int = 0
    feedback: List[str] = []
    contact_completeness: Dict[str, bool] = {}
    issues_found: List[str] = []
    recommendations: List[str] = []

class GrammarSpellingEvaluation(BaseModel):
    section_name: str = "grammar_spelling"
    ats_score: int = 0
    feedback: List[str] = []
    grammar_errors: List[str] = []
    spelling_errors: List[str] = []
    corrections: List[str] = []
    improved_content: List[str] = []

class FormattingLayoutEvaluation(BaseModel):
    section_name: str = "formatting_layout"
    ats_score: int = 0
    feedback: List[str] = []
    formatting_issues: List[str] = []
    recommendations: List[str] = []
    examples: List[str] = []

class ATSKeywordsEvaluation(BaseModel):
    section_name: str = "ats_keywords"
    ats_score: int = 0
    feedback: List[str] = []
    missing_keywords: List[str] = []
    relevant_keywords: List[str] = []
    recommendations: List[str] = []
    improved_content: List[str] = []

class SkillsRelevanceEvaluation(BaseModel):
    section_name: str = "skills_relevance"
    ats_score: int = 0
    feedback: List[str] = []
    issues_found: List[str] = []
    missing_information: List[str] = []
    recommendations: List[str] = []
    improved_content: List[str] = []

class AchievementsVsResponsibilitiesEvaluation(BaseModel):
    section_name: str = "achievements_vs_responsibilities"
    ats_score: int = 0
    feedback: List[str] = []
    weak_sentences: List[str] = []
    strong_sentences: List[str] = []
    improved_content: List[Dict[str, Any]] = []
    examples: List[str] = []

class EducationClarityEvaluation(BaseModel):
    section_name: str = "education_clarity"
    ats_score: int = 0
    feedback: List[str] = []
    issues_found: List[str] = []
    missing_information: List[str] = []
    recommendations: List[str] = []
    corrections: List[str] = []
class RelevantSkillSuggestionRequest(BaseModel):
    resume_data: Dict[str, Any]
    target_role: str = ""  # Optional: User may provide a target job/role

class RelevantSkillSuggestionResponse(BaseModel):
    suggested_skills: List[str]
    rationale: List[str]  # Optional explanations

class SectionRewriteRequest(BaseModel):
    section: str  # e.g., "WorkExperience", "Education", "Projects"
    description: str  # The original description to be rewritten
    resume_data: Dict[str, Any] = {}  # Optionally provide context, e.g., full resume

class SectionRewriteResponse(BaseModel):
    original: str
    rewritten: str
    rationale: str
class SummaryImprovement(BaseModel):
    improved: str
    original_score: int
    improved_score: int
    explanation: str

class SummaryEvaluation(BaseModel):
    extracted_summary: str
    ats_score: int
    weak_sentences: List[str]
    strong_sentences: List[str]
    score_feedback: List[str]
    improved_summaries: List[SummaryImprovement]

