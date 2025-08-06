import openai
import json
import re
from typing import Dict, Any, List, Optional, Tuple
import os
from datetime import datetime
from dataclasses import dataclass
from dotenv import load_dotenv
import hashlib

load_dotenv()

@dataclass
class ATSConfig:
    """Advanced ATS Configuration"""
    scoring_weights: Dict[str, float] = None
    keyword_boost: float = 1.5
    quantifiable_boost: float = 2.0
    action_verb_boost: float = 1.3
    experience_boost: float = 1.4
    education_boost: float = 1.2
    
    def __post_init__(self):
        if self.scoring_weights is None:
            self.scoring_weights = {
                "summary": 0.25,
                "skills": 0.20,
                "experience": 0.25,
                "education": 0.15,
                "keywords": 0.10,
                "formatting": 0.05
            }

class AdvancedATSEngine:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.config = ATSConfig()
        self.cache = {}
        
    def _get_cache_key(self, data: str) -> str:
        """Generate cache key for data"""
        return hashlib.md5(data.encode()).hexdigest()
    
    def _get_cached_result(self, key: str) -> Optional[Dict]:
        """Get cached result if available"""
        return self.cache.get(key)
    
    def _cache_result(self, key: str, result: Dict):
        """Cache result for future use"""
        self.cache[key] = result

    def analyze_resume_comprehensive(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Comprehensive resume analysis with advanced ATS optimization"""
        
        cache_key = self._get_cache_key(json.dumps(resume_data, sort_keys=True))
        cached = self._get_cached_result(cache_key)
        if cached:
            return cached
        
        # Extract all sections
        summary = self._extract_summary(resume_data)
        skills = self._extract_skills(resume_data)
        experience = self._extract_experience(resume_data)
        education = self._extract_education(resume_data)
        
        # Advanced analysis
        summary_analysis = self._analyze_summary_advanced(summary)
        skills_analysis = self._analyze_skills_advanced(skills)
        experience_analysis = self._analyze_experience_advanced(experience)
        education_analysis = self._analyze_education_advanced(education)
        keyword_analysis = self._analyze_keywords_advanced(resume_data)
        formatting_analysis = self._analyze_formatting_advanced(resume_data)
        
        # Calculate weighted score
        overall_score = self._calculate_weighted_score({
            "summary": summary_analysis["score"],
            "skills": skills_analysis["score"],
            "experience": experience_analysis["score"],
            "education": education_analysis["score"],
            "keywords": keyword_analysis["score"],
            "formatting": formatting_analysis["score"]
        })
        
        # Generate optimization recommendations
        recommendations = self._generate_optimization_recommendations({
            "summary": summary_analysis,
            "skills": skills_analysis,
            "experience": experience_analysis,
            "education": education_analysis,
            "keywords": keyword_analysis,
            "formatting": formatting_analysis
        })
        
        result = {
            "overall_ats_score": overall_score,
            "section_scores": {
                "summary": summary_analysis["score"],
                "skills": skills_analysis["score"],
                "experience": experience_analysis["score"],
                "education": education_analysis["score"],
                "keywords": keyword_analysis["score"],
                "formatting": formatting_analysis["score"]
            },
            "detailed_analysis": {
                "summary": summary_analysis,
                "skills": skills_analysis,
                "experience": experience_analysis,
                "education": education_analysis,
                "keywords": keyword_analysis,
                "formatting": formatting_analysis
            },
            "optimization_recommendations": recommendations,
            "ats_compatibility_score": self._calculate_ats_compatibility(resume_data),
            "keyword_match_score": keyword_analysis["keyword_match_percentage"],
            "quantifiable_achievements": experience_analysis["quantifiable_count"],
            "action_verbs_used": experience_analysis["action_verbs_count"],
            "missing_keywords": keyword_analysis["missing_keywords"],
            "suggested_improvements": self._generate_suggested_improvements(resume_data)
        }
        
        self._cache_result(cache_key, result)
        return result

    def _extract_summary(self, resume_data: Dict[str, Any]) -> str:
        """Extract summary with multiple fallbacks"""
        summary = (
            resume_data.get("Summary")
            or resume_data.get("summary")
            or resume_data.get("resume", {}).get("Summary")
            or resume_data.get("resume", {}).get("summary")
            or ""
        )
        return summary.strip() if summary else ""

    def _extract_skills(self, resume_data: Dict[str, Any]) -> List[str]:
        """Extract all skills from resume"""
        skills = []
        skills_section = resume_data.get("Skills", {})
        
        if isinstance(skills_section, dict):
            for category in ["TechStack", "Tools", "soft_skills", "Languages", "Others"]:
                category_skills = skills_section.get(category, [])
                if isinstance(category_skills, list):
                    skills.extend(category_skills)
        
        return [skill.strip() for skill in skills if skill.strip()]

    def _extract_experience(self, resume_data: Dict[str, Any]) -> List[Dict]:
        """Extract work experience"""
        experience = resume_data.get("WorkExperience", [])
        if not isinstance(experience, list):
            return []
        return experience

    def _extract_education(self, resume_data: Dict[str, Any]) -> List[Dict]:
        """Extract education information"""
        education = resume_data.get("Education", [])
        if not isinstance(education, list):
            return []
        return education

    def _analyze_summary_advanced(self, summary: str) -> Dict[str, Any]:
        """Advanced summary analysis with detailed scoring"""
        
        if not summary:
            return {
                "score": 0,
                "strengths": [],
                "weaknesses": ["No summary provided"],
                "improved_versions": [],
                "analysis": "Missing summary section"
            }
        
        prompt = f"""
You are an expert ATS (Applicant Tracking System) evaluator with deep knowledge of resume optimization. Analyze this professional summary with extreme precision.

SUMMARY TO ANALYZE:
"{summary}"

EVALUATION CRITERIA (0-10 scale):
- **0-2**: No summary, completely generic, or irrelevant content
- **3-4**: Basic summary with minimal relevant information
- **5-6**: Good summary with relevant skills and experience
- **7-8**: Strong summary with specific achievements and keywords
- **9-10**: Excellent summary with quantifiable results, strong action verbs, perfect ATS optimization

DETAILED ANALYSIS REQUIREMENTS:
1. Count quantifiable achievements (numbers, percentages, metrics)
2. Identify strong action verbs used
3. Check for industry-specific keywords
4. Evaluate clarity and impact
5. Assess ATS compatibility

Respond in this EXACT JSON format:
{{
  "score": <number 0-10>,
  "score_explanation": "<detailed explanation of scoring>",
  "strengths": ["<list of specific strengths>"],
  "weaknesses": ["<list of specific weaknesses>"],
  "quantifiable_achievements": <count of numbers/metrics>,
  "action_verbs_found": ["<list of action verbs>"],
  "keywords_present": ["<list of relevant keywords>"],
  "missing_elements": ["<list of missing important elements>"],
  "improved_versions": [
    {{
      "version": "<first excellent ATS-optimized version with quantifiable achievements>",
      "score": 9,
      "focus": "achievements and metrics",
      "explanation": "<why this version is excellent>"
    }},
    {{
      "version": "<second excellent version with strong action verbs and leadership>",
      "score": 9,
      "focus": "leadership and impact",
      "explanation": "<why this version is excellent>"
    }},
    {{
      "version": "<third excellent version emphasizing technical expertise>",
      "score": 10,
      "focus": "technical skills and results",
      "explanation": "<why this version is excellent>"
    }},
    {{
      "version": "<fourth excellent version with comprehensive optimization>",
      "score": 10,
      "focus": "comprehensive ATS optimization",
      "explanation": "<why this version is excellent>"
    }}
  ],
  "ats_optimization_tips": ["<specific tips for ATS optimization>"]
}}

IMPORTANT: Be extremely precise and thorough. Every improved version must be excellent (9-10 score) with quantifiable achievements, strong action verbs, and perfect ATS optimization.
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            result = json.loads(response.choices[0].message.content)
            
            # Validate and normalize score
            result["score"] = max(0, min(10, float(result.get("score", 0))))
            
            return result
        except Exception as e:
            return {
                "score": 0 if not summary else 5,
                "score_explanation": f"Analysis failed: {str(e)}",
                "strengths": [],
                "weaknesses": ["Analysis error occurred"],
                "improved_versions": []
            }

    def _analyze_skills_advanced(self, skills: List[str]) -> Dict[str, Any]:
        """Advanced skills analysis"""
        
        if not skills:
            return {
                "score": 0,
                "analysis": "No skills found",
                "recommendations": ["Add relevant technical and soft skills"]
            }
        
        # Analyze skills for relevance, specificity, and market demand
        technical_skills = [s for s in skills if self._is_technical_skill(s)]
        soft_skills = [s for s in skills if not self._is_technical_skill(s)]
        
        score = min(10, len(technical_skills) * 2 + len(soft_skills))
        
        return {
            "score": score,
            "technical_skills_count": len(technical_skills),
            "soft_skills_count": len(soft_skills),
            "technical_skills": technical_skills,
            "soft_skills": soft_skills,
            "analysis": f"Found {len(technical_skills)} technical and {len(soft_skills)} soft skills",
            "recommendations": self._generate_skill_recommendations(technical_skills, soft_skills)
        }

    def _is_technical_skill(self, skill: str) -> bool:
        """Determine if a skill is technical"""
        technical_keywords = [
            "python", "java", "javascript", "react", "angular", "vue", "node", "sql",
            "aws", "azure", "docker", "kubernetes", "git", "agile", "scrum",
            "machine learning", "ai", "data science", "analytics", "devops"
        ]
        return any(keyword in skill.lower() for keyword in technical_keywords)

    def _analyze_experience_advanced(self, experience: List[Dict]) -> Dict[str, Any]:
        """Advanced experience analysis"""
        
        if not experience:
            return {
                "score": 0,
                "analysis": "No work experience found",
                "recommendations": ["Add relevant work experience"]
            }
        
        total_years = 0
        quantifiable_count = 0
        action_verbs_count = 0
        strong_achievements = []
        
        for job in experience:
            # Estimate years from duration
            duration = job.get("Duration", "")
            years = self._extract_years_from_duration(duration)
            total_years += years
            
            # Analyze responsibilities for quantifiable achievements
            responsibilities = job.get("Responsibilities", [])
            for resp in responsibilities:
                if self._has_quantifiable_metrics(resp):
                    quantifiable_count += 1
                if self._has_action_verb(resp):
                    action_verbs_count += 1
                if self._is_strong_achievement(resp):
                    strong_achievements.append(resp)
        
        # Calculate score based on experience quality
        score = min(10, total_years * 0.5 + quantifiable_count * 0.3 + action_verbs_count * 0.2)
        
        return {
            "score": score,
            "total_years": total_years,
            "quantifiable_count": quantifiable_count,
            "action_verbs_count": action_verbs_count,
            "strong_achievements": strong_achievements,
            "analysis": f"{total_years} years experience with {quantifiable_count} quantifiable achievements",
            "recommendations": self._generate_experience_recommendations(experience)
        }

    def _extract_years_from_duration(self, duration: str) -> float:
        """Extract years from duration string"""
        if not duration:
            return 0
        
        # Simple extraction - can be enhanced
        years_match = re.search(r'(\d+(?:\.\d+)?)\s*years?', duration.lower())
        if years_match:
            return float(years_match.group(1))
        return 1.0  # Default to 1 year if unclear

    def _has_quantifiable_metrics(self, text: str) -> bool:
        """Check if text contains quantifiable metrics"""
        metrics_patterns = [
            r'\d+%', r'\d+\s*percent', r'\$\d+', r'\d+\s*million',
            r'\d+\s*users', r'\d+\s*customers', r'\d+\s*team members'
        ]
        return any(re.search(pattern, text.lower()) for pattern in metrics_patterns)

    def _has_action_verb(self, text: str) -> bool:
        """Check if text starts with action verb"""
        action_verbs = [
            "developed", "implemented", "created", "designed", "managed", "led",
            "increased", "improved", "reduced", "optimized", "delivered", "achieved"
        ]
        return any(text.lower().startswith(verb) for verb in action_verbs)

    def _is_strong_achievement(self, text: str) -> bool:
        """Check if text represents a strong achievement"""
        return self._has_quantifiable_metrics(text) and self._has_action_verb(text)

    def _analyze_education_advanced(self, education: List[Dict]) -> Dict[str, Any]:
        """Advanced education analysis"""
        
        if not education:
            return {
                "score": 0,
                "analysis": "No education information found",
                "recommendations": ["Add education details"]
            }
        
        highest_degree = self._get_highest_degree(education)
        score = self._calculate_education_score(highest_degree)
        
        return {
            "score": score,
            "highest_degree": highest_degree,
            "institutions": [edu.get("Institution", "") for edu in education],
            "analysis": f"Highest degree: {highest_degree}",
            "recommendations": self._generate_education_recommendations(education)
        }

    def _get_highest_degree(self, education: List[Dict]) -> str:
        """Get highest degree level"""
        degree_levels = {
            "phd": 5, "doctorate": 5, "master": 4, "bachelor": 3,
            "associate": 2, "diploma": 1, "certificate": 1
        }
        
        highest_level = 0
        highest_degree = "Unknown"
        
        for edu in education:
            degree = edu.get("Degree", "").lower()
            for level_name, level_value in degree_levels.items():
                if level_name in degree and level_value > highest_level:
                    highest_level = level_value
                    highest_degree = edu.get("Degree", "")
        
        return highest_degree

    def _calculate_education_score(self, degree: str) -> float:
        """Calculate education score based on degree level"""
        degree_lower = degree.lower()
        if any(word in degree_lower for word in ["phd", "doctorate"]):
            return 10.0
        elif any(word in degree_lower for word in ["master", "mba"]):
            return 8.0
        elif any(word in degree_lower for word in ["bachelor", "bs", "ba"]):
            return 6.0
        elif any(word in degree_lower for word in ["associate", "diploma"]):
            return 4.0
        else:
            return 2.0

    def _analyze_keywords_advanced(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Advanced keyword analysis"""
        
        # Extract all text content
        all_text = self._extract_all_text(resume_data)
        
        # Define relevant keywords for tech industry
        relevant_keywords = [
            "python", "javascript", "java", "react", "angular", "vue", "node.js",
            "sql", "mongodb", "aws", "azure", "docker", "kubernetes", "git",
            "agile", "scrum", "devops", "ci/cd", "api", "rest", "graphql",
            "machine learning", "ai", "data science", "analytics", "cloud",
            "microservices", "serverless", "blockchain", "cybersecurity"
        ]
        
        found_keywords = []
        for keyword in relevant_keywords:
            if keyword.lower() in all_text.lower():
                found_keywords.append(keyword)
        
        keyword_match_percentage = (len(found_keywords) / len(relevant_keywords)) * 100
        score = min(10, keyword_match_percentage / 10)
        
        return {
            "score": score,
            "found_keywords": found_keywords,
            "missing_keywords": [k for k in relevant_keywords if k not in found_keywords],
            "keyword_match_percentage": keyword_match_percentage,
            "analysis": f"Found {len(found_keywords)} relevant keywords",
            "recommendations": self._generate_keyword_recommendations(found_keywords)
        }

    def _extract_all_text(self, resume_data: Dict[str, Any]) -> str:
        """Extract all text content from resume"""
        text_parts = []
        
        # Extract summary
        summary = self._extract_summary(resume_data)
        if summary:
            text_parts.append(summary)
        
        # Extract skills
        skills = self._extract_skills(resume_data)
        text_parts.extend(skills)
        
        # Extract experience
        experience = self._extract_experience(resume_data)
        for job in experience:
            text_parts.append(job.get("JobTitle", ""))
            text_parts.append(job.get("Company", ""))
            text_parts.extend(job.get("Responsibilities", []))
        
        return " ".join(text_parts)

    def _analyze_formatting_advanced(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Advanced formatting analysis"""
        
        # Check for common formatting issues
        issues = []
        score = 10
        
        # Check for required sections
        required_sections = ["Summary", "Skills", "WorkExperience", "Education"]
        for section in required_sections:
            if not resume_data.get(section):
                issues.append(f"Missing {section} section")
                score -= 2
        
        # Check contact information
        contact_info = resume_data.get("resume", {}).get("Name") or resume_data.get("Name")
        if not contact_info:
            issues.append("Missing contact information")
            score -= 1
        
        return {
            "score": max(0, score),
            "issues": issues,
            "analysis": f"Found {len(issues)} formatting issues",
            "recommendations": self._generate_formatting_recommendations(issues)
        }

    def _calculate_weighted_score(self, section_scores: Dict[str, float]) -> float:
        """Calculate weighted overall score"""
        total_score = 0
        total_weight = 0
        
        for section, score in section_scores.items():
            weight = self.config.scoring_weights.get(section, 0.1)
            total_score += score * weight
            total_weight += weight
        
        return total_score / total_weight if total_weight > 0 else 0

    def _calculate_ats_compatibility(self, resume_data: Dict[str, Any]) -> float:
        """Calculate overall ATS compatibility score"""
        
        # Factors that affect ATS compatibility
        factors = {
            "has_summary": 1.0 if self._extract_summary(resume_data) else 0.0,
            "has_skills": 1.0 if self._extract_skills(resume_data) else 0.0,
            "has_experience": 1.0 if self._extract_experience(resume_data) else 0.0,
            "has_education": 1.0 if self._extract_education(resume_data) else 0.0,
            "has_contact": 1.0 if resume_data.get("resume", {}).get("Name") else 0.0,
            "has_keywords": 1.0 if self._analyze_keywords_advanced(resume_data)["found_keywords"] else 0.0
        }
        
        return sum(factors.values()) / len(factors) * 10

    def _generate_optimization_recommendations(self, analyses: Dict[str, Any]) -> List[str]:
        """Generate comprehensive optimization recommendations"""
        recommendations = []
        
        for section, analysis in analyses.items():
            if analysis.get("score", 0) < 7:
                recommendations.extend(analysis.get("recommendations", []))
        
        return list(set(recommendations))  # Remove duplicates

    def _generate_suggested_improvements(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate specific improvement suggestions"""
        
        summary = self._extract_summary(resume_data)
        skills = self._extract_skills(resume_data)
        experience = self._extract_experience(resume_data)
        
        improvements = {
            "summary_improvements": [],
            "skills_improvements": [],
            "experience_improvements": [],
            "general_improvements": []
        }
        
        # Summary improvements
        if not summary:
            improvements["summary_improvements"].append("Add a compelling professional summary")
        elif len(summary) < 100:
            improvements["summary_improvements"].append("Expand summary with more details and achievements")
        
        # Skills improvements
        if len(skills) < 5:
            improvements["skills_improvements"].append("Add more relevant technical and soft skills")
        
        # Experience improvements
        for job in experience:
            responsibilities = job.get("Responsibilities", [])
            if not responsibilities:
                improvements["experience_improvements"].append(f"Add responsibilities for {job.get('JobTitle', 'position')}")
            else:
                quantifiable_count = sum(1 for resp in responsibilities if self._has_quantifiable_metrics(resp))
                if quantifiable_count < len(responsibilities) * 0.5:
                    improvements["experience_improvements"].append("Add more quantifiable achievements to experience")
        
        return improvements

    def _generate_skill_recommendations(self, technical_skills: List[str], soft_skills: List[str]) -> List[str]:
        """Generate skill-specific recommendations"""
        recommendations = []
        
        if len(technical_skills) < 3:
            recommendations.append("Add more technical skills relevant to your target role")
        
        if len(soft_skills) < 2:
            recommendations.append("Include relevant soft skills like leadership, communication, teamwork")
        
        return recommendations

    def _generate_experience_recommendations(self, experience: List[Dict]) -> List[str]:
        """Generate experience-specific recommendations"""
        recommendations = []
        
        if not experience:
            recommendations.append("Add relevant work experience")
            return recommendations
        
        for job in experience:
            responsibilities = job.get("Responsibilities", [])
            if not responsibilities:
                recommendations.append(f"Add detailed responsibilities for {job.get('JobTitle', 'position')}")
            else:
                quantifiable_count = sum(1 for resp in responsibilities if self._has_quantifiable_metrics(resp))
                if quantifiable_count < len(responsibilities) * 0.5:
                    recommendations.append("Add more quantifiable achievements to experience")
        
        return recommendations

    def _generate_education_recommendations(self, education: List[Dict]) -> List[str]:
        """Generate education-specific recommendations"""
        recommendations = []
        
        if not education:
            recommendations.append("Add education information")
            return recommendations
        
        for edu in education:
            if not edu.get("Institution"):
                recommendations.append("Add institution names")
            if not edu.get("Degree"):
                recommendations.append("Add degree information")
        
        return recommendations

    def _generate_keyword_recommendations(self, found_keywords: List[str]) -> List[str]:
        """Generate keyword-specific recommendations"""
        recommendations = []
        
        if len(found_keywords) < 5:
            recommendations.append("Include more industry-relevant keywords")
        
        return recommendations

    def _generate_formatting_recommendations(self, issues: List[str]) -> List[str]:
        """Generate formatting-specific recommendations"""
        recommendations = []
        
        for issue in issues:
            if "Missing" in issue:
                recommendations.append(f"Add {issue.lower().replace('missing ', '')}")
        
        return recommendations 