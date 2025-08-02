from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, Any
import json

from services.pdf_parser import PDFParser
from services.openai_service import OpenAIService
from models.schemas import (
    ResumeResponse, SummaryEvaluation,
    QuantifiableImpactEvaluation, DateFormatEvaluation, WeakVerbsEvaluation,
    TeamworkCollaborationEvaluation, BuzzwordsEvaluation, UnnecessarySectionsEvaluation,
    ContactDetailsEvaluation, GrammarSpellingEvaluation, FormattingLayoutEvaluation,
    ATSKeywordsEvaluation, SkillsRelevanceEvaluation, AchievementsVsResponsibilitiesEvaluation,
    EducationClarityEvaluation
    # Removed GenericSectionEvaluation from import
)

app = FastAPI(title="Resume Analyzer API", version="1.0.0")

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
    """Evaluate resume summary with ATS scoring"""
    try:
        evaluation = openai_service.evaluate_summary(resume_data)
        return SummaryEvaluation(**evaluation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluating summary: {str(e)}")

@app.post("/evaluate-quantifiable-impact", response_model=QuantifiableImpactEvaluation)
async def evaluate_quantifiable_impact(resume_data: Dict[str, Any]):
    """Evaluate quantifiable impact and metrics"""
    try:
        evaluation = openai_service.evaluate_section(resume_data, "quantifiable_impact")
        return QuantifiableImpactEvaluation(**evaluation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluating section: {str(e)}")

@app.post("/evaluate-date-format", response_model=DateFormatEvaluation)
async def evaluate_date_format(resume_data: Dict[str, Any]):
    """Evaluate date format and chronology"""
    try:
        evaluation = openai_service.evaluate_section(resume_data, "date_format")
        return DateFormatEvaluation(**evaluation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluating section: {str(e)}")

@app.post("/evaluate-weak-verbs", response_model=WeakVerbsEvaluation)
async def evaluate_weak_verbs(resume_data: Dict[str, Any]):
    """Evaluate and suggest improvements for weak verbs"""
    try:
        evaluation = openai_service.evaluate_section(resume_data, "weak_verbs")
        return WeakVerbsEvaluation(**evaluation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluating section: {str(e)}")

@app.post("/evaluate-teamwork", response_model=TeamworkCollaborationEvaluation)
async def evaluate_teamwork(resume_data: Dict[str, Any]):
    """Evaluate teamwork and collaboration aspects"""
    try:
        evaluation = openai_service.evaluate_section(resume_data, "teamwork_collaboration")
        return TeamworkCollaborationEvaluation(**evaluation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluating section: {str(e)}")

@app.post("/evaluate-buzzwords", response_model=BuzzwordsEvaluation)
async def evaluate_buzzwords(resume_data: Dict[str, Any]):
    """Evaluate buzzwords and cliches"""
    try:
        evaluation = openai_service.evaluate_section(resume_data, "buzzwords_cliches")
        return BuzzwordsEvaluation(**evaluation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluating section: {str(e)}")

@app.post("/evaluate-unnecessary-sections", response_model=UnnecessarySectionsEvaluation)
async def evaluate_unnecessary_sections(resume_data: Dict[str, Any]):
    """Evaluate unnecessary and irrelevant sections"""
    try:
        evaluation = openai_service.evaluate_section(resume_data, "unnecessary_sections")
        return UnnecessarySectionsEvaluation(**evaluation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluating section: {str(e)}")

@app.post("/evaluate-contact-details", response_model=ContactDetailsEvaluation)
async def evaluate_contact_details(resume_data: Dict[str, Any]):
    """Evaluate contact details completeness and professionalism"""
    try:
        evaluation = openai_service.evaluate_section(resume_data, "contact_details")
        return ContactDetailsEvaluation(**evaluation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluating section: {str(e)}")

@app.post("/evaluate-grammar-spelling", response_model=GrammarSpellingEvaluation)
async def evaluate_grammar_spelling(resume_data: Dict[str, Any]):
    """Evaluate grammar and spelling"""
    try:
        evaluation = openai_service.evaluate_section(resume_data, "grammar_spelling")
        return GrammarSpellingEvaluation(**evaluation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluating section: {str(e)}")

@app.post("/evaluate-formatting", response_model=FormattingLayoutEvaluation)
async def evaluate_formatting(resume_data: Dict[str, Any]):
    """Evaluate formatting and layout"""
    try:
        evaluation = openai_service.evaluate_section(resume_data, "formatting_layout")
        return FormattingLayoutEvaluation(**evaluation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluating section: {str(e)}")

@app.post("/evaluate-ats-keywords", response_model=ATSKeywordsEvaluation)
async def evaluate_ats_keywords(resume_data: Dict[str, Any]):
    """Evaluate ATS keyword optimization"""
    try:
        evaluation = openai_service.evaluate_section(resume_data, "ats_keywords")
        return ATSKeywordsEvaluation(**evaluation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluating section: {str(e)}")

@app.post("/evaluate-skills-relevance", response_model=SkillsRelevanceEvaluation)
async def evaluate_skills_relevance(resume_data: Dict[str, Any]):
    """Evaluate skill section relevance"""
    try:
        evaluation = openai_service.evaluate_section(resume_data, "skills_relevance")
        return SkillsRelevanceEvaluation(**evaluation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluating section: {str(e)}")

@app.post("/evaluate-achievements-vs-responsibilities", response_model=AchievementsVsResponsibilitiesEvaluation)
async def evaluate_achievements_vs_responsibilities(resume_data: Dict[str, Any]):
    """Evaluate achievements versus responsibilities"""
    try:
        evaluation = openai_service.evaluate_section(resume_data, "achievements_vs_responsibilities")
        return AchievementsVsResponsibilitiesEvaluation(**evaluation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluating section: {str(e)}")

@app.post("/evaluate-education-clarity", response_model=EducationClarityEvaluation)
async def evaluate_education_clarity(resume_data: Dict[str, Any]):
    """Evaluate education section clarity"""
    try:
        evaluation = openai_service.evaluate_section(resume_data, "education_clarity")
        return EducationClarityEvaluation(**evaluation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluating section: {str(e)}")

@app.post("/analyze-complete-resume")
async def analyze_complete_resume(resume_data: Dict[str, Any]):
    """Perform complete resume analysis across all sections"""
    try:
        from services.resume_analyzer import ResumeAnalyzer
        analyzer = ResumeAnalyzer()
        analysis = analyzer.analyze_complete_resume(resume_data)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in complete analysis: {str(e)}")

@app.post("/improvement-report")
async def get_improvement_report(resume_data: Dict[str, Any]):
    """Generate comprehensive improvement report"""
    try:
        from services.resume_analyzer import ResumeAnalyzer
        analyzer = ResumeAnalyzer()
        report = analyzer.generate_improvement_report(resume_data)
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Resume Analyzer API is running"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)



