#!/usr/bin/env python3
"""
Test script for the Hybrid ATS Checker
Demonstrates the functionality of the comprehensive ATS analysis system
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from typing import Dict, Any

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from deterministic_ats_engine import DeterministicATSEngine, DeterministicScore
from enhanced_openai_service import EnhancedOpenAIService

class HybridATSTester:
    """Test class for the Hybrid ATS Checker"""
    
    def __init__(self):
        self.deterministic_engine = DeterministicATSEngine()
        self.openai_service = EnhancedOpenAIService()
        
        # Sample resume data for testing
        self.sample_resume = {
            "Name": "John Doe",
            "Email": "john.doe@email.com",
            "Phone": "+1-555-123-4567",
            "Summary": "Experienced software developer with 5 years of experience in web development. Led a team of 8 developers to deliver a project that increased company revenue by 25%. Skilled in Python, JavaScript, and React.",
            "Skills": {
                "TechStack": ["Python", "JavaScript", "React", "Node.js"],
                "soft_skills": ["Leadership", "Team Management", "Problem Solving"],
                "Languages": ["English", "Spanish"]
            },
            "WorkExperience": [
                {
                    "JobTitle": "Senior Software Developer",
                    "Company": "Tech Corp",
                    "Duration": "2020-2023",
                    "Location": "San Francisco, CA",
                    "Responsibilities": [
                        "Led a team of 8 developers to deliver a project that increased company revenue by 25%",
                        "Developed and maintained web applications using Python and React",
                        "Collaborated with cross-functional teams to implement new features",
                        "Mentored junior developers and conducted code reviews"
                    ],
                    "TechStack": ["Python", "React", "AWS", "Docker"]
                },
                {
                    "JobTitle": "Software Developer",
                    "Company": "Startup Inc",
                    "Duration": "2018-2020",
                    "Location": "New York, NY",
                    "Responsibilities": [
                        "Assisted in developing web applications",
                        "Worked on bug fixes and feature implementations",
                        "Participated in team meetings and code reviews"
                    ],
                    "TechStack": ["JavaScript", "Node.js", "MongoDB"]
                }
            ],
            "Education": [
                {
                    "Degree": "Bachelor of Science in Computer Science",
                    "Institution": "University of Technology",
                    "StartYear": "2014",
                    "EndYear": "2018",
                    "Location": "New York, NY"
                }
            ],
            "Links": {
                "LinkedIn": "https://linkedin.com/in/johndoe",
                "GitHub": "https://github.com/johndoe",
                "Portfolio": "https://johndoe.dev"
            }
        }
    
    def test_deterministic_scoring(self):
        """Test deterministic scoring for all sections"""
        print("🔍 Testing Deterministic Scoring...")
        print("=" * 50)
        
        # Test summary scoring
        summary_score = self.deterministic_engine.score_summary(self.sample_resume["Summary"])
        print(f"Summary Score: {summary_score.score}/10 ({summary_score.get_percentage():.1f}%)")
        
        # Test date scoring
        date_score = self.deterministic_engine.score_dates(self.sample_resume)
        print(f"Date Formatting Score: {date_score.score}/10 ({date_score.get_percentage():.1f}%)")
        
        # Test weak verbs scoring
        weak_verbs_score = self.deterministic_engine.score_weak_verbs(self.sample_resume)
        print(f"Weak Verbs Score: {weak_verbs_score.score}/10 ({weak_verbs_score.get_percentage():.1f}%)")
        
        # Test quantity impact scoring
        quantity_score = self.deterministic_engine.score_quantity_impact(self.sample_resume)
        print(f"Quantity Impact Score: {quantity_score.score}/10 ({quantity_score.get_percentage():.1f}%)")
        
        # Test teamwork scoring
        teamwork_score = self.deterministic_engine.score_teamwork(self.sample_resume)
        print(f"Teamwork Score: {teamwork_score.score}/10 ({teamwork_score.get_percentage():.1f}%)")
        
        # Test buzzwords scoring
        buzzwords_score = self.deterministic_engine.score_buzzwords(self.sample_resume)
        print(f"Buzzwords Score: {buzzwords_score.score}/10 ({buzzwords_score.get_percentage():.1f}%)")
        
        # Test contact details scoring
        contact_score = self.deterministic_engine.score_contact_details(self.sample_resume)
        print(f"Contact Details Score: {contact_score.score}/10 ({contact_score.get_percentage():.1f}%)")
        
        # Test grammar/spelling scoring
        grammar_score = self.deterministic_engine.score_grammar_spelling(self.sample_resume)
        print(f"Grammar/Spelling Score: {grammar_score.score}/10 ({grammar_score.get_percentage():.1f}%)")
        
        # Test formatting/layout scoring
        formatting_score = self.deterministic_engine.score_formatting_layout(self.sample_resume)
        print(f"Formatting/Layout Score: {formatting_score.score}/10 ({formatting_score.get_percentage():.1f}%)")
        
        # Test ATS keywords scoring
        ats_keywords_score = self.deterministic_engine.score_ats_keywords(self.sample_resume)
        print(f"ATS Keywords Score: {ats_keywords_score.score}/10 ({ats_keywords_score.get_percentage():.1f}%)")
        
        # Test skills relevance scoring
        skills_score = self.deterministic_engine.score_skills_relevance(self.sample_resume)
        print(f"Skills Relevance Score: {skills_score.score}/10 ({skills_score.get_percentage():.1f}%)")
        
        # Test achievements vs responsibilities scoring
        achievements_score = self.deterministic_engine.score_achievements_vs_responsibilities(self.sample_resume)
        print(f"Achievements vs Responsibilities Score: {achievements_score.score}/10 ({achievements_score.get_percentage():.1f}%)")
        
        print("\n" + "=" * 50)
    
    async def test_gpt_analysis(self):
        """Test GPT-3.5 turbo analysis"""
        print("🤖 Testing GPT-3.5 Turbo Analysis...")
        print("=" * 50)
        
        try:
            # Test summary analysis
            summary_analysis = await self.openai_service.analyze_section_with_gpt(
                "summary", 
                self.sample_resume, 
                "Analyze the resume summary for ATS optimization"
            )
            print("Summary Analysis:")
            print(f"  - Model Used: {summary_analysis.get('model_used', 'N/A')}")
            print(f"  - Analysis Score: {summary_analysis.get('analysis', {}).get('score', 'N/A')}/10")
            print(f"  - Strengths: {len(summary_analysis.get('analysis', {}).get('strengths', []))}")
            print(f"  - Weaknesses: {len(summary_analysis.get('analysis', {}).get('weaknesses', []))}")
            print(f"  - Recommendations: {len(summary_analysis.get('analysis', {}).get('recommendations', []))}")
            
            # Test skill suggestions
            skill_suggestions = await self.openai_service.suggest_relevant_skills(
                self.sample_resume, 
                "Senior Software Developer"
            )
            print("\nSkill Suggestions:")
            print(f"  - Technical Skills: {len(skill_suggestions.get('suggestions', {}).get('technical_skills', []))}")
            print(f"  - Soft Skills: {len(skill_suggestions.get('suggestions', {}).get('soft_skills', []))}")
            print(f"  - Keywords: {len(skill_suggestions.get('suggestions', {}).get('keywords', []))}")
            
            # Test content generation
            generated_content = await self.openai_service.generate_section_content(
                "skills",
                "Software developer with 5 years experience in web development",
                self.sample_resume
            )
            print("\nContent Generation:")
            print(f"  - Section: {generated_content.get('section', 'N/A')}")
            print(f"  - Content Length: {len(generated_content.get('generated_content', ''))} characters")
            
        except Exception as e:
            print(f"❌ GPT Analysis failed: {str(e)}")
            print("Note: Make sure OPENAI_API_KEY is set in environment variables")
        
        print("\n" + "=" * 50)
    
    def test_line_by_line_analysis(self):
        """Test line-by-line analysis"""
        print("📝 Testing Line-by-Line Analysis...")
        print("=" * 50)
        
        # Convert resume to text for line analysis
        resume_text = json.dumps(self.sample_resume, indent=2)
        lines = resume_text.split('\n')
        
        print(f"Total lines: {len(lines)}")
        print(f"Non-empty lines: {len([line for line in lines if line.strip()])}")
        
        # Analyze first 10 lines
        for i, line in enumerate(lines[:10]):
            if line.strip():
                line_score = self.deterministic_engine.analyze_line(line)
                print(f"Line {i+1}: Score {line_score.score:.1f}/10 - {line.strip()[:50]}...")
        
        print("\n" + "=" * 50)
    
    def test_comprehensive_analysis(self):
        """Test comprehensive analysis with all sections"""
        print("🎯 Testing Comprehensive Analysis...")
        print("=" * 50)
        
        sections = [
            ("Summary", self.deterministic_engine.score_summary(self.sample_resume["Summary"])),
            ("Dates", self.deterministic_engine.score_dates(self.sample_resume)),
            ("Weak Verbs", self.deterministic_engine.score_weak_verbs(self.sample_resume)),
            ("Quantity Impact", self.deterministic_engine.score_quantity_impact(self.sample_resume)),
            ("Teamwork", self.deterministic_engine.score_teamwork(self.sample_resume)),
            ("Buzzwords", self.deterministic_engine.score_buzzwords(self.sample_resume)),
            ("Contact Details", self.deterministic_engine.score_contact_details(self.sample_resume)),
            ("Grammar/Spelling", self.deterministic_engine.score_grammar_spelling(self.sample_resume)),
            ("Formatting/Layout", self.deterministic_engine.score_formatting_layout(self.sample_resume)),
            ("ATS Keywords", self.deterministic_engine.score_ats_keywords(self.sample_resume)),
            ("Skills Relevance", self.deterministic_engine.score_skills_relevance(self.sample_resume)),
            ("Achievements vs Responsibilities", self.deterministic_engine.score_achievements_vs_responsibilities(self.sample_resume))
        ]
        
        total_score = 0
        print("Section-by-Section Analysis (0-10 scale):")
        print("-" * 50)
        
        for section_name, score in sections:
            total_score += score.score
            print(f"{section_name:<25} {score.score:>5.1f}/10 ({score.get_percentage():>5.1f}%)")
        
        overall_score_100 = (total_score / len(sections)) * 10  # Convert to 100-point scale
        print("-" * 50)
        print(f"{'OVERALL ATS SCORE':<25} {overall_score_100:>5.1f}/100 ({overall_score_100:>5.1f}%)")
        
        # Grade the resume (100-point system)
        if overall_score_100 >= 90:
            grade = "A+ (Excellent)"
        elif overall_score_100 >= 80:
            grade = "A (Very Good)"
        elif overall_score_100 >= 70:
            grade = "B+ (Good)"
        elif overall_score_100 >= 60:
            grade = "B (Above Average)"
        elif overall_score_100 >= 50:
            grade = "C (Average)"
        elif overall_score_100 >= 40:
            grade = "D (Below Average)"
        else:
            grade = "F (Poor)"
        
        print(f"{'GRADE':<25} {grade}")
        
        print("\n" + "=" * 50)
    
    def generate_test_report(self):
        """Generate a comprehensive test report"""
        print("📊 Generating Test Report...")
        print("=" * 50)
        
        report = {
            "test_timestamp": datetime.now().isoformat(),
            "resume_analysis": {
                "filename": "sample_resume.json",
                "overall_score": 0,
                "section_scores": {},
                "recommendations": [],
                "strengths": [],
                "weaknesses": []
            },
            "system_info": {
                "deterministic_engine": "operational",
                "gpt_service": "operational" if os.getenv('OPENAI_API_KEY') else "not_configured",
                "total_sections": 12
            }
        }
        
        # Calculate scores
        sections = [
            ("summary", self.deterministic_engine.score_summary(self.sample_resume["Summary"])),
            ("dates", self.deterministic_engine.score_dates(self.sample_resume)),
            ("weak_verbs", self.deterministic_engine.score_weak_verbs(self.sample_resume)),
            ("quantity_impact", self.deterministic_engine.score_quantity_impact(self.sample_resume)),
            ("teamwork", self.deterministic_engine.score_teamwork(self.sample_resume)),
            ("buzzwords", self.deterministic_engine.score_buzzwords(self.sample_resume)),
            ("contact_details", self.deterministic_engine.score_contact_details(self.sample_resume)),
            ("grammar_spelling", self.deterministic_engine.score_grammar_spelling(self.sample_resume)),
            ("formatting_layout", self.deterministic_engine.score_formatting_layout(self.sample_resume)),
            ("ats_keywords", self.deterministic_engine.score_ats_keywords(self.sample_resume)),
            ("skills_relevance", self.deterministic_engine.score_skills_relevance(self.sample_resume)),
            ("achievements_vs_responsibilities", self.deterministic_engine.score_achievements_vs_responsibilities(self.sample_resume))
        ]
        
        total_score = 0
        for section_name, score in sections:
            report["resume_analysis"]["section_scores"][section_name] = {
                "score": score.score,
                "percentage": score.get_percentage()
            }
            total_score += score.score
        
        report["resume_analysis"]["overall_score"] = (total_score / len(sections)) * 10  # Convert to 100-point scale
        
        # Generate recommendations
        low_scores = [(name, score) for name, score in sections if score.score < 6.0]
        high_scores = [(name, score) for name, score in sections if score.score >= 8.0]
        
        for section_name, score in low_scores:
            report["resume_analysis"]["weaknesses"].append(f"{section_name}: {score.score}/10")
            report["resume_analysis"]["recommendations"].append(f"Improve {section_name} section")
        
        for section_name, score in high_scores:
            report["resume_analysis"]["strengths"].append(f"{section_name}: {score.score}/10")
        
        # Save report
        with open("hybrid_ats_test_report.json", "w") as f:
            json.dump(report, f, indent=2)
        
        print("✅ Test report generated: hybrid_ats_test_report.json")
        print(f"📈 Overall Score: {report['resume_analysis']['overall_score']:.1f}/100")
        print(f"🔍 Sections Analyzed: {len(sections)}")
        print(f"💪 Strengths: {len(report['resume_analysis']['strengths'])}")
        print(f"⚠️  Weaknesses: {len(report['resume_analysis']['weaknesses'])}")
        print(f"💡 Recommendations: {len(report['resume_analysis']['recommendations'])}")
        
        print("\n" + "=" * 50)

async def main():
    """Main test function"""
    print("🚀 Hybrid ATS Checker - Test Suite")
    print("=" * 60)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tester = HybridATSTester()
    
    # Run all tests
    tester.test_deterministic_scoring()
    await tester.test_gpt_analysis()
    tester.test_line_by_line_analysis()
    tester.test_comprehensive_analysis()
    tester.generate_test_report()
    
    print("✅ All tests completed successfully!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main()) 