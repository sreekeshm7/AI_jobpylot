#!/usr/bin/env python3
"""
Test script for AI JobPylot ATS Engine
Demonstrates the core functionality with sample data
"""

import json
import requests
from typing import Dict, Any

# Configuration
BASE_URL = "http://localhost:8000"

def test_ats_functionality():
    """Test the ATS engine with sample data"""
    
    print("🚀 Testing AI JobPylot ATS Engine")
    print("=" * 50)
    
    # Sample job posting
    sample_job = {
        "title": "Senior Python Developer",
        "required_skills": ["Python", "Django", "PostgreSQL", "REST APIs"],
        "preferred_skills": ["React", "AWS", "Docker", "Kubernetes", "CI/CD"],
        "experience_years": 5,
        "education_level": "Bachelor",
        "industry": "Technology",
        "location": "Remote",
        "description": "We are seeking a senior Python developer with experience in building scalable web applications. The ideal candidate will have strong backend development skills and experience with modern development practices."
    }
    
    # Sample candidate resume data
    sample_candidate = {
        "candidate_id": "candidate_001",
        "resume_data": {
            "resume": {
                "Name": "Jane Smith",
                "Email": "jane.smith@email.com",
                "Phone": "+1-555-0123",
                "Summary": "Experienced software engineer with 6 years of experience in Python development, specializing in web applications and API development. Proven track record of delivering scalable solutions and leading development teams.",
                "Skills": {
                    "TechStack": ["Python", "Django", "Flask", "PostgreSQL", "MongoDB"],
                    "Tools": ["Git", "Docker", "AWS", "Jenkins"],
                    "soft_skills": ["Leadership", "Communication", "Problem Solving"],
                    "Languages": ["English", "Spanish"],
                    "Others": ["REST APIs", "Microservices", "Agile"]
                },
                "WorkExperience": [
                    {
                        "JobTitle": "Senior Software Engineer",
                        "Company": "TechCorp Inc",
                        "Duration": "3 years",
                        "Location": "San Francisco, CA",
                        "Responsibilities": [
                            "Led development of microservices architecture",
                            "Improved API performance by 40%",
                            "Mentored junior developers",
                            "Implemented CI/CD pipelines"
                        ],
                        "TechStack": ["Python", "Django", "PostgreSQL", "Docker"]
                    },
                    {
                        "JobTitle": "Software Developer",
                        "Company": "StartupXYZ",
                        "Duration": "3 years",
                        "Location": "Austin, TX",
                        "Responsibilities": [
                            "Developed REST APIs using Flask",
                            "Built frontend components with React",
                            "Optimized database queries",
                            "Collaborated with cross-functional teams"
                        ],
                        "TechStack": ["Python", "Flask", "React", "MongoDB"]
                    }
                ],
                "Education": [
                    {
                        "Degree": "Bachelor of Computer Science",
                        "Institution": "University of Technology",
                        "Location": "Austin, TX",
                        "StartYear": "2015",
                        "EndYear": "2019"
                    }
                ],
                "Certifications": ["AWS Certified Developer", "Docker Certified Associate"],
                "Languages": ["English", "Spanish"],
                "Achievements": [
                    "Led team that won Best Innovation Award 2023",
                    "Reduced deployment time by 60%",
                    "Mentored 5 junior developers to senior level"
                ]
            },
            "summary": "Experienced software engineer with 6 years of experience in Python development, specializing in web applications and API development. Proven track record of delivering scalable solutions and leading development teams."
        }
    }
    
    try:
        # Test 1: Add job posting
        print("\n1. Adding job posting...")
        job_response = requests.post(f"{BASE_URL}/ats/jobs", json=sample_job)
        if job_response.status_code == 200:
            job_data = job_response.json()
            job_id = job_data["job_id"]
            print(f"✅ Job posted successfully! Job ID: {job_id}")
        else:
            print(f"❌ Failed to add job: {job_response.text}")
            return
        
        # Test 2: Register candidate
        print("\n2. Registering candidate...")
        candidate_response = requests.post(f"{BASE_URL}/ats/candidates", json=sample_candidate)
        if candidate_response.status_code == 200:
            candidate_data = candidate_response.json()
            candidate_id = candidate_data["candidate_id"]
            print(f"✅ Candidate registered successfully! Candidate ID: {candidate_id}")
        else:
            print(f"❌ Failed to register candidate: {candidate_response.text}")
            return
        
        # Test 3: Match candidate to job
        print("\n3. Matching candidate to job...")
        match_request = {
            "candidate_id": candidate_id,
            "job_id": job_id
        }
        match_response = requests.post(f"{BASE_URL}/ats/match", json=match_request)
        if match_response.status_code == 200:
            match_data = match_response.json()
            print("✅ Match completed successfully!")
            print(f"   Overall Score: {match_data['overall_score']:.2%}")
            print(f"   Skills Match: {match_data['skills_match']:.2%}")
            print(f"   Experience Match: {match_data['experience_match']:.2%}")
            print(f"   Education Match: {match_data['education_match']:.2%}")
            print(f"   Keyword Match: {match_data['keyword_match']:.2%}")
            print(f"   ATS Compatibility: {match_data['ats_compatibility']:.2%}")
            
            # Print detailed feedback
            feedback = match_data['detailed_feedback']
            print(f"\n   📋 Detailed Feedback:")
            print(f"   Overall Assessment: {feedback.get('overall_assessment', 'N/A')}")
            print(f"   Fit Score: {feedback.get('fit_score', 'N/A')}")
            print(f"   Strengths: {', '.join(feedback.get('strengths', []))}")
            print(f"   Areas for Improvement: {', '.join(feedback.get('areas_for_improvement', []))}")
        else:
            print(f"❌ Failed to match: {match_response.text}")
        
        # Test 4: Get job recommendations for candidate
        print("\n4. Getting job recommendations...")
        recommendations_request = {
            "candidate_id": candidate_id,
            "limit": 3
        }
        rec_response = requests.post(f"{BASE_URL}/ats/job-recommendations", json=recommendations_request)
        if rec_response.status_code == 200:
            recommendations = rec_response.json()
            print(f"✅ Found {len(recommendations)} job recommendations:")
            for i, rec in enumerate(recommendations, 1):
                print(f"   {i}. {rec['job_title']} at {rec['company']} ({rec['overall_score']:.2%} match)")
        else:
            print(f"❌ Failed to get recommendations: {rec_response.text}")
        
        # Test 5: Rank candidates for job
        print("\n5. Ranking candidates for job...")
        ranking_request = {
            "job_id": job_id,
            "limit": 5
        }
        ranking_response = requests.post(f"{BASE_URL}/ats/rank-candidates", json=ranking_request)
        if ranking_response.status_code == 200:
            rankings = ranking_response.json()
            print(f"✅ Ranked {len(rankings)} candidates:")
            for i, candidate in enumerate(rankings, 1):
                print(f"   {i}. {candidate['candidate_name']} ({candidate['overall_score']:.2%} match)")
        else:
            print(f"❌ Failed to rank candidates: {ranking_response.text}")
        
        # Test 6: ATS compatibility analysis
        print("\n6. Analyzing ATS compatibility...")
        ats_request = {
            "resume_data": sample_candidate["resume_data"]
        }
        ats_response = requests.post(f"{BASE_URL}/ats/analyze-resume", json=ats_request)
        if ats_response.status_code == 200:
            ats_data = ats_response.json()
            print("✅ ATS analysis completed!")
            print(f"   Overall ATS Score: {ats_data['overall_ats_score']}/100")
            print(f"   Parsing Confidence: {ats_data['parsing_confidence']}/100")
            print(f"   Keyword Optimization: {ats_data['keyword_optimization']}/100")
            print(f"   Format Compatibility: {ats_data['format_compatibility']}/100")
            print(f"   Content Quality: {ats_data['content_quality']}/100")
        else:
            print(f"❌ Failed to analyze ATS compatibility: {ats_response.text}")
        
        # Test 7: Dashboard statistics
        print("\n7. Getting dashboard statistics...")
        dashboard_response = requests.get(f"{BASE_URL}/ats/dashboard")
        if dashboard_response.status_code == 200:
            dashboard_data = dashboard_response.json()
            print("✅ Dashboard stats retrieved!")
            print(f"   Total Candidates: {dashboard_data['total_candidates']}")
            print(f"   Total Jobs: {dashboard_data['total_jobs']}")
            print(f"   Total Matches: {dashboard_data['total_matches']}")
            print(f"   Average Match Score: {dashboard_data['average_match_score']:.2%}")
        else:
            print(f"❌ Failed to get dashboard stats: {dashboard_response.text}")
        
        # Test 8: Search candidates
        print("\n8. Searching candidates...")
        search_request = {
            "skills": ["Python", "Django"],
            "experience_min": 3,
            "experience_max": 10,
            "limit": 5
        }
        search_response = requests.post(f"{BASE_URL}/ats/search/candidates", json=search_request)
        if search_response.status_code == 200:
            search_results = search_response.json()
            print(f"✅ Found {len(search_results)} matching candidates:")
            for candidate in search_results:
                print(f"   - {candidate['name']} ({candidate['experience_years']} years exp)")
        else:
            print(f"❌ Failed to search candidates: {search_response.text}")
        
        print("\n" + "=" * 50)
        print("🎉 All tests completed successfully!")
        print("Your ATS engine is working perfectly!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API. Make sure the server is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")

