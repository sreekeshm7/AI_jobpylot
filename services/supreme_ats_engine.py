import re
import hashlib
from typing import Dict, Any, List, Optional
import os
from datetime import datetime
from dataclasses import dataclass
from dotenv import load_dotenv
import openai

load_dotenv()

@dataclass
class SupremeATSConfig:
    """Supreme ATS Configuration - 100% Deterministic"""
    scoring_weights: Dict[str, float] = None
    keyword_boost: float = 2.0
    quantifiable_boost: float = 2.5
    action_verb_boost: float = 1.8
    experience_boost: float = 1.9
    education_boost: float = 1.5
    leadership_boost: float = 2.2

    def __post_init__(self):
        if self.scoring_weights is None:
            self.scoring_weights = {
                "summary": 0.30,
                "experience": 0.25,
                "skills": 0.20,
                "education": 0.15,
                "keywords": 0.07,
                "formatting": 0.03
            }

class SupremeATSEngine:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.config = SupremeATSConfig()
        self.cache = {}

        # Deterministic industry keywords
        self.industry_keywords = {
            "technology": [
                "python", "javascript", "java", "react", "angular", "vue", "node.js",
                "sql", "mongodb", "aws", "azure", "docker", "kubernetes", "git",
                "agile", "scrum", "devops", "ci/cd", "api", "rest", "graphql",
                "machine learning", "ai", "data science", "analytics", "cloud",
                "microservices", "serverless", "blockchain", "cybersecurity"
            ]
        }

        # Deterministic action verbs with predefined scores
        self.action_verbs = {
            "leadership": ["led", "managed", "directed", "oversaw", "supervised", "coordinated", "orchestrated"],
            "achievement": ["achieved", "delivered", "implemented", "launched", "developed", "created", "built"],
            "improvement": ["improved", "optimized", "enhanced", "streamlined", "reduced", "increased", "boosted"],
            "technical": ["developed", "built", "designed", "architected", "engineered", "programmed", "coded"]
        }

        # Deterministic scoring rules
        self.scoring_rules = {
            "summary_length": {"optimal": (100, 200), "good": (50, 300), "poor": (0, 50)},
            "quantifiable_metrics": {"excellent": 3, "good": 2, "average": 1, "poor": 0},
            "action_verbs": {"excellent": 5, "good": 3, "average": 2, "poor": 0},
            "keyword_density": {"excellent": 0.15, "good": 0.10, "average": 0.05, "poor": 0.02},
            "experience_years": {"excellent": 8, "good": 5, "average": 3, "poor": 1},
            "skills_count": {"excellent": 15, "good": 10, "average": 6, "poor": 3}
        }

    def analyze_resume_supreme(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Supreme ATS analysis with 100% deterministic scoring"""
        
        # Extract resume sections deterministically
        summary_data = self._extract_summary_enhanced(resume_data)
        skills_data = self._extract_skills_enhanced(resume_data)
        experience_data = self._extract_experience_enhanced(resume_data)
        education_data = self._extract_education_enhanced(resume_data)
        
        # Calculate deterministic scores
        summary_score = self._calculate_summary_score_deterministic(summary_data)
        skills_score = self._calculate_skills_score_deterministic(skills_data)
        experience_score = self._calculate_experience_score_deterministic(experience_data)
        education_score = self._calculate_education_score_deterministic(education_data)
        keywords_score = self._calculate_keywords_score_deterministic(resume_data)
        formatting_score = self._calculate_formatting_score_deterministic(resume_data)
        
        # Compile section scores
        section_scores = {
            "summary": summary_score,
            "skills": skills_score,
            "experience": experience_score,
            "education": education_score,
            "keywords": keywords_score,
            "formatting": formatting_score
        }
        
        # Calculate supreme score deterministically
        supreme_score = self._calculate_supreme_score(section_scores)
        
        # Generate deterministic analysis
        detailed_analysis = {
            "summary": self._analyze_summary_deterministic(summary_data, summary_score),
            "skills": self._analyze_skills_deterministic(skills_data, skills_score),
            "experience": self._analyze_experience_deterministic(experience_data, experience_score),
            "education": self._analyze_education_deterministic(education_data, education_score),
            "keywords": self._analyze_keywords_deterministic(resume_data, keywords_score),
            "formatting": self._analyze_formatting_deterministic(resume_data, formatting_score)
        }
        
        # Generate deterministic recommendations
        optimization_recommendations = self._generate_deterministic_recommendations(section_scores)
        
        # Market analysis
        market_analysis = self._analyze_market_fit_deterministic(resume_data)
        
        # Improvement predictions
        improvement_predictions = self._predict_improvement_impact_deterministic(supreme_score)
        
        # Advanced insights
        advanced_insights = self._generate_advanced_insights_deterministic(section_scores)
        
        return {
            "resume_id": hashlib.md5(str(resume_data).encode()).hexdigest()[:8],
            "timestamp": datetime.now().isoformat(),
            "supreme_ats_score": supreme_score,
            "section_scores": section_scores,
            "detailed_analysis": detailed_analysis,
            "optimization_recommendations": optimization_recommendations,
            "market_analysis": market_analysis,
            "improvement_predictions": improvement_predictions,
            "advanced_insights": advanced_insights,
            "deterministic": True
        }

    def _calculate_summary_score_deterministic(self, summary_data: Dict[str, Any]) -> float:
        """Calculate summary score using deterministic rules"""
        text = summary_data.get("text", "").lower()
        length = len(text)
        
        # Length score (0-2 points)
        length_score = 0
        if self.scoring_rules["summary_length"]["optimal"][0] <= length <= self.scoring_rules["summary_length"]["optimal"][1]:
            length_score = 2.0
        elif self.scoring_rules["summary_length"]["good"][0] <= length <= self.scoring_rules["summary_length"]["good"][1]:
            length_score = 1.5
        elif self.scoring_rules["summary_length"]["poor"][0] <= length <= self.scoring_rules["summary_length"]["poor"][1]:
            length_score = 0.5
        else:
            length_score = 1.0
        
        # Quantifiable metrics score (0-3 points)
        metrics_count = summary_data.get("metrics_found", 0)
        metrics_score = 0
        if metrics_count >= self.scoring_rules["quantifiable_metrics"]["excellent"]:
            metrics_score = 3.0
        elif metrics_count >= self.scoring_rules["quantifiable_metrics"]["good"]:
            metrics_score = 2.0
        elif metrics_count >= self.scoring_rules["quantifiable_metrics"]["average"]:
            metrics_score = 1.0
        else:
            metrics_score = 0.0
        
        # Action verbs score (0-2 points)
        action_verbs_count = summary_data.get("action_verbs", 0)
        verbs_score = 0
        if action_verbs_count >= self.scoring_rules["action_verbs"]["excellent"]:
            verbs_score = 2.0
        elif action_verbs_count >= self.scoring_rules["action_verbs"]["good"]:
            verbs_score = 1.5
        elif action_verbs_count >= self.scoring_rules["action_verbs"]["average"]:
            verbs_score = 1.0
        else:
            verbs_score = 0.0
        
        # Keyword density score (0-2 points)
        keyword_density = summary_data.get("keyword_density", 0)
        keyword_score = 0
        if keyword_density >= self.scoring_rules["keyword_density"]["excellent"]:
            keyword_score = 2.0
        elif keyword_density >= self.scoring_rules["keyword_density"]["good"]:
            keyword_score = 1.5
        elif keyword_density >= self.scoring_rules["keyword_density"]["average"]:
            keyword_score = 1.0
        else:
            keyword_score = 0.0
        
        # Readability score (0-1 point)
        avg_sentence_length = summary_data.get("avg_sentence_length", 20)
        readability_score = 1.0 if 15 <= avg_sentence_length <= 25 else 0.5
        
        total_score = length_score + metrics_score + verbs_score + keyword_score + readability_score
        return round(min(10.0, total_score), 2)

    def _calculate_skills_score_deterministic(self, skills_data: Dict[str, Any]) -> float:
        """Calculate skills score using deterministic rules"""
        all_skills = skills_data.get("all_skills", [])
        technical_count = skills_data.get("technical_count", 0)
        soft_count = skills_data.get("soft_count", 0)
        
        # Total skills score (0-4 points)
        total_skills = len(all_skills)
        skills_count_score = 0
        if total_skills >= self.scoring_rules["skills_count"]["excellent"]:
            skills_count_score = 4.0
        elif total_skills >= self.scoring_rules["skills_count"]["good"]:
            skills_count_score = 3.0
        elif total_skills >= self.scoring_rules["skills_count"]["average"]:
            skills_count_score = 2.0
        else:
            skills_count_score = 1.0
        
        # Technical skills balance (0-3 points)
        technical_ratio = technical_count / max(total_skills, 1)
        technical_score = 3.0 if technical_ratio >= 0.6 else 2.0 if technical_ratio >= 0.4 else 1.0
        
        # Soft skills balance (0-2 points)
        soft_ratio = soft_count / max(total_skills, 1)
        soft_score = 2.0 if soft_ratio >= 0.2 else 1.0 if soft_ratio >= 0.1 else 0.5
        
        # Industry relevance (0-1 point)
        relevant_keywords = sum(1 for skill in all_skills if skill.lower() in [kw.lower() for kw in self.industry_keywords["technology"]])
        relevance_score = 1.0 if relevant_keywords >= 3 else 0.5 if relevant_keywords >= 1 else 0.0
        
        total_score = skills_count_score + technical_score + soft_score + relevance_score
        return round(min(10.0, total_score), 2)

    def _calculate_experience_score_deterministic(self, experience_data: List[Dict]) -> float:
        """Calculate experience score using deterministic rules"""
        if not experience_data:
            return 0.0
        
        total_years = 0
        leadership_roles = 0
        quantifiable_achievements = 0
        
        for job in experience_data:
            # Extract years from duration
            duration = job.get("Duration", "0 years")
            years = self._extract_years_from_duration(duration)
            total_years += years
            
            # Count leadership indicators
            title = job.get("JobTitle", "").lower()
            if any(word in title for word in ["senior", "lead", "manager", "director", "head"]):
                leadership_roles += 1
            
            # Count quantifiable achievements
            responsibilities = job.get("Responsibilities", [])
            for resp in responsibilities:
                if any(char.isdigit() for char in resp):
                    quantifiable_achievements += 1
        
        # Years of experience score (0-4 points)
        years_score = 0
        if total_years >= self.scoring_rules["experience_years"]["excellent"]:
            years_score = 4.0
        elif total_years >= self.scoring_rules["experience_years"]["good"]:
            years_score = 3.0
        elif total_years >= self.scoring_rules["experience_years"]["average"]:
            years_score = 2.0
        else:
            years_score = 1.0
        
        # Leadership score (0-3 points)
        leadership_score = min(3.0, leadership_roles * 1.5)
        
        # Quantifiable achievements score (0-3 points)
        achievements_score = min(3.0, quantifiable_achievements * 0.5)
        
        total_score = years_score + leadership_score + achievements_score
        return round(min(10.0, total_score), 2)

    def _calculate_education_score_deterministic(self, education_data: List[Dict]) -> float:
        """Calculate education score using deterministic rules"""
        if not education_data:
            return 0.0
        
        highest_degree = education_data[0]
        degree = highest_degree.get("Degree", "").lower()
        
        # Degree level score (0-6 points)
        degree_score = 0
        if "phd" in degree or "doctorate" in degree:
            degree_score = 6.0
        elif "master" in degree:
            degree_score = 5.0
        elif "bachelor" in degree:
            degree_score = 4.0
        elif "associate" in degree:
            degree_score = 3.0
        elif "diploma" in degree or "certificate" in degree:
            degree_score = 2.0
        else:
            degree_score = 1.0
        
        # Institution quality (0-2 points)
        institution = highest_degree.get("Institution", "").lower()
        institution_score = 2.0 if any(word in institution for word in ["university", "college", "institute"]) else 1.0
        
        # Recency score (0-2 points)
        end_year = highest_degree.get("EndYear", "0")
        try:
            year = int(end_year)
            current_year = datetime.now().year
            years_since = current_year - year
            recency_score = 2.0 if years_since <= 5 else 1.5 if years_since <= 10 else 1.0
        except:
            recency_score = 1.0
        
        total_score = degree_score + institution_score + recency_score
        return round(min(10.0, total_score), 2)

    def _calculate_keywords_score_deterministic(self, resume_data: Dict[str, Any]) -> float:
        """Calculate keywords score using deterministic rules"""
        all_text = self._extract_all_text(resume_data).lower()
        found_keywords = []
        
        for keyword in self.industry_keywords["technology"]:
            if keyword.lower() in all_text:
                found_keywords.append(keyword)
        
        keyword_density = len(found_keywords) / max(len(all_text.split()), 1)
        
        # Keyword density score (0-5 points)
        density_score = 0
        if keyword_density >= self.scoring_rules["keyword_density"]["excellent"]:
            density_score = 5.0
        elif keyword_density >= self.scoring_rules["keyword_density"]["good"]:
            density_score = 4.0
        elif keyword_density >= self.scoring_rules["keyword_density"]["average"]:
            density_score = 3.0
        else:
            density_score = 1.0
        
        # Keyword variety score (0-5 points)
        variety_score = min(5.0, len(found_keywords) * 0.5)
        
        total_score = density_score + variety_score
        return round(min(10.0, total_score), 2)

    def _calculate_formatting_score_deterministic(self, resume_data: Dict[str, Any]) -> float:
        """Calculate formatting score using deterministic rules"""
        # Basic formatting checks
        resume = resume_data.get("resume", {})
        
        # Required sections (0-4 points)
        required_sections = ["Name", "Email", "Summary", "Skills", "WorkExperience", "Education"]
        present_sections = sum(1 for section in required_sections if section in resume)
        sections_score = (present_sections / len(required_sections)) * 4.0
        
        # Contact information (0-2 points)
        contact_score = 0
        if resume.get("Name") and resume.get("Email"):
            contact_score = 2.0
        elif resume.get("Name") or resume.get("Email"):
            contact_score = 1.0
        
        # Structure quality (0-2 points)
        structure_score = 2.0 if len(resume) >= 5 else 1.0
        
        # Content length (0-2 points)
        all_text = self._extract_all_text(resume_data)
        content_score = 2.0 if len(all_text) >= 500 else 1.0 if len(all_text) >= 200 else 0.5
        
        total_score = sections_score + contact_score + structure_score + content_score
        return round(min(10.0, total_score), 2)

    def _extract_years_from_duration(self, duration: str) -> int:
        """Extract years from duration string deterministically"""
        duration = duration.lower()
        if "year" in duration:
            numbers = re.findall(r'\d+', duration)
            return int(numbers[0]) if numbers else 0
        elif "month" in duration:
            numbers = re.findall(r'\d+', duration)
            return int(numbers[0]) // 12 if numbers else 0
        return 0

    def _analyze_summary_deterministic(self, summary_data: Dict[str, Any], score: float) -> Dict[str, Any]:
        """Generate deterministic summary analysis"""
        text = summary_data.get("text", "")
        
        strengths = []
        weaknesses = []
        
        if summary_data.get("metrics_found", 0) >= 2:
            strengths.append("Quantifiable achievements present")
        else:
            weaknesses.append("Lacks quantifiable achievements")
        
        if summary_data.get("action_verbs", 0) >= 3:
            strengths.append("Strong action verbs used")
        else:
            weaknesses.append("Needs more action verbs")
        
        if len(text) >= 100:
            strengths.append("Appropriate length")
        else:
            weaknesses.append("Too short")
        
        if summary_data.get("keyword_density", 0) >= 0.10:
            strengths.append("Good keyword density")
        else:
            weaknesses.append("Low keyword density")
        
        return {
            "score": score,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "analysis": f"Summary scored {score}/10 based on length, metrics, action verbs, and keywords"
        }

    def _analyze_skills_deterministic(self, skills_data: Dict[str, Any], score: float) -> Dict[str, Any]:
        """Generate deterministic skills analysis"""
        all_skills = skills_data.get("all_skills", [])
        technical_count = skills_data.get("technical_count", 0)
        soft_count = skills_data.get("soft_count", 0)
        
        strengths = []
        weaknesses = []
        
        if len(all_skills) >= 10:
            strengths.append("Comprehensive skill set")
        else:
            weaknesses.append("Limited skill set")
        
        if technical_count >= 6:
            strengths.append("Strong technical skills")
        else:
            weaknesses.append("Needs more technical skills")
        
        if soft_count >= 3:
            strengths.append("Good soft skills")
        else:
            weaknesses.append("Could use more soft skills")
        
        return {
            "score": score,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "analysis": f"Skills scored {score}/10 based on quantity, technical/soft balance, and relevance"
        }

    def _analyze_experience_deterministic(self, experience_data: List[Dict], score: float) -> Dict[str, Any]:
        """Generate deterministic experience analysis"""
        strengths = []
        weaknesses = []
        
        if experience_data:
            total_years = sum(self._extract_years_from_duration(job.get("Duration", "0")) for job in experience_data)
            
            if total_years >= 5:
                strengths.append("Significant experience")
            else:
                weaknesses.append("Limited experience")
            
            leadership_count = sum(1 for job in experience_data if any(word in job.get("JobTitle", "").lower() for word in ["senior", "lead", "manager"]))
            if leadership_count > 0:
                strengths.append("Leadership experience")
            else:
                weaknesses.append("No leadership roles")
        else:
            weaknesses.append("No work experience")
        
        return {
            "score": score,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "analysis": f"Experience scored {score}/10 based on years, leadership, and achievements"
        }

    def _analyze_education_deterministic(self, education_data: List[Dict], score: float) -> Dict[str, Any]:
        """Generate deterministic education analysis"""
        strengths = []
        weaknesses = []
        
        if education_data:
            degree = education_data[0].get("Degree", "").lower()
            if "bachelor" in degree or "master" in degree or "phd" in degree:
                strengths.append("Relevant degree level")
            else:
                weaknesses.append("Could benefit from higher education")
        else:
            weaknesses.append("No education listed")
        
        return {
            "score": score,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "analysis": f"Education scored {score}/10 based on degree level and institution"
        }

    def _analyze_keywords_deterministic(self, resume_data: Dict[str, Any], score: float) -> Dict[str, Any]:
        """Generate deterministic keywords analysis"""
        all_text = self._extract_all_text(resume_data).lower()
        found_keywords = [kw for kw in self.industry_keywords["technology"] if kw.lower() in all_text]
        
        strengths = []
        weaknesses = []
        
        if len(found_keywords) >= 5:
            strengths.append("Good keyword coverage")
        else:
            weaknesses.append("Limited keyword coverage")
        
        return {
            "score": score,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "analysis": f"Keywords scored {score}/10 based on industry relevance and density"
        }

    def _analyze_formatting_deterministic(self, resume_data: Dict[str, Any], score: float) -> Dict[str, Any]:
        """Generate deterministic formatting analysis"""
        resume = resume_data.get("resume", {})
        
        strengths = []
        weaknesses = []
        
        required_sections = ["Name", "Email", "Summary", "Skills", "WorkExperience", "Education"]
        present_sections = [section for section in required_sections if section in resume]
        
        if len(present_sections) >= 5:
            strengths.append("Complete structure")
        else:
            weaknesses.append("Missing sections")
        
        if resume.get("Name") and resume.get("Email"):
            strengths.append("Contact information present")
        else:
            weaknesses.append("Missing contact information")
        
        return {
            "score": score,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "analysis": f"Formatting scored {score}/10 based on structure and completeness"
        }

    def _generate_deterministic_recommendations(self, section_scores: Dict[str, float]) -> List[str]:
        """Generate deterministic recommendations based on scores"""
        recommendations = []
        
        if section_scores["summary"] < 7.0:
            recommendations.append("Enhance summary with quantifiable achievements and action verbs")
        
        if section_scores["skills"] < 7.0:
            recommendations.append("Add more relevant technical and soft skills")
        
        if section_scores["experience"] < 7.0:
            recommendations.append("Include more quantifiable achievements and leadership examples")
        
        if section_scores["keywords"] < 7.0:
            recommendations.append("Incorporate more industry-specific keywords naturally")
        
        if section_scores["formatting"] < 7.0:
            recommendations.append("Ensure all required sections are present and well-structured")
        
        if len(recommendations) == 0:
            recommendations.append("Resume is well-optimized. Focus on continuous improvement")
        
        return recommendations

    def _analyze_market_fit_deterministic(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate deterministic market fit analysis"""
        all_text = self._extract_all_text(resume_data).lower()
        found_keywords = [kw for kw in self.industry_keywords["technology"] if kw.lower() in all_text]
        missing_keywords = [kw for kw in self.industry_keywords["technology"] if kw.lower() not in all_text]
        
        keyword_match_percentage = (len(found_keywords) / len(self.industry_keywords["technology"])) * 100
        
        if keyword_match_percentage >= 30:
            market_competitiveness = "high"
        elif keyword_match_percentage >= 15:
            market_competitiveness = "medium"
        else:
            market_competitiveness = "low"
        
        return {
            "keyword_match_percentage": round(keyword_match_percentage, 1),
            "found_keywords": found_keywords,
            "missing_keywords": missing_keywords[:10],  # Limit to top 10
            "market_competitiveness": market_competitiveness
        }

    def _predict_improvement_impact_deterministic(self, current_score: float) -> Dict[str, Any]:
        """Generate deterministic improvement predictions"""
        if current_score >= 9.0:
            return {
                "quick_wins": {"score_increase": 0.2, "timeline": "1 week", "effort": "low", "actions": ["Minor tweaks"]},
                "strategic_improvements": {"score_increase": 0.5, "timeline": "1 month", "effort": "medium", "actions": ["Content refinement"]},
                "supreme_optimization": {"score_increase": 0.8, "timeline": "2-3 months", "effort": "high", "actions": ["Complete overhaul"]}
            }
        elif current_score >= 7.0:
            return {
                "quick_wins": {"score_increase": 0.5, "timeline": "1 week", "effort": "low", "actions": ["Add keywords"]},
                "strategic_improvements": {"score_increase": 1.0, "timeline": "1 month", "effort": "medium", "actions": ["Enhance achievements"]},
                "supreme_optimization": {"score_increase": 1.5, "timeline": "2-3 months", "effort": "high", "actions": ["Major improvements"]}
            }
        else:
            return {
                "quick_wins": {"score_increase": 1.0, "timeline": "1 week", "effort": "low", "actions": ["Basic fixes"]},
                "strategic_improvements": {"score_increase": 2.0, "timeline": "1 month", "effort": "medium", "actions": ["Content enhancement"]},
                "supreme_optimization": {"score_increase": 3.0, "timeline": "2-3 months", "effort": "high", "actions": ["Complete transformation"]}
            }

    def _generate_advanced_insights_deterministic(self, section_scores: Dict[str, float]) -> Dict[str, Any]:
        """Generate deterministic advanced insights"""
        avg_score = sum(section_scores.values()) / len(section_scores)
        
        if avg_score >= 8.5:
            progression = "excellent"
            potential = "high"
        elif avg_score >= 7.0:
            progression = "good"
            potential = "medium"
        else:
            progression = "needs_improvement"
            potential = "low"
        
        skill_gaps = []
        if section_scores["skills"] < 7.0:
            skill_gaps.append("Technical skills")
        if section_scores["experience"] < 7.0:
            skill_gaps.append("Leadership experience")
        if section_scores["keywords"] < 7.0:
            skill_gaps.append("Industry keywords")
        
        return {
            "career_progression": {"progression": progression, "confidence": "high"},
            "skill_gaps": skill_gaps,
            "market_positioning": {"position": "competitive" if avg_score >= 7.0 else "needs_work"},
            "leadership_potential": {"potential": potential, "indicators": "present" if section_scores["experience"] >= 7.0 else "limited"},
            "optimization_opportunities": {"count": len([s for s in section_scores.values() if s < 7.0]), "priority": "high" if avg_score < 7.0 else "medium"}
        }

    # Keep existing extraction methods for compatibility
    def _extract_summary_enhanced(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract and analyze summary with deterministic metrics"""
        summary = resume_data.get("resume", {}).get("Summary", "")
        
        # Calculate deterministic metrics
        words = summary.split()
        sentences = re.split(r'[.!?]+', summary)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Count quantifiable metrics (numbers + %)
        metrics_pattern = r'\d+%|\d+\s*(?:years?|months?|people|users|customers|projects|applications|systems|teams|companies|dollars?|\$|percent|%)'
        metrics_found = len(re.findall(metrics_pattern, summary, re.IGNORECASE))
        
        # Count action verbs
        action_verbs_count = 0
        for category, verbs in self.action_verbs.items():
            for verb in verbs:
                action_verbs_count += summary.lower().count(verb)
        
        # Calculate keyword density
        keyword_count = 0
        for keyword in self.industry_keywords["technology"]:
            keyword_count += summary.lower().count(keyword.lower())
        
        keyword_density = keyword_count / max(len(words), 1)
        
        # Calculate average sentence length
        avg_sentence_length = sum(len(s.split()) for s in sentences) / max(len(sentences), 1)
        
        return {
            "text": summary,
            "length": len(summary),
            "metrics_found": metrics_found,
            "action_verbs": action_verbs_count,
            "keyword_density": keyword_density,
            "avg_sentence_length": avg_sentence_length,
            "impact_score": metrics_found * 2 + action_verbs_count * 0.5
        }

    def _extract_skills_enhanced(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract skills with deterministic categorization"""
        skills = resume_data.get("resume", {}).get("Skills", {})
        
        all_skills = []
        technical_count = 0
        soft_count = 0
        
        # Extract all skills
        for category, skill_list in skills.items():
            if isinstance(skill_list, list):
                all_skills.extend(skill_list)
        
        # Categorize skills deterministically
        technical_keywords = ["python", "java", "javascript", "react", "sql", "aws", "docker", "git", "api", "html", "css", "node", "angular", "vue", "mongodb", "postgresql", "mysql", "redis", "kubernetes", "jenkins", "agile", "scrum", "devops", "machine learning", "ai", "data science", "analytics", "cloud", "microservices", "serverless", "blockchain", "cybersecurity"]
        
        for skill in all_skills:
            if skill.lower() in technical_keywords:
                technical_count += 1
            else:
                soft_count += 1
        
        return {
            "all_skills": all_skills,
            "technical_count": technical_count,
            "soft_count": soft_count
        }

    def _extract_experience_enhanced(self, resume_data: Dict[str, Any]) -> List[Dict]:
        """Extract work experience"""
        return resume_data.get("resume", {}).get("WorkExperience", [])

    def _extract_education_enhanced(self, resume_data: Dict[str, Any]) -> List[Dict]:
        """Extract education"""
        return resume_data.get("resume", {}).get("Education", [])

    def _extract_all_text(self, resume_data: Dict[str, Any]) -> str:
        """Extract all text from resume deterministically"""
        resume = resume_data.get("resume", {})
        text_parts = []
        
        # Add basic info
        text_parts.extend([
            resume.get("Name", ""),
            resume.get("Email", ""),
            resume.get("Phone", ""),
            resume.get("Summary", "")
        ])
        
        # Add skills
        skills = resume.get("Skills", {})
        for category, skill_list in skills.items():
            if isinstance(skill_list, list):
                text_parts.extend(skill_list)
        
        # Add experience
        for job in resume.get("WorkExperience", []):
            text_parts.extend([
                job.get("JobTitle", ""),
                job.get("Company", ""),
                job.get("Duration", ""),
                job.get("Location", "")
            ])
            text_parts.extend(job.get("Responsibilities", []))
            text_parts.extend(job.get("TechStack", []))
        
        # Add education
        for edu in resume.get("Education", []):
            text_parts.extend([
                edu.get("Degree", ""),
                edu.get("Institution", ""),
                edu.get("Location", ""),
                edu.get("StartYear", ""),
                edu.get("EndYear", "")
            ])
        
        return " ".join(text_parts)

    def _calculate_supreme_score(self, section_scores: Dict[str, float]) -> float:
        """Calculate supreme weighted score deterministically"""
        total_score = 0
        total_weight = 0
        
        for section, score in section_scores.items():
            base_weight = self.config.scoring_weights.get(section, 0.1)
            
            # Apply deterministic boost factors
            boost = 1.0
            if section == "summary" and score >= 8:
                boost = self.config.leadership_boost
            elif section == "experience" and score >= 7:
                boost = self.config.experience_boost
            elif section == "skills" and score >= 8:
                boost = self.config.action_verb_boost
            elif section == "keywords" and score >= 7:
                boost = self.config.keyword_boost
            
            total_score += score * base_weight * boost
            total_weight += base_weight * boost
        
        supreme_score = total_score / total_weight if total_weight > 0 else 0
        
        # Apply final deterministic adjustment
        supreme_score = min(10, supreme_score * 1.15)  # 15% boost for supreme optimization
        
        return round(supreme_score, 2)

    # Keep AI-based methods for optional enhanced analysis (clearly marked as non-deterministic)
    def _analyze_summary_supreme(self, summary_data: Dict[str, Any]) -> Dict[str, Any]:
        """AI-powered summary analysis (non-deterministic, optional)"""
        # This method is kept for optional AI enhancement but is not used in core scoring
        # Users can call this separately if they want AI-generated insights
        pass 