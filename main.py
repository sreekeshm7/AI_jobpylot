from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Dict, Any

from services.pdf_parser import PDFParser
from services.openai_service import OpenAIService
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

app = FastAPI(title="Resume Analyzer API", version="1.0.0")

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
    # Ensure extracted_summary is always the literal input, not paraphrased
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

@app.post("/evaluate-quantifiable-impact", response_model=QuantifiableImpactEvaluation)
async def evaluate_quantifiable_impact(resume_data: Dict[str, Any]):
    try:
        evaluation = openai_service.evaluate_section(resume_data, "quantifiable_impact")
        return QuantifiableImpactEvaluation(**evaluation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluating section: {str(e)}")

@app.post("/evaluate-date-format", response_model=DateFormatEvaluation)
async def evaluate_date_format(resume_data: Dict[str, Any]):
    try:
        evaluation = openai_service.evaluate_section(resume_data, "date_format")
        return DateFormatEvaluation(**evaluation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluating section: {str(e)}")

@app.post("/evaluate-weak-verbs", response_model=WeakVerbsEvaluation)
async def evaluate_weak_verbs(resume_data: Dict[str, Any]):
    try:
        evaluation = openai_service.evaluate_section(resume_data, "weak_verbs")
        return WeakVerbsEvaluation(**evaluation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluating section: {str(e)}")

@app.post("/evaluate-teamwork", response_model=TeamworkCollaborationEvaluation)
async def evaluate_teamwork(resume_data: Dict[str, Any]):
    try:
        evaluation = openai_service.evaluate_section(resume_data, "teamwork_collaboration")
        return TeamworkCollaborationEvaluation(**evaluation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluating section: {str(e)}")

@app.post("/evaluate-buzzwords", response_model=BuzzwordsEvaluation)
async def evaluate_buzzwords(resume_data: Dict[str, Any]):
    try:
        evaluation = openai_service.evaluate_section(resume_data, "buzzwords_cliches")
        return BuzzwordsEvaluation(**evaluation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluating section: {str(e)}")

@app.post("/evaluate-unnecessary-sections", response_model=UnnecessarySectionsEvaluation)
async def evaluate_unnecessary_sections(resume_data: Dict[str, Any]):
    try:
        evaluation = openai_service.evaluate_section(resume_data, "unnecessary_sections")
        return UnnecessarySectionsEvaluation(**evaluation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluating section: {str(e)}")

@app.post("/evaluate-contact-details", response_model=ContactDetailsEvaluation)
async def evaluate_contact_details(resume_data: Dict[str, Any]):
    try:
        evaluation = openai_service.evaluate_section(resume_data, "contact_details")
        return ContactDetailsEvaluation(**evaluation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluating section: {str(e)}")

@app.post("/evaluate-grammar-spelling", response_model=GrammarSpellingEvaluation)
async def evaluate_grammar_spelling(resume_data: Dict[str, Any]):
    try:
        evaluation = openai_service.evaluate_section(resume_data, "grammar_spelling")
        return GrammarSpellingEvaluation(**evaluation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluating section: {str(e)}")

@app.post("/evaluate-formatting", response_model=FormattingLayoutEvaluation)
async def evaluate_formatting(resume_data: Dict[str, Any]):
    try:
        evaluation = openai_service.evaluate_section(resume_data, "formatting_layout")
        return FormattingLayoutEvaluation(**evaluation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluating section: {str(e)}")

@app.post("/evaluate-ats-keywords", response_model=ATSKeywordsEvaluation)
async def evaluate_ats_keywords(resume_data: Dict[str, Any]):
    try:
        evaluation = openai_service.evaluate_section(resume_data, "ats_keywords")
        return ATSKeywordsEvaluation(**evaluation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluating section: {str(e)}")

@app.post("/evaluate-skills-relevance", response_model=SkillsRelevanceEvaluation)
async def evaluate_skills_relevance(resume_data: Dict[str, Any]):
    try:
        evaluation = openai_service.evaluate_section(resume_data, "skills_relevance")
        return SkillsRelevanceEvaluation(**evaluation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluating section: {str(e)}")

@app.post("/evaluate-achievements-vs-responsibilities", response_model=AchievementsVsResponsibilitiesEvaluation)
async def evaluate_achievements_vs_responsibilities(resume_data: Dict[str, Any]):
    try:
        evaluation = openai_service.evaluate_section(resume_data, "achievements_vs_responsibilities")
        return AchievementsVsResponsibilitiesEvaluation(**evaluation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluating section: {str(e)}")

@app.post("/evaluate-education-clarity", response_model=EducationClarityEvaluation)
async def evaluate_education_clarity(resume_data: Dict[str, Any]):
    try:
        evaluation = openai_service.evaluate_section(resume_data, "education_clarity")
        return EducationClarityEvaluation(**evaluation)
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

@app.get("/")
async def root():
    return {"message": "Resume Analyzer API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