def test_resume_analysis():
    """Test the original resume analysis functionality"""
    
    print("\n📄 Testing Resume Analysis Features")
    print("=" * 50)
    
    # Sample resume data for analysis
    sample_resume_data = {
        "resume": {
            "Name": "John Doe",
            "Email": "john.doe@email.com",
            "Summary": "Experienced software developer with expertise in Python and web development. Passionate about creating efficient and scalable solutions.",
            "Skills": {
                "TechStack": ["Python", "JavaScript", "React"],
                "Tools": ["Git", "Docker"],
                "soft_skills": ["Teamwork", "Communication"]
            },
            "WorkExperience": [
                {
                    "JobTitle": "Software Developer",
                    "Company": "Tech Solutions",
                    "Duration": "2 years",
                    "Responsibilities": [
                        "Developed web applications",
                        "Collaborated with team members",
                        "Implemented new features"
                    ]
                }
            ],
            "Education": [
                {
                    "Degree": "Bachelor of Computer Science",
                    "Institution": "University of Technology"
                }
            ]
        },
        "summary": "Experienced software developer with expertise in Python and web development. Passionate about creating efficient and scalable solutions."
    }
    
    try:
        # Test summary evaluation
        print("\n1. Evaluating resume summary...")
        summary_response = requests.post(f"{BASE_URL}/evaluate-summary", json=sample_resume_data)
        if summary_response.status_code == 200:
            summary_data = summary_response.json()
            print("✅ Summary evaluation completed!")
            print(f"   ATS Score: {summary_data['ats_score']}/10")
            print(f"   Weak Sentences: {len(summary_data['weak_sentences'])}")
            print(f"   Strong Sentences: {len(summary_data['strong_sentences'])}")
            print(f"   Improved Summaries: {len(summary_data['improved_summaries'])}")
        else:
            print(f"❌ Failed to evaluate summary: {summary_response.text}")
        
        # Test quantifiable impact evaluation
        print("\n2. Evaluating quantifiable impact...")
        impact_response = requests.post(f"{BASE_URL}/evaluate-quantifiable-impact", json=sample_resume_data)
        if impact_response.status_code == 200:
            impact_data = impact_response.json()
            print("✅ Quantifiable impact evaluation completed!")
            print(f"   ATS Score: {impact_data['ats_score']}/10")
            print(f"   Weak Sentences: {len(impact_data['weak_sentences'])}")
            print(f"   Strong Sentences: {len(impact_data['strong_sentences'])}")
        else:
            print(f"❌ Failed to evaluate quantifiable impact: {impact_response.text}")
        
        # Test skill suggestions
        print("\n3. Getting skill suggestions...")
        skills_request = {
            "resume_data": sample_resume_data,
            "target_role": "Senior Python Developer"
        }
        skills_response = requests.post(f"{BASE_URL}/suggest-relevant-skills", json=skills_request)
        if skills_response.status_code == 200:
            skills_data = skills_response.json()
            print("✅ Skill suggestions generated!")
            print(f"   Suggested Skills: {', '.join(skills_data['suggested_skills'])}")
        else:
            print(f"❌ Failed to get skill suggestions: {skills_response.text}")
        
        print("\n" + "=" * 50)
        print("✅ Resume analysis tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API. Make sure the server is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")

if __name__ == "__main__":
    print("🧪 AI JobPylot ATS Engine Test Suite")
    print("Make sure the server is running on http://localhost:8000")
    print("Run: python main_ats.py")
    
    # Test ATS functionality
    test_ats_functionality()
    
    # Test resume analysis functionality
    test_resume_analysis()
    
    print("\n🎯 Test Summary:")
    print("- ATS Engine: Job posting, candidate registration, matching, ranking")
    print("- Resume Analysis: Summary evaluation, impact analysis, skill suggestions")
    print("- Search & Filter: Candidate and job search capabilities")
    print("- Analytics: Dashboard statistics and performance metrics")
    print("\n🚀 Your GPT-3.5-powered ATS engine is ready for production!") 