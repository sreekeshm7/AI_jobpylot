import os
import json
from typing import Dict, Any, Optional, Callable

# Uncomment if using OpenAI SDK:
# import openai

class OpenAIService:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize with LLM API key. Uses OPENAI_API_KEY from env if not supplied.
        """
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        # openai.api_key = self.api_key
        self.model = "gpt-4o"

    def parse_resume_to_json(self, resume_text: str) -> Dict[str, Any]:
        """
        Parse an unstructured resume—extract EVERYTHING. For each section and especially Projects:
        - For Projects, extract:
          * All titles, main description/summary, links (live, GitHub etc.)
          * EVERY sentence about the project (turn paragraphs into bullets if needed)
          * Action/result/impact sentences even if not formatted as bullets
          * Full TechStack (from any mention)
        - For all other sections (WorkExperience/Education): same fidelity; extract every detail and split into most granular JSON.
        """
        prompt = (
            "Extract every detail from the following resume into the JSON format below. "
            "In the Projects section, capture each project as an object with: Title, short Description (project summary), LiveLink, GitHubLink, StartDate, EndDate, Role. "
            "ALWAYS include:\n- ALL sentences from paragraphs (as a list of bullets, even if not bullet-formatted)\n"
            "- Main paragraph description (joined text for summary)\n"
            "- TechStack (all tools/libraries/skills/tech mentioned for each project)\n"
            "If explicit bullets exist, use them. Otherwise, split project descriptions into meaningful achievement/action/result sentences as bullets. "
            "For WorkExperience and Education, extract every sentence or bullet. Fill empty lists if no data. DO NOT hallucinate. Only output the JSON object."
            "\n\nRESUME TEXT:\n"
            f"{resume_text}\n\n"
            "OUTPUT EXACT FORMAT:\n"
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
            "All project and experience descriptions must capture every impactful sentence, whether bullet or not."
        )
        # Place your LLM call here:
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
        #     return result_text
        raise NotImplementedError("Plug in your own LLM call as per your stack.")

    def analyze_resume_section(self, resume_json: Dict[str, Any], section_name: str) -> Dict[str, Any]:
        """
        Analyze one resume section; always recommend the BEST possible ('ideal ATS') rewritten content for that section.
        """
        prompt = self._get_section_specific_prompt(resume_json, section_name)

        # Place your LLM call here:
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
        raise NotImplementedError("Plug in your own LLM call as per your stack.")

    def _get_section_specific_prompt(self, resume_data: Dict[str, Any], section_name: str) -> str:
        """
        For each ATS section, provides a highly tailored evaluation prompt.
        ALWAYS returns BOTH an objective score/evaluation and the best possible, model-recommended rewrite.
        """
        resume_json = json.dumps(resume_data, indent=2)
        s = section_name  # for clarity/shorthand

        # Maintainable template for every section:
        PROMPT_TEMPLATES = {
            "quantifiable_impact": f"""
You are an expert resume analyst.
Given the resume data, for the 'quantifiable impact' section, do ALL:
- Identify every result, outcome, or achievement with numbers/percentages/metrics (quantified).
- For every weak or generic statement, rewrite to maximize impact, with ATS-winning specificity, quantification, and action verbs.
- List the section's ATS score (1–10), and give the single BEST rewriting of all content as it would appear on a perfect ATS-oriented resume.
Return: JSON with fields: ats_score, feedback, weak_sentences, strong_sentences, improved_content, best_ats_version.
Resume Data:
{resume_json}
""",
            "date_format": f"""
You are an expert in resume chronology and date formatting.
- Audit date fields for uniformity (e.g., MM/YYYY everywhere), completeness, and chronology (no gaps/out-of-order entries).
- Suggest and show one universal date format for the resume.
- Rewrite all date entries for best ATS standards.
- Return score (1-10), feedback, issues, best_ats_version (dates properly reformatted only).
Resume Data:
{resume_json}
""",
            "weak_verbs": f"""
You are an ATS resume language coach.
- Identify all instances of weak, repetitive, or passive verbs.
- Rewrite every sentence for strong, varied, ATS-winning action verbs.
- Output: score (1-10), feedback, improved_content, best_ats_version.
Resume Data:
{resume_json}
""",
            "teamwork_collaboration": f"""
