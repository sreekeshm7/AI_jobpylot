import openai
import json
from typing import Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

class OpenAIService:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def parse_resume_to_json(self, resume_text: str) -> Dict[str, Any]:
        prompt = f"""
Parse the following resume text and convert it to the exact JSON format specified below.

For the 'Projects' section:
- Extract the main project description as a paragraph into the "description" field.
- Also extract ALL bullet points (if any) into the "bullets" array, as individual action/result-oriented sentences.
- Do not merge project bullets into the project description; each bullet should be a sentence starting with an action verb.
- If the project has no bullets, "bullets" should be an empty array.

Preserve as much original content as possible; accurately separate descriptions from bullets.

Resume Text:
{resume_text}

Required JSON Format:
{{
  "resume": {{
    "Name": "...",
    "Email": "...",
    "Phone": "...",
    "Links": {{
      "LinkedIn": "...",
      "GitHub": "...",
      "Portfolio": "...",
      "OtherLinks": [],
      "Projects": [
        {{
          "Title": "...",
          "Description": "...",
          "LiveLink": "...",
          "GitHubLink": "...",
          "StartDate": "...",
          "EndDate": "...",
          "Role": "...",
          "description": "...",
          "bullets": ["...", "..."],
          "TechStack": []
        }}
      ]
    }},
    "Summary": "...",
    "Skills": {{
      "Tools": [],
      "soft_skills": [],
      "TechStack": [],
      "Languages": [],
      "Others": []
    }},
    "WorkExperience": [
      {{
        "JobTitle": "...",
        "Company": "...",
        "Duration": "...",
        "Location": "...",
        "Responsibilities": [],
        "TechStack": []
      }}
    ],
    "Education": [
      {{
        "Degree": "...",
        "Mark": "...",
        "Institution": "...",
        "Location": "...",
        "StartYear": "...",
        "EndYear": "..."
      }}
    ],
    "Certifications": [],
    "Languages": [],
    "Achievements": [],
    "Awards": [],
    "VolunteerExperience": [],
    "Hobbies": [],
    "Interests": [],
    "References": []
  }},
  "summary": "One-paragraph professional summary (same as Summary above)"
}}
Only return the JSON object. Do not include explanations or extra prose.
"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse OpenAI response as JSON: {str(e)}")
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")

    def evaluate_summary(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluate resume summary with ATS scoring, returning ATS score before and after improvement for each improved summary.
    """
    prompt = f"""
You are an elite Applicant Tracking System (ATS) resume evaluator. Your job is to analyze the "Summary" section of a resume and evaluate its effectiveness for passing automated resume screening.

Resume Data:
{json.dumps(resume_data, indent=2)}

Step 1: Extract the "Summary" field from the resume exactly as it appears.

Step 2: Assign an ATS Score (0–10) to the original summary.
- Use criteria such as keyword density, relevance, action language, clarity, conciseness, and alignment with the full resume.

Step 3: Identify weak sentences or gaps.
- List vague, generic, or irrelevant phrases that reduce the ATS score.
- Include brief reasons (e.g., “lacks measurable impact”, “missing keyword for skill”, “unclear phrasing”).
- Identify any missing but important content.

Step 4: Identify strong sentences.
- Highlight sentences that boost ATS score.
- Explain why they are effective.

Step 5: Give 3–5 bullets explaining how the score was determined.

Step 6: Generate and return exactly 4 dramatically improved summaries.
- Each must be a new version (not a rewording) based on the resume content, concise, max 4 sentences.
- For each, return:
    - "improved": the improved summary text.
    - "original_score": the ATS score (0-10) for the original.
    - "improved_score": the ATS score (0-10) for this new summary.
    - "explanation": why the new summary's score improved (or didn't).

Respond ONLY in the following JSON format:
{{
  "extracted_summary": "...",
  "ats_score": 0,
  "weak_sentences": ["..."],
  "strong_sentences": ["..."],
  "score_feedback": ["...", "...", "..."],
  "improved_summaries": [
    {{"improved": "...", "original_score": 0, "improved_score": 0, "explanation": "..."}},
    {{"improved": "...", "original_score": 0, "improved_score": 0, "explanation": "..."}},
    {{"improved": "...", "original_score": 0, "improved_score": 0, "explanation": "..."}},
    {{"improved": "...", "original_score": 0, "improved_score": 0, "explanation": "..."}}
  ]
}}
"""
    try:
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        # Accept only "improved_summaries", not "new_summaries"
        result = json.loads(response.choices[0].message.content)
        # Backwards compatibility: if "new_summaries" exists and "improved_summaries" does not, migrate over
        if "new_summaries" in result and not result.get("improved_summaries"):
            result["improved_summaries"] = []
            for ns in result["new_summaries"]:
                result["improved_summaries"].append({"improved": ns, "original_score": result.get("ats_score", 0), "improved_score": result.get("ats_score", 0), "explanation": ""})
            result.pop("new_summaries")
        return result
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse OpenAI response as JSON: {str(e)}")
    except Exception as e:
        raise Exception(f"OpenAI API error: {str(e)}")



    def evaluate_section(self, resume_data: Dict[str, Any], section_name: str) -> Dict[str, Any]:
        """
        Evaluate specific resume section with detailed, targeted prompts.
        """
        prompt = self._get_section_specific_prompt(resume_data, section_name)
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse OpenAI response as JSON: {str(e)}")
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")

    def _get_section_specific_prompt(self, resume_data: Dict[str, Any], section_name: str) -> str:
        resume_json = json.dumps(resume_data, indent=2)
        if section_name == "quantifiable_impact":
            return f"""
You are an ATS resume analysis expert. Analyze quantifiable impact and measurable achievements in the resume.

Resume Data: {resume_json}

Tasks:
1. Identify sentences where impact is NOT quantified or metrics are missing.
2. For each weak sentence, rewrite it to maximize quantifiable impact and metrics.
3. For every improvement, output:
   - "original": the original sentence,
   - "improved": the improved version,
   - "original_score": ATS score (0-10) for the original,
   - "improved_score": ATS score (0-10) for your improved sentence,
   - "explanation": why/if the score has changed.
Return:
{{
  "section_name": "quantifiable_impact",
  "ats_score": <overall section score>,
  "feedback": [...],
  "weak_sentences": [...],
  "strong_sentences": [...],
  "improved_content": [
      {{
          "original": "...",
          "improved": "...",
          "original_score": X,
          "improved_score": Y,
          "explanation": "..."
      }}, ...
  ],
  "examples": [...]
}}
"""
        elif section_name == "date_format":
            return f"""
You are an expert resume analyst specializing in date formatting and chronology.

Resume Data: {resume_json}

Return:
{{
  "section_name": "date_format",
  "ats_score": 0,
  "feedback": ["..."],
  "date_issues": ["..."],
  "suggested_format": "...",
  "formatting_issues": ["..."],
  "corrections": ["..."]
}}
"""
        elif section_name == "weak_verbs":
            return f"""
You are an ATS resume expert focusing on action verbs.

Resume Data: {resume_json}

Tasks:
- For every weak/passive verb sentence, rewrite using a strong, active verb.
- For each improvement, return:
   - "original": "...",
   - "improved": "...",
   - "original_score": X,
   - "improved_score": Y,
   - "explanation": "..."
Return:
{{
  "section_name": "weak_verbs",
  "ats_score": <overall section score>,
  "feedback": [...],
  "weak_sentences": [...],
  "strong_sentences": [...],
  "improved_content": [
      {{
        "original": "...",
        "improved": "...",
        "original_score": X,
        "improved_score": Y,
        "explanation": "..."
      }},
      ...
  ],
  "examples": [...]
}}
"""
        elif section_name == "teamwork_collaboration":
            return f"""
You are an expert resume analyst specializing in teamwork indicators.

Resume Data: {resume_json}

Return:
{{
  "section_name": "teamwork_collaboration",
  "ats_score": 0,
  "feedback": [...],
  "weak_sentences": [...],
  "strong_sentences": [...],
  "improved_content": [...],
  "examples": [...]
}}
"""
        elif section_name == "buzzwords_cliches":
            return f"""
You are an expert resume analyst specializing in buzzwords and clichés.

Resume Data: {resume_json}

Return:
{{
  "section_name": "buzzwords_cliches",
  "ats_score": 0,
  "feedback": [...],
  "issues_found": [...],
  "corrections": [...],
  "improved_content": [...],
  "examples": [...]
}}
"""
        elif section_name == "unnecessary_sections":
            return f"""
You are an expert resume analyst specializing in section relevance.

Resume Data: {resume_json}

Return:
{{
  "section_name": "unnecessary_sections",
  "ats_score": 0,
  "feedback": [...],
  "issues_found": [...],
  "missing_information": [...],
  "recommendations": [...]
}}
"""
        elif section_name == "contact_details":
            return f"""
You are an expert resume analyst specializing in contact information.

Resume Data: {resume_json}

Return:
{{
  "section_name": "contact_details",
  "ats_score": 0,
  "feedback": [...],
  "contact_completeness": {{
    "email": true,
    "phone": true,
    "linkedin": true,
    "github": true,
    "portfolio": true,
    "location": true
  }},
  "issues_found": [...],
  "recommendations": [...]
}}
"""
        elif section_name == "grammar_spelling":
            return f"""
You are an expert resume editor specializing in grammar and spelling.

Resume Data: {resume_json}

Return:
{{
  "section_name": "grammar_spelling",
  "ats_score": 0,
  "feedback": [...],
  "grammar_errors": [...],
  "spelling_errors": [...],
  "corrections": [...],
  "improved_content": [...]
}}
"""
        elif section_name == "formatting_layout":
            return f"""
You are an expert in resume formatting and ATS compatibility.

Resume Data: {resume_json}

Return:
{{
  "section_name": "formatting_layout",
  "ats_score": 0,
  "feedback": [...],
  "formatting_issues": [...],
  "recommendations": [...],
  "examples": [...]
}}
"""
        elif section_name == "ats_keywords":
            return f"""
You are an ATS keyword optimization expert.

Resume Data: {resume_json}

Return:
{{
  "section_name": "ats_keywords",
  "ats_score": 0,
  "feedback": [...],
  "missing_keywords": [...],
  "relevant_keywords": [...],
  "recommendations": [...],
  "improved_content": [...]
}}
"""
        elif section_name == "skills_relevance":
            return f"""
You are a resume skills relevance analyst.

Resume Data: {resume_json}

Return:
{{
  "section_name": "skills_relevance",
  "ats_score": 0,
  "feedback": [...],
  "issues_found": [...],
  "missing_information": [...],
  "recommendations": [...],
  "improved_content": [...]
}}
"""
        elif section_name == "achievements_vs_responsibilities":
            return f"""
You are an ATS resume analysis expert. For each responsibility-focused statement:

Resume Data: {resume_json}

Tasks:
- Rewrite to focus on achievements and outcomes.
- For every improvement, output:
  "improved_content": [
      {{
        "original": "...",
        "improved": "...",
        "original_score": X,
        "improved_score": Y,
        "explanation": "..."
      }},
      ...
  ]
Return:
{{
  "section_name": "achievements_vs_responsibilities",
  "ats_score": <overall section score>,
  "feedback": [...],
  "weak_sentences": [...],
  "strong_sentences": [...],
  "improved_content": [...],
  "examples": [...]
}}
"""
        elif section_name == "education_clarity":
            return f"""
You are an expert in resume education section clarity.

Resume Data: {resume_json}

Return:
{{
  "section_name": "education_clarity",
  "ats_score": 0,
  "feedback": [...],
  "issues_found": [...],
  "missing_information": [...],
  "recommendations": [...],
  "corrections": [...]
}}
"""
        else:
            return f"""
You are an expert resume analyst for the {section_name.replace('_',' ')} section.

Resume Data: {resume_json}

Return:
{{
  "section_name": "{section_name}",
  "ats_score": 0,
  "feedback": ["..."]
}}
"""



