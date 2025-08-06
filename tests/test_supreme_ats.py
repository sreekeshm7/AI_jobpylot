"""
Tests for the Supreme ATS Engine
"""

import pytest
import json
from unittest.mock import Mock, patch
from services.supreme_ats_engine import SupremeATSEngine, SupremeATSConfig


class TestSupremeATSEngine:
    """Test cases for Supreme ATS Engine"""

    @pytest.fixture
    def engine(self):
        """Create a Supreme ATS Engine instance for testing"""
        return SupremeATSEngine()

    @pytest.fixture
    def sample_resume_data(self):
        """Sample resume data for testing"""
        return {
            "resume": {
                "Name": "John Doe",
                "Email": "john.doe@email.com",
                "Phone": "+1-555-0123",
                "Summary": "Experienced software developer with 5 years of experience in Python and web development. Led development of 3 major applications and improved team productivity by 25%.",
                "Skills": {
                    "TechStack": ["Python", "Django", "React", "JavaScript", "SQL"],
                    "Tools": ["Git", "Docker", "AWS"],
                    "soft_skills": ["Leadership", "Communication", "Problem Solving"]
                },
                "WorkExperience": [
                    {
                        "JobTitle": "Senior Software Developer",
                        "Company": "Tech Corp",
                        "Duration": "3 years",
                        "Location": "San Francisco, CA",
                        "Responsibilities": [
                            "Developed and maintained 5 web applications using Python and React",
                            "Led a team of 4 developers and improved project delivery time by 30%",
                            "Implemented CI/CD pipeline that reduced deployment time by 50%"
                        ],
                        "TechStack": ["Python", "Django", "React", "PostgreSQL", "AWS"]
                    }
                ],
                "Education": [
                    {
                        "Degree": "Bachelor of Science in Computer Science",
                        "Institution": "University of Technology",
                        "Location": "Boston, MA",
                        "StartYear": "2015",
                        "EndYear": "2019"
                    }
                ]
            }
        }

    def test_engine_initialization(self, engine):
        """Test Supreme ATS Engine initialization"""
        assert engine is not None
        assert hasattr(engine, 'config')
        assert hasattr(engine, 'cache')
        assert hasattr(engine, 'industry_keywords')
        assert hasattr(engine, 'action_verbs')

    def test_config_default_values(self, engine):
        """Test default configuration values"""
        config = engine.config
        assert config.keyword_boost == 2.0
        assert config.quantifiable_boost == 2.5
        assert config.action_verb_boost == 1.8
        assert config.experience_boost == 1.9
        assert config.education_boost == 1.5
        assert config.leadership_boost == 2.2

    def test_scoring_weights(self, engine):
        """Test scoring weights configuration"""
        weights = engine.config.scoring_weights
        assert weights["summary"] == 0.30
        assert weights["experience"] == 0.25
        assert weights["skills"] == 0.20
        assert weights["education"] == 0.15
        assert weights["keywords"] == 0.07
        assert weights["formatting"] == 0.03

    def test_extract_summary_enhanced(self, engine, sample_resume_data):
        """Test enhanced summary extraction"""
        summary_data = engine._extract_summary_enhanced(sample_resume_data)
        
        assert "text" in summary_data
        assert "length" in summary_data
        assert "impact_score" in summary_data
        assert "metrics_found" in summary_data
        assert "action_verbs" in summary_data
        assert "avg_sentence_length" in summary_data
        
        assert summary_data["text"] == "Experienced software developer with 5 years of experience in Python and web development. Led development of 3 major applications and improved team productivity by 25%."
        assert summary_data["length"] > 0
        assert summary_data["impact_score"] >= 0

    def test_extract_skills_enhanced(self, engine, sample_resume_data):
        """Test enhanced skills extraction"""
        skills_data = engine._extract_skills_enhanced(sample_resume_data)
        
        assert "all_skills" in skills_data
        assert "technical_count" in skills_data
        assert "soft_count" in skills_data
        
        assert len(skills_data["all_skills"]) > 0
        assert skills_data["technical_count"] >= 0
        assert skills_data["soft_count"] >= 0

    def test_extract_experience_enhanced(self, engine, sample_resume_data):
        """Test enhanced experience extraction"""
        experience_data = engine._extract_experience_enhanced(sample_resume_data)
        
        assert isinstance(experience_data, list)
        assert len(experience_data) > 0
        
        job = experience_data[0]
        assert "JobTitle" in job
        assert "Company" in job
        assert "Duration" in job
        assert "Responsibilities" in job

    def test_extract_education_enhanced(self, engine, sample_resume_data):
        """Test enhanced education extraction"""
        education_data = engine._extract_education_enhanced(sample_resume_data)
        
        assert isinstance(education_data, list)
        assert len(education_data) > 0
        
        education = education_data[0]
        assert "Degree" in education
        assert "Institution" in education

    def test_extract_all_text(self, engine, sample_resume_data):
        """Test all text extraction"""
        all_text = engine._extract_all_text(sample_resume_data)
        
        assert isinstance(all_text, str)
        assert len(all_text) > 0
        assert "Python" in all_text
        assert "John Doe" in all_text

    def test_analyze_skills_supreme(self, engine):
        """Test supreme skills analysis"""
        skills_data = {
            "all_skills": ["Python", "Django", "React", "Leadership"],
            "technical_count": 3,
            "soft_count": 1
        }
        
        analysis = engine._analyze_skills_supreme(skills_data)
        
        assert "score" in analysis
        assert "analysis" in analysis
        assert "recommendations" in analysis
        assert analysis["score"] >= 0
        assert analysis["score"] <= 10

    def test_analyze_experience_supreme(self, engine):
        """Test supreme experience analysis"""
        experience_data = [
            {
                "JobTitle": "Senior Developer",
                "Company": "Tech Corp",
                "Duration": "3 years",
                "Responsibilities": ["Led team", "Developed applications"]
            }
        ]
        
        analysis = engine._analyze_experience_supreme(experience_data)
        
        assert "score" in analysis
        assert "analysis" in analysis
        assert "recommendations" in analysis
        assert analysis["score"] >= 0
        assert analysis["score"] <= 10

    def test_analyze_education_supreme(self, engine):
        """Test supreme education analysis"""
        education_data = [
            {
                "Degree": "Bachelor of Science",
                "Institution": "University",
                "StartYear": "2015",
                "EndYear": "2019"
            }
        ]
        
        analysis = engine._analyze_education_supreme(education_data)
        
        assert "score" in analysis
        assert "analysis" in analysis
        assert "recommendations" in analysis
        assert analysis["score"] >= 0
        assert analysis["score"] <= 10

    def test_analyze_keywords_supreme(self, engine, sample_resume_data):
        """Test supreme keywords analysis"""
        analysis = engine._analyze_keywords_supreme(sample_resume_data)
        
        assert "score" in analysis
        assert "analysis" in analysis
        assert "recommendations" in analysis
        assert analysis["score"] >= 0
        assert analysis["score"] <= 10

    def test_analyze_formatting_supreme(self, engine, sample_resume_data):
        """Test supreme formatting analysis"""
        analysis = engine._analyze_formatting_supreme(sample_resume_data)
        
        assert "score" in analysis
        assert "analysis" in analysis
        assert "recommendations" in analysis
        assert analysis["score"] >= 0
        assert analysis["score"] <= 10

    def test_calculate_supreme_score(self, engine):
        """Test supreme score calculation"""
        section_scores = {
            "summary": 8.5,
            "skills": 7.8,
            "experience": 8.9,
            "education": 6.5,
            "keywords": 7.5,
            "formatting": 9.0
        }
        
        supreme_score = engine._calculate_supreme_score(section_scores)
        
        assert supreme_score >= 0
        assert supreme_score <= 10
        assert supreme_score > 0  # Should be positive

    def test_generate_supreme_recommendations(self, engine):
        """Test supreme recommendations generation"""
        analyses = {
            "summary": {"score": 7.0, "recommendations": ["Improve summary"]},
            "skills": {"score": 8.0, "recommendations": ["Add more skills"]},
            "experience": {"score": 6.0, "recommendations": ["Enhance experience"]},
            "education": {"score": 8.0, "recommendations": []},
            "keywords": {"score": 7.0, "recommendations": []},
            "formatting": {"score": 9.0, "recommendations": []}
        }
        
        recommendations = engine._generate_supreme_recommendations(analyses)
        
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0

    def test_analyze_market_fit(self, engine, sample_resume_data):
        """Test market fit analysis"""
        market_analysis = engine._analyze_market_fit(sample_resume_data)
        
        assert "keyword_match_percentage" in market_analysis
        assert "found_keywords" in market_analysis
        assert "missing_keywords" in market_analysis
        assert "market_competitiveness" in market_analysis
        
        assert market_analysis["keyword_match_percentage"] >= 0
        assert market_analysis["keyword_match_percentage"] <= 100
        assert isinstance(market_analysis["found_keywords"], list)
        assert isinstance(market_analysis["missing_keywords"], list)
        assert market_analysis["market_competitiveness"] in ["high", "medium", "low"]

    def test_predict_improvement_impact(self, engine):
        """Test improvement impact prediction"""
        current_score = 7.5
        
        predictions = engine._predict_improvement_impact(current_score)
        
        assert "quick_wins" in predictions
        assert "strategic_improvements" in predictions
        assert "supreme_optimization" in predictions
        
        for scenario, details in predictions.items():
            assert "score_increase" in details
            assert "timeline" in details
            assert "effort" in details
            assert "actions" in details

    def test_generate_advanced_insights(self, engine):
        """Test advanced insights generation"""
        analyses = {
            "summary": {"score": 8.0},
            "skills": {"score": 7.5},
            "experience": {"score": 8.5},
            "education": {"score": 7.0},
            "keywords": {"score": 7.8},
            "formatting": {"score": 9.0}
        }
        
        insights = engine._generate_advanced_insights(analyses)
        
        assert "career_progression" in insights
        assert "skill_gaps" in insights
        assert "market_positioning" in insights
        assert "leadership_potential" in insights
        assert "optimization_opportunities" in insights

    @patch('services.supreme_ats_engine.openai.OpenAI')
    def test_analyze_summary_supreme_with_mock(self, mock_openai, engine, sample_resume_data):
        """Test supreme summary analysis with mocked OpenAI"""
        # Mock OpenAI response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = json.dumps({
            "score": 9.0,
            "score_explanation": "Excellent summary with quantifiable achievements",
            "strengths": ["Quantifiable achievements", "Strong action verbs"],
            "weaknesses": ["Could include more keywords"],
            "impact_analysis": {
                "quantifiable_achievements": 2,
                "action_verbs_used": 3,
                "keyword_density": 75.0,
                "readability_score": 8.5
            },
            "improved_versions": [
                {
                    "version": "Supreme optimized version",
                    "score": 10,
                    "focus": "maximum impact",
                    "explanation": "Supreme optimization"
                }
            ],
            "optimization_strategy": {
                "immediate_improvements": ["Add keywords"],
                "strategic_enhancements": ["Enhance leadership"],
                "keyword_opportunities": ["python", "development"]
            }
        })
        
        mock_openai.return_value.chat.completions.create.return_value = mock_response
        
        summary_data = engine._extract_summary_enhanced(sample_resume_data)
        analysis = engine._analyze_summary_supreme(summary_data)
        
        assert "score" in analysis
        assert "score_explanation" in analysis
        assert "strengths" in analysis
        assert "weaknesses" in analysis
        assert "improved_versions" in analysis
        assert analysis["score"] == 9.0

    def test_empty_resume_data(self, engine):
        """Test handling of empty resume data"""
        empty_data = {"resume": {}}
        
        # Test summary extraction
        summary_data = engine._extract_summary_enhanced(empty_data)
        assert summary_data["text"] == ""
        assert summary_data["length"] == 0
        assert summary_data["impact_score"] == 0
        
        # Test skills extraction
        skills_data = engine._extract_skills_enhanced(empty_data)
        assert skills_data["all_skills"] == []
        assert skills_data["technical_count"] == 0
        assert skills_data["soft_count"] == 0
        
        # Test experience extraction
        experience_data = engine._extract_experience_enhanced(empty_data)
        assert experience_data == []
        
        # Test education extraction
        education_data = engine._extract_education_enhanced(empty_data)
        assert education_data == []

    def test_custom_config(self):
        """Test custom configuration"""
        custom_config = SupremeATSConfig(
            scoring_weights={
                "summary": 0.35,
                "experience": 0.25,
                "skills": 0.20,
                "education": 0.15,
                "keywords": 0.03,
                "formatting": 0.02
            },
            keyword_boost=3.0,
            quantifiable_boost=3.5,
            action_verb_boost=2.5,
            experience_boost=2.5,
            education_boost=2.0,
            leadership_boost=3.0
        )
        
        engine = SupremeATSEngine()
        engine.config = custom_config
        
        assert engine.config.scoring_weights["summary"] == 0.35
        assert engine.config.keyword_boost == 3.0
        assert engine.config.quantifiable_boost == 3.5
        assert engine.config.action_verb_boost == 2.5
        assert engine.config.experience_boost == 2.5
        assert engine.config.education_boost == 2.0
        assert engine.config.leadership_boost == 3.0


if __name__ == "__main__":
    pytest.main([__file__]) 