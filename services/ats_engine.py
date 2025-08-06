import openai
import json
import re
from typing import Dict, Any, List, Optional, Tuple
import os
from datetime import datetime
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class JobRequirement:
    title: str
    required_skills: List[str]
    preferred_skills: List[str]
    experience_years: int
    education_level: str
    industry: str
    location: str
    description: str

@dataclass
class CandidateScore:
    candidate_id: str
    overall_score: float
    skills_match: float
    experience_match: float
    education_match: float
    keyword_match: float
    ats_compatibility: float
    detailed_feedback: Dict[str, Any]

class ATSEngine:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.job_requirements_db = {}
        self.candidates_db = {}
        
    def add_job_posting(self, job_id: str, job_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new job posting to the ATS system"""
        job_requirement = JobRequirement(
            title=job_data.get("title", ""),
            required_skills=job_data.get("required_skills", []),
            preferred_skills=job_data.get("preferred_skills", []),
            experience_years=job_data.get("experience_years", 0),
            education_level=job_data.get("education_level", ""),
            industry=job_data.get("industry", ""),
            location=job_data.get("location", ""),
            description=job_data.get("description", "")
        )
        
        self.job_requirements_db[job_id] = job_requirement
        
        return {
            "job_id": job_id,
            "status": "added",
            "requirements": job_requirement.__dict__
        }
    
    def add_candidate(self, candidate_id: str, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a candidate to the ATS system"""
        # Extract key information from resume
        candidate_info = {
            "name": resume_data.get("resume", {}).get("Name", ""),
            "email": resume_data.get("resume", {}).get("Email", ""),
            "skills": self._extract_all_skills(resume_data),
            "experience_years": self._calculate_experience_years(resume_data),
            "education": self._extract_education(resume_data),
            "work_history": resume_data.get("resume", {}).get("WorkExperience", []),
            "resume_data": resume_data,
            "added_date": datetime.now().isoformat()
        }
        
        self.candidates_db[candidate_id] = candidate_info
        
        return {
            "candidate_id": candidate_id,
            "status": "added",
            "candidate_info": candidate_info
        }
    
    def match_candidate_to_job(self, candidate_id: str, job_id: str) -> CandidateScore:
        """Match a candidate to a specific job and return detailed scoring"""
        if candidate_id not in self.candidates_db:
            raise ValueError(f"Candidate {candidate_id} not found")
        if job_id not in self.job_requirements_db:
            raise ValueError(f"Job {job_id} not found")
        
        candidate = self.candidates_db[candidate_id]
        job = self.job_requirements_db[job_id]
        
        # Calculate individual scores
        skills_match = self._calculate_skills_match(candidate, job)
        experience_match = self._calculate_experience_match(candidate, job)
        education_match = self._calculate_education_match(candidate, job)
        keyword_match = self._calculate_keyword_match(candidate, job)
        ats_compatibility = self._calculate_ats_compatibility(candidate)
        
        # Calculate overall score (weighted average)
        overall_score = (
            skills_match * 0.3 +
            experience_match * 0.25 +
            education_match * 0.15 +
            keyword_match * 0.2 +
            ats_compatibility * 0.1
        )
        
        detailed_feedback = self._generate_detailed_feedback(
            candidate, job, skills_match, experience_match, 
            education_match, keyword_match, ats_compatibility
        )
        
        return CandidateScore(
            candidate_id=candidate_id,
            overall_score=overall_score,
            skills_match=skills_match,
            experience_match=experience_match,
            education_match=education_match,
            keyword_match=keyword_match,
            ats_compatibility=ats_compatibility,
            detailed_feedback=detailed_feedback
        )
    
    def rank_candidates_for_job(self, job_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Rank all candidates for a specific job"""
        if job_id not in self.job_requirements_db:
            raise ValueError(f"Job {job_id} not found")
        
        candidate_scores = []
        
        for candidate_id in self.candidates_db:
            try:
                score = self.match_candidate_to_job(candidate_id, job_id)
                candidate_scores.append({
                    "candidate_id": candidate_id,
                    "candidate_name": self.candidates_db[candidate_id]["name"],
                    "overall_score": score.overall_score,
                    "skills_match": score.skills_match,
                    "experience_match": score.experience_match,
                    "education_match": score.education_match,
                    "keyword_match": score.keyword_match,
                    "ats_compatibility": score.ats_compatibility,
                    "detailed_feedback": score.detailed_feedback
                })
            except Exception as e:
                print(f"Error scoring candidate {candidate_id}: {str(e)}")
                continue
        
        # Sort by overall score (descending)
        candidate_scores.sort(key=lambda x: x["overall_score"], reverse=True)
        
        return candidate_scores[:limit]
    
    def get_job_recommendations(self, candidate_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Get job recommendations for a candidate"""
        if candidate_id not in self.candidates_db:
            raise ValueError(f"Candidate {candidate_id} not found")
        
        job_scores = []
        
        for job_id, job in self.job_requirements_db.items():
            try:
                score = self.match_candidate_to_job(candidate_id, job_id)
                job_scores.append({
                    "job_id": job_id,
                    "job_title": job.title,
                    "company": job.industry,
                    "location": job.location,
                    "overall_score": score.overall_score,
                    "skills_match": score.skills_match,
                    "experience_match": score.experience_match,
                    "education_match": score.education_match,
                    "keyword_match": score.keyword_match,
                    "ats_compatibility": score.ats_compatibility
                })
            except Exception as e:
                print(f"Error scoring job {job_id}: {str(e)}")
                continue
        
        # Sort by overall score (descending)
        job_scores.sort(key=lambda x: x["overall_score"], reverse=True)
        
        return job_scores[:limit]
    
    def analyze_resume_ats_compatibility(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Comprehensive ATS compatibility analysis"""
        prompt = f"""
You are an expert ATS (Applicant Tracking System) analyst. Analyze the following resume for ATS compatibility and provide a comprehensive evaluation.

Resume Data:
{json.dumps(resume_data, indent=2)}

Provide a detailed analysis in the following JSON format:
{{
  "overall_ats_score": 0-100,
  "parsing_confidence": 0-100,
  "keyword_optimization": 0-100,
  "format_compatibility": 0-100,
  "content_quality": 0-100,
  "detailed_analysis": {{
    "strengths": ["..."],
    "weaknesses": ["..."],
    "critical_issues": ["..."],
    "recommendations": ["..."]
  }},
  "keyword_analysis": {{
    "found_keywords": ["..."],
    "missing_keywords": ["..."],
    "keyword_density": {{"keyword": "density_percentage"}}
  }},
  "format_analysis": {{
    "file_format": "pdf/docx",
    "font_compatibility": "good/fair/poor",
    "layout_issues": ["..."],
    "parsing_confidence": "high/medium/low"
  }},
  "content_analysis": {{
    "quantifiable_achievements": ["..."],
    "action_verbs_used": ["..."],
    "weak_phrases": ["..."],
    "grammar_issues": ["..."]
  }}
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
            raise Exception(f"ATS analysis error: {str(e)}")
    
    def _extract_all_skills(self, resume_data: Dict[str, Any]) -> List[str]:
        """Extract all skills from resume data"""
        skills = []
        resume = resume_data.get("resume", {})
        
        # Extract from skills section
        skills_section = resume.get("Skills", {})
        skills.extend(skills_section.get("Tools", []))
        skills.extend(skills_section.get("TechStack", []))
        skills.extend(skills_section.get("Languages", []))
        skills.extend(skills_section.get("soft_skills", []))
        skills.extend(skills_section.get("Others", []))
        
        # Extract from work experience
        for job in resume.get("WorkExperience", []):
            skills.extend(job.get("TechStack", []))
        
        # Extract from projects
        for project in resume.get("Links", {}).get("Projects", []):
            skills.extend(project.get("TechStack", []))
        
        return list(set(skills))  # Remove duplicates
    
    def _calculate_experience_years(self, resume_data: Dict[str, Any]) -> float:
        """Calculate total years of experience"""
        work_experience = resume_data.get("resume", {}).get("WorkExperience", [])
        total_years = 0
        
        for job in work_experience:
            duration = job.get("Duration", "")
            # Simple duration parsing - in production, use more sophisticated parsing
            if "year" in duration.lower():
                years = re.findall(r'(\d+)', duration)
                if years:
                    total_years += float(years[0])
        
        return total_years
    
    def _extract_education(self, resume_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract education information"""
        return resume_data.get("resume", {}).get("Education", [])
    
    def _calculate_skills_match(self, candidate: Dict[str, Any], job: JobRequirement) -> float:
        """Calculate skills match percentage"""
        candidate_skills = set(skill.lower() for skill in candidate["skills"])
        required_skills = set(skill.lower() for skill in job.required_skills)
        preferred_skills = set(skill.lower() for skill in job.preferred_skills)
        
        if not required_skills:
            return 0.0
        
        # Calculate required skills match
        required_match = len(candidate_skills.intersection(required_skills)) / len(required_skills)
        
        # Calculate preferred skills bonus
        preferred_match = len(candidate_skills.intersection(preferred_skills)) / len(preferred_skills) if preferred_skills else 0
        
        # Weighted score: 80% required skills, 20% preferred skills
        return (required_match * 0.8) + (preferred_match * 0.2)
    
    def _calculate_experience_match(self, candidate: Dict[str, Any], job: JobRequirement) -> float:
        """Calculate experience match"""
        candidate_years = candidate["experience_years"]
        required_years = job.experience_years
        
        if candidate_years >= required_years:
            return 1.0
        elif candidate_years >= required_years * 0.7:
            return 0.8
        elif candidate_years >= required_years * 0.5:
            return 0.6
        else:
            return 0.3
    
    def _calculate_education_match(self, candidate: Dict[str, Any], job: JobRequirement) -> float:
        """Calculate education match"""
        # Simple education level matching
        education_levels = {
            "high school": 1,
            "associate": 2,
            "bachelor": 3,
            "master": 4,
            "phd": 5
        }
        
        candidate_education = candidate["education"]
        required_level = job.education_level.lower()
        
        if not candidate_education:
            return 0.0
        
        # Find highest education level
        highest_level = 0
        for edu in candidate_education:
            degree = edu.get("Degree", "").lower()
            for level, score in education_levels.items():
                if level in degree and score > highest_level:
                    highest_level = score
        
        required_score = education_levels.get(required_level, 0)
        
        if highest_level >= required_score:
            return 1.0
        elif highest_level >= required_score - 1:
            return 0.7
        else:
            return 0.3
    
    def _calculate_keyword_match(self, candidate: Dict[str, Any], job: JobRequirement) -> float:
        """Calculate keyword match using AI analysis"""
        prompt = f"""
Analyze the keyword match between a candidate's resume and a job description.

Job Title: {job.title}
Job Description: {job.description}
Required Skills: {', '.join(job.required_skills)}
Preferred Skills: {', '.join(job.preferred_skills)}

Candidate Resume Summary: {candidate['resume_data'].get('summary', '')}
Candidate Skills: {', '.join(candidate['skills'])}

Rate the keyword match from 0-100 and provide specific feedback.

Return JSON:
{{
  "keyword_match_score": 0-100,
  "matched_keywords": ["..."],
  "missing_keywords": ["..."],
  "feedback": "..."
}}
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                response_format={"type": "json_object"}
            )
            result = json.loads(response.choices[0].message.content)
            return result["keyword_match_score"] / 100.0
        except Exception:
            # Fallback to simple keyword matching
            return self._simple_keyword_match(candidate, job)
    
    def _simple_keyword_match(self, candidate: Dict[str, Any], job: JobRequirement) -> float:
        """Simple keyword matching fallback"""
        candidate_text = f"{candidate['resume_data'].get('summary', '')} {' '.join(candidate['skills'])}".lower()
        job_keywords = f"{job.title} {job.description} {' '.join(job.required_skills)}".lower()
        
        job_words = set(job_keywords.split())
        candidate_words = set(candidate_text.split())
        
        if not job_words:
            return 0.0
        
        match_count = len(job_words.intersection(candidate_words))
        return min(match_count / len(job_words), 1.0)
    
    def _calculate_ats_compatibility(self, candidate: Dict[str, Any]) -> float:
        """Calculate ATS compatibility score"""
        # This would typically use the analyze_resume_ats_compatibility method
        # For now, return a basic score based on resume structure
        resume = candidate["resume_data"].get("resume", {})
        
        score = 0.0
        if resume.get("Name"):
            score += 0.1
        if resume.get("Email"):
            score += 0.1
        if resume.get("Phone"):
            score += 0.1
        if resume.get("Summary"):
            score += 0.2
        if resume.get("Skills"):
            score += 0.2
        if resume.get("WorkExperience"):
            score += 0.2
        if resume.get("Education"):
            score += 0.1
        
        return min(score, 1.0)
    
    def _generate_detailed_feedback(self, candidate: Dict[str, Any], job: JobRequirement, 
                                  skills_match: float, experience_match: float, 
                                  education_match: float, keyword_match: float, 
                                  ats_compatibility: float) -> Dict[str, Any]:
        """Generate detailed feedback for the candidate-job match"""
        prompt = f"""
Generate detailed feedback for a candidate applying to a job position.

Job Details:
- Title: {job.title}
- Required Skills: {', '.join(job.required_skills)}
- Preferred Skills: {', '.join(job.preferred_skills)}
- Experience Required: {job.experience_years} years
- Education: {job.education_level}

Candidate Details:
- Name: {candidate['name']}
- Skills: {', '.join(candidate['skills'])}
- Experience: {candidate['experience_years']} years
- Education: {len(candidate['education'])} degrees

Match Scores:
- Skills Match: {skills_match:.2f}
- Experience Match: {experience_match:.2f}
- Education Match: {education_match:.2f}
- Keyword Match: {keyword_match:.2f}
- ATS Compatibility: {ats_compatibility:.2f}

Provide detailed feedback in JSON format:
{{
  "overall_assessment": "...",
  "strengths": ["..."],
  "areas_for_improvement": ["..."],
  "specific_recommendations": ["..."],
  "fit_score": "excellent/good/fair/poor",
  "next_steps": ["..."]
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
        except Exception:
            # Fallback feedback
            return {
                "overall_assessment": "Basic assessment completed",
                "strengths": ["Resume analyzed successfully"],
                "areas_for_improvement": ["Consider enhancing keyword optimization"],
                "specific_recommendations": ["Review job requirements and align skills"],
                "fit_score": "fair",
                "next_steps": ["Apply and follow up"]
            } 