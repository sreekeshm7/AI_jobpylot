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
        Evaluate resume summary with ATS scoring, or generate 4 new summaries if there is no summary in the input.
        """
        prompt = f"""
    You are an elite Applicant Tracking System (ATS) resume evaluator and writer.
    Review the provided resume data. If a summary is present, analyze and score it as instructed below. 
    If there is **no summary, or the summary is blank**, you must compose FOUR brand-new, ATS-optimized professional summaries from scratch. Each summary should be realistic, concise (max 4 sentences), and directly based on the full experience, skills, education, and roles listed in the resume.
    
    Instructions:
    
    **Step 1:** Extract the "Summary" field from the resume *exactly as it appears*.
    
    **Step 2:** Assign an ATS Score (0–10) to the original summary.  
    If there is no summary, set "extracted_summary" to an empty string and "ats_score" to 0.
    
    **Step 3:** Identify Weak Sentences
    - From the summary, list the literal sentences or fragments that reduce ATS score (if any).
    - If there is no summary, leave the list empty: [].
    
    **Step 4:** Identify Strong Sentences
    - From the summary, list the sentences or phrases that effectively boost ATS score, copying their literal text as they appear in the summary.
    - If there is no summary, leave the list empty: [].
    
    **Step 5:** Give 3–5 bullets in "score_feedback" explaining the ATS score.
    - If there is no summary, explain that no summary was available, so scoring is not possible.
    
    **Step 6:** Compose or Improve ATS-Optimized Summaries
    - If a summary is present, rewrite it into 4 new and improved summaries, each with:
        - "improved": the improved summary.
        - "original_score": the ATS score (for the original).
        - "improved_score": ATS score for this improved version.
        - "explanation": what makes this new version better for ATS/recruiter screening.
    - If the summary is missing/blank, analyze the entire resume and GENERATE FOUR original professional summaries. Each summary should:
        - Use the candidate's actual experience, skills, education, and background.
        - Fit the length and clarity requirements of top-tier resumes (max 4 sentences).
        - Highlight slightly different strengths (technical, leadership, impact, etc).
        - Score 9–10 for modern ATS.
        - For each, set "original_score" to 0 and "explanation" to explain its ATS strengths.
    
    Respond ONLY in the following JSON format:
    {{
      "extracted_summary": "...",
      "ats_score": 0,
      "weak_sentences": [...],
      "strong_sentences": [...],
      "score_feedback": [...],
      "improved_summaries": [
        {{"improved": "...", "original_score": 0, "improved_score": 10, "explanation": "..."}},
        {{"improved": "...", "original_score": 0, "improved_score": 10, "explanation": "..."}},
        {{"improved": "...", "original_score": 0, "improved_score": 10, "explanation": "..."}},
        {{"improved": "...", "original_score": 0, "improved_score": 10, "explanation": "..."}}
      ]
    }}
    - If there is no input summary, synthesize the four improved_summaries as new summaries from the resume data and make them excellent ATS-ready options. Do NOT return blanks.
    """
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            result = json.loads(response.choices[0].message.content)
            return result
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse OpenAI response as JSON: {str(e)}")
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")



    def suggest_relevant_skills(self, resume_data: Dict[str, Any], target_role: str = "") -> Dict[str, Any]:
        prompt = f"""
You are an expert resume AI and career advisor.
Analyze the following resume. Your job is to suggest the most relevant and high-impact skills (technical and soft) that are either missing from the 'Skills' section or could be added or emphasized to make this candidate a stronger fit for{" the role of " + target_role if target_role else " their next job"}.
- Be specific and job-market-aware for {target_role if target_role else "the technology sector"}.
- Suggest only skills that align with the candidate's background or desired role, not random "buzzwords".
Resume JSON:
{json.dumps(resume_data, indent=2)}
Return your answer as:
{{
  "suggested_skills": ["...", "..."],
  "rationale": ["...Explain why each skill is suggested (one per skill, or one rationale string for all)..."]
}}
"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            raise Exception(f"OpenAI API error (skill suggestion): {str(e)}")

    def rewrite_section(self, section: str, description: str, resume_data: Dict[str, Any] = None) -> Dict[str, Any]:
        context_block = f"\nResume Context:\n{json.dumps(resume_data, indent=2)}" if resume_data else ""
        prompt = f"""
You are an expert resume writer and ATS optimization specialist.
Your job is to rewrite the following {section} section's description to maximize professional clarity, impact, strong action verbs, and ATS-relevant keywords.
- Keep the output the same length or shorter.
- Use specific, quantifiable achievements if possible.
- Improve grammar, clarity, and alignment with the best resume practices for this section.
Original description:
\"\"\"{description}\"\"\"
{context_block}
Return your answer in this JSON format:
{{
  "original": "...",
  "rewritten": "...",
  "rationale": "...(brief, 1–2 sentence explanation of how and why the rewrite is improved for ATS and recruiter impact)..."
}}
"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            raise Exception(f"OpenAI API error (section rewrite): {str(e)}")

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