You are an ATS-focused resume expert.
- Evaluate all statements for demonstration of teamwork, leadership, collaboration, stakeholder communication.
- For any project/role lacking teamwork evidence, rewrite for greatest ATS impact.
- Output: score (1-10), feedback, best/weakest evidence, improved_content, best_ats_version.
Resume Data:
{resume_json}
""",
            "buzzwords_cliches": f"""
You are an expert in ATS language optimization.
- Flag all generic buzzwords/clichés and replace them with concrete, result-oriented phrasing.
- Show before/after comparisons.
- Return: score (1-10), feedback, improved_content (rewritten for specificity), best_ats_version (all fluff removed).
Resume Data:
{resume_json}
""",
            "unnecessary_sections": f"""
You are a resume optimization strategist.
- Evaluate the value of all resume sections (hobbies, references, summary, objective, etc).
- For any irrelevant or outdated section, recommend omission or replacement.
- Reorder for best ATS results.
- Output: ats_score, feedback, recommended layout/sections (as best_ats_version).
Resume Data:
{resume_json}
""",
            "contact_details": f"""
You are a professional resume auditor for contact details.
- Audit: Name, Email (professional), Phone, LinkedIn, Portfolio/GitHub, Location (city/state only).
- Flag any risky, missing, or unprofessional detail.
- Recommend best-structured, ATS-compliant contact block as best_ats_version.
Resume Data:
{resume_json}
""",
            "grammar_spelling": f"""
You are a senior editor for ATS resumes.
- Identify and correct errors in grammar, spelling, punctuation, tense, and bullet structure.
- Output: ats_score, all corrections, feedback, best_ats_version (flawless grammar).
Resume Data:
{resume_json}
""",
            "formatting_layout": f"""
You are an ATS compliance and formatting expert.
- Audit: logical flow, section separation, spacing, bullet alignment, ATS safety (no columns, graphics, or weird fonts).
- List all improvements, and present the best-possible formatted section as best_ats_version.
Resume Data:
{resume_json}
""",
            "ats_keywords": f"""
You are an ATS keyword optimization specialist.
- Identify all present and missing keywords relevant for the target field/role/seniority.
- Rewrite the section to maximally include the most important ATS keywords in context, without fluff.
- Output: ats_score, recommended keywords, best_ats_version.
Resume Data:
{resume_json}
""",
            "skills_relevance": f"""
You are a skills section ATS optimizer.
- Audit skill lists for completeness, currency, and grouping (technical, soft, languages, certifications).
- Rewrite for organization and keyword richness (best_ats_version).
- Output: ats_score, feedback, missing items, best_ats_version.
Resume Data:
{resume_json}
""",
            "achievements_vs_responsibilities": f"""
You are an ATS resume achievements expert.
- Extract all statements on work/experience. For any duty-only ("responsible for..."), rewrite to achievement/result/impact form for maximum ATS.
- Output: ats_score, feedback, before/after, best_ats_version.
Resume Data:
{resume_json}
""",
            "education_clarity": f"""
You are an education section evaluator with ATS focus.
- Check for education completeness, clarity, date consistency.
- Summarize as concise, ATS-best version (clean, chronological, all fields filled, with any honors/awards).
- Output: ats_score, feedback, missing info, best_ats_version.
Resume Data:
{resume_json}
"""
        }
        prompt = PROMPT_TEMPLATES.get(
            s,
            f"""
You are an ATS-focused resume expert.
- Carefully evaluate the '{s.replace('_', ' ')}' section in the resume data below.
- Score the section 1–10 for ATS excellence. Recommend all improvements as best_ats_version in strict JSON.
Resume Data:
{resume_json}
"""
        )
        return prompt

    def improve_and_rescore_section(
        self,
        resume_json: Dict[str, Any],
        section_name: str,
        improvements: Any,
        apply_func: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """
        Apply improvements, then re-score by re-analyzing the improved section as latest.
        """
        if apply_func:
            resume_json = apply_func(resume_json, section_name, improvements)
        # Or: user can externally update resume_json, then simply call analyze_resume_section
        return self.analyze_resume_section(resume_json, section_name)
