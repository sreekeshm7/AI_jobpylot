import os
import json
from typing import Dict, Any, Optional

# Uncomment these if you use openai or other SDK
# import openai

class OpenAIService:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize with LLM API key. Uses OPENAI_API_KEY from env if not supplied.
        """
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        # Uncomment for OpenAI
        # openai.api_key = self.api_key
        self.model = "gpt-4o"

    def parse_resume_to_json(self, resume_text: str) -> Dict[str, Any]:
        """
        Parses a resume into a detailed JSON following advanced instructions for maximum extraction.
        """
        prompt = (
            "Parse the following resume text into JSON, using the exact schema below. "
            "Pay special attention to the Projects section: "
            "If bullets are present, use them. If not, extract clear action/result statements from paragraphs as bullets. "
            "Always extract both the main description (as a paragraph) and a granular bullets array from project narratives, even if only paragraph text is given. "
            "Never skip tech stack. Always provide everything possible, using lists or empty as per type. "
            "Do not hallucinate. Return only the JSON object. "
            "Resume Text:\n"
            f"{resume_text}\n\n"
            "SCHEMA:\n"
            "{\n"
            '  "resume": {\n'
            '    "Name": "...",\n'
            '    "Email": "...",\n'
            '    "Phone": "...",\n'
            '    "Links": {\n'
            '      "LinkedIn": "...",\n'
            '      "GitHub": "...",\n'
            '      "Portfolio": "...",\n'
            '      "OtherLinks": []\n'
            '    },\n'
            '    "Projects": [\n'
            "      {\n"
            '        "Title": "...",\n'
            '        "Description": "...",\n'
            '        "LiveLink": "...",\n'
            '        "GitHubLink": "...",\n'
            '        "StartDate": "...",\n'
            '        "EndDate": "...",\n'
            '        "Role": "...",\n'
            '        "description": "...",\n'
            '        "bullets": [],\n'
            '        "TechStack": []\n'
            "      }\n"
            "    ],\n"
            '    "Summary": "...",\n'
            '    "Skills": {\n'
            '      "Tools": [],\n'
            '      "soft_skills": [],\n'
            '      "TechStack": [],\n'
            '      "Languages": [],\n'
            '      "Others": []\n'
            "    },\n"
            '    "WorkExperience": [\n'
            "      {\n"
            '        "JobTitle": "...",\n'
            '        "Company": "...",\n'
            '        "Duration": "...",\n'
            '        "Location": "...",\n'
            '        "Responsibilities": [],\n'
            '        "TechStack": []\n'
            "      }\n"
            "    ],\n"
            '    "Education": [\n'
            "      {\n"
            '        "Degree": "...",\n'
            '        "Mark": "...",\n'
            '        "Institution": "...",\n'
            '        "Location": "...",\n'
            '        "StartYear": "...",\n'
            '        "EndYear": "..."\n'
            "      }\n"
            "    ],\n"
            '    "Certifications": [],\n'
            '    "Languages": [],\n'
            '    "Achievements": [],\n'
            '    "Awards": [],\n'
            '    "VolunteerExperience": [],\n'
            '    "Hobbies": [],\n'
            '    "Interests": [],\n'
            '    "References": []\n'
            "  },\n"
            '  "summary": "A single-paragraph professional summary as above"\n'
            "}\n"
            "Extract all sentences and all details, and fully parse Projects section even from unstructured text."
        )

        # -- Your LLM/LLM API call goes here --
        # Uncomment and adjust:
        # response = openai.ChatCompletion.create(
        #     model=self.model,
        #     messages=[{"role": "user", "content": prompt}],
        #     temperature=0,
        #     max_tokens=4096
        # )
        # result_text = response.choices[0].message["content"]

        # try:
        #     return json.loads(result_text)
        # except Exception:
        #     return result_text  # or raise or return {"error": "Parsing failed", ...}

        # For demonstration purposes:
        raise NotImplementedError("Plug in your own LLM call as annotated above.")

    def analyze_resume_section(self, resume_json: Dict[str, Any], section_name: str) -> Dict[str, Any]:
        """
        Analyzes one resume section or aspect at a time using improved prompts.
        """
        prompt = self._get_section_specific_prompt(resume_json, section_name)

        # -- Your LLM/LLM API call goes here --
        # Uncomment and adjust:
        # response = openai.ChatCompletion.create(
        #     model=self.model,
        #     messages=[{"role": "user", "content": prompt}],
        #     temperature=0,
        #     max_tokens=2048
        # )
        # result_text = response.choices[0].message["content"]
        # try:
        #     return json.loads(result_text)
        # except Exception:
        #     return result_text

        # For demonstration purposes:
        raise NotImplementedError("Plug in your own LLM call as annotated above.")

    def _get_section_specific_prompt(self, resume_data: Dict[str, Any], section_name: str) -> str:
        """
        Improved prompts per section, as in prior completions.
        """
        resume_json = json.dumps(resume_data, indent=2)
        if section_name == "quantifiable_impact":
            prompt = f'''
You are an expert resume analyst with specialization in identifying quantifiable achievements and measurable impact statements.
Resume Data: {resume_json}
ANALYSIS TASKS:
- Identify and extract all statements that include specific numbers, percentages, metrics, or measurable results.
- Distinguish actual achievements from generic duties.
- Rate the use of metrics: revenue, time saved, KPIs, etc.
- For weak statements, suggest how to add quantification and rewrite to highlight impact.
- Provide at least 3 strong achievement-focused sentence examples tailored to the field.
- In feedback, highlight both missing opportunities and best practices.
SCORING:
- 9–10: Many clear quantified results, strong impact, matches role/industry.
- 5–8: Some quantification, but inconsistent.
- 1–4: Little/no quantification.
Respond ONLY in this JSON:
{{
  "section_name": "quantifiable_impact",
  "ats_score": 0,
  "feedback": [],
  "weak_sentences": [],
  "strong_sentences": [],
  "improved_content": [],
  "examples": []
}}
'''
        elif section_name == "date_format":
            prompt = f'''
You are an expert in resume chronology and date formatting.
Resume Data: {resume_json}
ANALYSIS TASKS:
- Scrutinize all date fields for format consistency (e.g., MM/YYYY everywhere).
- Detect any missing, ambiguous, or inconsistent date entries—especially start/end dates in Education/Experience.
- Flag chronology issues (are most recent entries listed first? Are there gaps?).
- Check correct use and formatting of "Present"/"Current."
- Recommend ONE clear, uniform date format to apply everywhere.
SCORING:
- 9–10: All dates logical, consistent, nothing missing.
- 1–4: Major inconsistencies or missing dates.
Respond ONLY in this JSON:
{{
  "section_name": "date_format",
  "ats_score": 0,
  "feedback": [],
  "date_issues": [],
  "suggested_format": "",
  "formatting_issues": [],
  "corrections": []
}}
'''
        elif section_name == "weak_verbs":
            prompt = f'''
You are an expert resume language coach focused on action verbs.
Resume Data: {resume_json}
ANALYSIS TASKS:
- Identify every bullet or phrase using weak, passive, or generic verbs (e.g., "helped with," "was responsible for").
- Suggest aggressive, impactful action verb replacements for each weak instance, tailored to the resume/job function.
- Provide at least 3 model rewrites showing strong verbs.
- For feedback, contrast before/after and explain why verb strength matters.
SCORING:
- 9–10: Strong, varied verbs throughout.
- 1–4: Excessive weak verbs.
Respond ONLY in this JSON:
{{
  "section_name": "weak_verbs",
  "ats_score": 0,
  "feedback": [],
  "weak_sentences": [],
  "strong_sentences": [],
  "improved_content": [],
  "examples": []
}}
'''
        elif section_name == "teamwork_collaboration":
            prompt = f'''
You are a resume evaluator with expertise in teamwork, collaboration, and cross-functional skills.
Resume Data: {resume_json}
ANALYSIS TASKS:
- Find all examples of teamwork: group accomplishments, collaboration, leadership.
- Suggest improvements for solo- or vague-sounding statements.
- Highlight best sentences/sections that show collaboration.
SCORING:
- 9–10: Ample, specific teamwork evidence.
- 1–4: Very little teamwork shown.
Respond ONLY in this JSON:
{{
  "section_name": "teamwork_collaboration",
  "ats_score": 0,
  "feedback": [],
  "weak_sentences": [],
  "strong_sentences": [],
  "improved_content": [],
  "examples": []
}}
'''
        elif section_name == "buzzwords_cliches":
            prompt = f'''
You are a resume expert specializing in language specificity and avoidance of clichés.
Resume Data: {resume_json}
ANALYSIS TASKS:
- Flag all buzzwords or clichés (e.g., dynamic, results-driven).
- For each, recommend concrete rewrites, or removal if fluff.
- Provide at least 3 examples of better alternatives for the field.
SCORING:
- 9–10: Direct, evidence-based language only.
- 1–4: Major buzzword/cliché problem.
Respond ONLY in this JSON:
{{
  "section_name": "buzzwords_cliches",
  "ats_score": 0,
  "feedback": [],
  "issues_found": [],
  "corrections": [],
  "improved_content": [],
  "examples": []
}}
'''
        elif section_name == "unnecessary_sections":
            prompt = f'''
You are an expert in resume structure and relevance.
Resume Data: {resume_json}
ANALYSIS TASKS:
- Evaluate if each section (Hobbies, References, etc.) adds job-relevant value.
- Flag outdated, irrelevant, redundant, or missing sections.
- Suggest best order/organization for maximum recruiter impact.
SCORING:
- 9–10: All sections add value and are relevant.
- 1–4: Contains fluff, missing essentials, poor order.
Respond ONLY in this JSON:
{{
  "section_name": "unnecessary_sections",
  "ats_score": 0,
  "feedback": [],
  "issues_found": [],
  "missing_information": [],
  "recommendations": []
}}
'''
        elif section_name == "contact_details":
            prompt = f'''
You are a professional resume auditor focusing on contact details.
Resume Data: {resume_json}
ANALYSIS TASKS:
- Check for presence, correctness, professionalism in: Name, Email, Phone, LinkedIn, Portfolio/GitHub, Location (not full address).
- Flag incomplete, unprofessional, or unsafe contact info.
- Suggest correct best-practice format for each.
SCORING:
- 9–10: Fully complete and professional.
- 1–4: Missing essentials/unprofessional.
Respond ONLY in this JSON:
{{
  "section_name": "contact_details",
  "ats_score": 0,
  "feedback": [],
  "contact_completeness": {{"email": false, "phone": false, "linkedin": false, "github": false, "portfolio": false, "location": false}},
  "issues_found": [],
  "recommendations": []
}}
'''
        elif section_name == "grammar_spelling":
            prompt = f'''
You are a senior editor auditing grammar, spelling, and language quality.
Resume Data: {resume_json}
ANALYSIS TASKS:
- Detect grammar, spelling, punctuation, capitalization errors everywhere.
- Spot tense inconsistencies, incomplete/awkward sentences, bullet punctuation.
- Provide direct corrections for every issue, and 3+ improved/rewritten examples.
SCORING:
- 9–10: Flawless grammar/spelling.
- 1–4: Frequent/serious errors.
Respond ONLY in this JSON:
{{
  "section_name": "grammar_spelling",
  "ats_score": 0,
  "feedback": [],
  "grammar_errors": [],
  "spelling_errors": [],
  "corrections": [],
  "improved_content": []
}}
'''
        elif section_name == "formatting_layout":
            prompt = f'''
You are a specialist in resume formatting and ATS compatibility.
Resume Data: {resume_json}
ANALYSIS TASKS:
- Ensure all sections are logically ordered and separated.
- Review date format, bullets, spacing, ATS compatibility.
- Suggest specific formatting improvements.
SCORING:
- 9–10: Clean, professional, ATS-friendly.
- 1–4: Disorganized/problematic.
Respond ONLY in this JSON:
{{
  "section_name": "formatting_layout",
  "ats_score": 0,
  "feedback": [],
  "formatting_issues": [],
  "recommendations": [],
  "examples": []
}}
'''
        elif section_name == "ats_keywords":
            prompt = f'''
You are an ATS optimization specialist focused on keyword coverage.
Resume Data: {resume_json}
ANALYSIS TASKS:
- List hard/soft skill keywords present and missing for the target role/field.
- Suggest where to integrate missing or stronger keywords.
- Give 3+ example sentences with optimal keyword density/context.
SCORING:
- 9–10: Rich, targeted keywords used contextually.
- 1–4: Major gaps or generic phrasing.
Respond ONLY in this JSON:
{{
  "section_name": "ats_keywords",
  "ats_score": 0,
  "feedback": [],
  "missing_keywords": [],
  "relevant_keywords": [],
  "recommendations": [],
  "improved_content": []
}}
'''
        elif section_name == "skills_relevance":
            prompt = f'''
You are a skills analyst evaluating skills section completeness/relevance.
Resume Data: {resume_json}
ANALYSIS TASKS:
- Assess for missing/irrelevant/outdated skills, organization, grouping.
- Suggest improvements (clarity, logic, impact).
- Provide examples for better grouping/language.
SCORING:
- 9–10: Well-organized, comprehensive, current.
- 1–4: Incomplete, poorly organized, irrelevant items.
Respond ONLY in this JSON:
{{
  "section_name": "skills_relevance",
  "ats_score": 0,
  "feedback": [],
  "issues_found": [],
  "missing_information": [],
  "recommendations": [],
  "improved_content": []
}}
'''
        elif section_name == "achievements_vs_responsibilities":
            prompt = f'''
You are an expert distinguishing achievements from responsibilities in resumes.
Resume Data: {resume_json}
ANALYSIS TASKS:
- Separate achievement-focused from responsibility-only statements.
- Transform duties into results/impact; give 3+ before/after examples.
- List best/weakest examples and rewrites.
- Tips for proper balance.
SCORING:
- 9–10: Mostly achievement-driven.
- 1–4: Mostly just responsibilities.
Respond ONLY in this JSON:
{{
  "section_name": "achievements_vs_responsibilities",
  "ats_score": 0,
  "feedback": [],
  "weak_sentences": [],
  "strong_sentences": [],
  "improved_content": [],
  "examples": []
}}
'''
        elif section_name == "education_clarity":
            prompt = f'''
You are a specialist in education section clarity/completeness.
Resume Data: {resume_json}
ANALYSIS TASKS:
- Check for degree, major, school, location, years.
- Spot missing/inconsistent dates, order, irrelevant schooling.
- Suggest best summary for job stage/seniority.
SCORING:
- 9–10: Clear, complete, professional.
- 1–4: Incomplete/unprofessional.
Respond ONLY in this JSON:
{{
  "section_name": "education_clarity",
  "ats_score": 0,
  "feedback": [],
  "issues_found": [],
  "missing_information": [],
  "recommendations": [],
  "corrections": []
}}
'''
        else:
            prompt = f'''
You are an expert resume analyst.
Resume Data: {resume_json}
TASK: Analyze "{section_name.replace('_', ' ')}" in the resume. Give detailed feedback, score, actionable suggestions.
Respond ONLY in this JSON:
{{
  "section_name": "{section_name}",
  "ats_score": 0,
  "feedback": [],
  "issues_found": [],
  "recommendations": []
}}
'''
        return prompt

    def improve_and_rescore_section(
        self,
        resume_json: Dict[str, Any],
        section_name: str,
        improvements: Any,
        apply_func=None
    ) -> Dict[str, Any]:
        """
        Apply improvements, then rescore the section.
        - improvements: new sentences/content to update
        - apply_func: function to inject improvements in proper place; override per section
        """
        # Step 1: Apply improvements to the resume_json structure.
        # You must provide a function to inject the improvement.
        if apply_func:
            resume_json = apply_func(resume_json, section_name, improvements)
        else:
            # Default: override 'improved_content' if present
            if "improved_content" in resume_json.get(section_name, {}):
                resume_json[section_name]["improved_content"] = improvements
            # Otherwise, user must provide custom apply function.
        # Step 2: Re-analyze and rescore
        return self.analyze_resume_section(resume_json, section_name)
