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
        """Convert resume text to structured JSON format"""
        prompt = f"""
        Parse the following resume text and convert it to the exact JSON format specified below. 
        Extract all available information and structure it properly. If any field is not available, use empty string or empty array as appropriate.

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
                  "bullets": [],
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

        Return only the JSON object, no additional text.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse OpenAI response as JSON: {str(e)}")
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    def evaluate_summary(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
    """Evaluate resume summary with ATS scoring"""
    prompt = f"""
You are an expert ATS resume evaluator. Analyze the following resume data and evaluate the 'Summary' section using the steps below.

Resume Data:
{json.dumps(resume_data, indent=2)}

Follow these exact steps:

**Step 1: Extract Existing Summary**
- Extract and display the current "Summary" field from the resume.

**Step 2: Give ATS Score (Out of 10)**
Evaluate the extracted summary based on the following ATS criteria:
- Presence of job-specific keywords
- Alignment with skills, experience, and qualifications in the resume
- Clarity, professionalism, and sentence structure
- Overall conciseness and relevance
Return an integer ATS score (0–10).

**Step 3: Identify Weak Sentences**
- List sentences or phrases that are generic, vague, or irrelevant.
- Briefly explain why each is weak and how it negatively affects the score.

**Step 4: Identify Strong Sentences**
- List sentences or phrases that boost the score.
- Explain why they are effective and ATS-friendly.

**Step 5: Justify the Score**
- Give 2–4 bullet points explaining how the score was determined (positive and negative factors).

**Step 6: Generate 4 Improved Summaries**
- Write 4 new summary versions that would score 10/10 in ATS.
- Each version must:
  - Be fewer than 4 sentences
  - Include relevant job title keywords
  - Be tailored to the resume’s actual skills and experience
  - Replace weak parts with strong, actionable, and specific phrases
- Ensure every new summary addresses the earlier weaknesses and shows clear improvement.

Return the output in this exact JSON format:
{{
  "extracted_summary": "...",
  "ats_score": 0,
  "weak_sentences": ["..."],
  "strong_sentences": ["..."],
  "score_feedback": ["...", "..."],
  "new_summaries": ["...", "...", "...", "..."]
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
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse OpenAI response as JSON: {str(e)}")
    except Exception as e:
        raise Exception(f"OpenAI API error: {str(e)}")

    
    def evaluate_section(self, resume_data: Dict[str, Any], section_name: str) -> Dict[str, Any]:
        """Evaluate specific resume section with detailed, targeted prompts"""
        
        # Get the specific prompt for this section
        prompt = self._get_section_specific_prompt(resume_data, section_name)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse OpenAI response as JSON: {str(e)}")
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")

    def _get_section_specific_prompt(self, resume_data: Dict[str, Any], section_name: str) -> str:
        """Get detailed, section-specific prompts for accurate analysis"""
        
        resume_json = json.dumps(resume_data, indent=2)
        
        if section_name == "quantifiable_impact":
            return f"""
            You are an expert resume analyst specializing in quantifiable achievements and measurable impact.

            Resume Data: {resume_json}

            TASK: Analyze this resume for quantifiable impact and measurable achievements.

            SPECIFIC ANALYSIS CRITERIA:
            1. Look for specific numbers, percentages, dollar amounts, timeframes
            2. Identify achievements with measurable outcomes vs. basic job duties
            3. Check for metrics like: revenue generated, costs saved, efficiency improvements, team size managed, project timelines, performance improvements
            4. Evaluate the use of action verbs combined with quantifiable results
            5. Assess whether achievements demonstrate clear business impact

            SCORING CRITERIA (1-10):
            - 9-10: Multiple quantified achievements with clear business impact
            - 7-8: Some quantified achievements, good use of metrics
            - 5-6: Few quantified achievements, mostly generic statements
            - 3-4: Minimal quantification, mostly job duties
            - 1-2: No quantifiable achievements, all generic statements

            Respond in this exact JSON format:
            {{
              "section_name": "quantifiable_impact",
              "ats_score": 0,
              "feedback": ["detailed analysis of quantifiable impact usage"],
              "weak_sentences": ["sentences lacking quantifiable impact"],
              "strong_sentences": ["sentences with good quantifiable impact"],
              "improved_content": ["improved versions with specific metrics"],
              "examples": ["examples of strong quantifiable statements for this field"]
            }}
            """
            
        elif section_name == "date_format":
            return f"""
            You are an expert resume analyst specializing in date formatting and chronological consistency.

            Resume Data: {resume_json}

            TASK: Analyze date formats, chronological order, and consistency across all sections.

            SPECIFIC ANALYSIS CRITERIA:
            1. Check date format consistency (MM/YYYY, Month YYYY, etc.)
            2. Verify chronological order (most recent first)
            3. Look for date gaps and overlaps in work experience and education
            4. Ensure all date fields are complete (start and end dates)
            5. Check for "Present", "Current", or ongoing positions formatting
            6. Verify logical progression of career timeline

            COMMON DATE FORMAT ISSUES:
            - Inconsistent formats (mixing MM/YYYY with Month YYYY)
            - Missing start or end dates
            - Illogical chronology (gaps or overlaps)
            - Using different formats for similar sections
            - Unclear current position indicators

            SCORING CRITERIA (1-10):
            - 9-10: Perfect date consistency, clear chronology, no gaps
            - 7-8: Minor inconsistencies, mostly good chronology
            - 5-6: Some date format issues, minor chronological problems
            - 3-4: Multiple date formatting problems, confusing timeline
            - 1-2: Major date inconsistencies, chronological chaos

            Respond in this exact JSON format:
            {{
              "section_name": "date_format",
              "ats_score": 0,
              "feedback": ["detailed analysis of date formatting and chronology"],
              "date_issues": ["specific date formatting problems found"],
              "suggested_format": "MM/YYYY (recommended consistent format)",
              "formatting_issues": ["inconsistencies in date presentation"],
              "corrections": ["corrected date formats for problematic entries"]
            }}
            """
            
        elif section_name == "weak_verbs":
            return f"""
            You are an expert resume analyst specializing in action verbs and impactful language usage.

            Resume Data: {resume_json}

            TASK: Analyze the use of action verbs, identify weak/passive language, and suggest powerful alternatives.

            SPECIFIC ANALYSIS CRITERIA:
            1. Identify weak, passive, or overused verbs (responsible for, worked on, helped with, handled, dealt with, involved in, participated in)
            2. Look for strong action verbs that demonstrate leadership and achievement (achieved, implemented, developed, optimized, spearheaded, delivered)
            3. Check for passive voice vs. active voice construction
            4. Evaluate verb variety and impact level
            5. Assess whether verbs match the seniority level and role type

            WEAK VERBS TO AVOID:
            - "Responsible for" → Use specific action verbs instead
            - "Worked on" → "Developed", "Built", "Created"
            - "Helped with" → "Collaborated on", "Contributed to", "Supported"
            - "Handled" → "Managed", "Coordinated", "Executed"
            - "Dealt with" → "Resolved", "Addressed", "Managed"

            STRONG VERBS TO USE:
            - Leadership: Led, Directed, Managed, Supervised, Coordinated
            - Achievement: Achieved, Accomplished, Delivered, Exceeded, Completed
            - Innovation: Developed, Created, Designed, Implemented, Launched
            - Improvement: Optimized, Enhanced, Streamlined, Improved, Increased

            SCORING CRITERIA (1-10):
            - 9-10: Strong, varied action verbs throughout, no weak language
            - 7-8: Mostly strong verbs, minimal weak language
            - 5-6: Mix of strong and weak verbs
            - 3-4: Many weak verbs, passive language
            - 1-2: Predominantly weak verbs, very passive language

            Respond in this exact JSON format:
            {{
              "section_name": "weak_verbs",
              "ats_score": 0,
              "feedback": ["detailed analysis of verb usage and language strength"],
              "weak_sentences": ["sentences with weak or passive verbs"],
              "strong_sentences": ["sentences with strong action verbs"],
              "improved_content": ["rewritten sentences with stronger verbs"],
              "examples": ["examples of powerful action verbs for this role type"]
            }}
            """
            
        elif section_name == "teamwork_collaboration":
            return f"""
            You are an expert resume analyst specializing in teamwork and collaboration indicators.

            Resume Data: {resume_json}

            TASK: Analyze how well the resume demonstrates teamwork, collaboration, and interpersonal skills.

            SPECIFIC ANALYSIS CRITERIA:
            1. Look for collaborative language and team-oriented achievements
            2. Identify examples of cross-functional collaboration
            3. Check for leadership within team contexts
            4. Evaluate mentions of team size, team management, or team contributions
            5. Assess balance between individual achievements and team collaboration
            6. Look for soft skills that indicate good teamwork

            COLLABORATION INDICATORS TO LOOK FOR:
            - "Collaborated with", "Worked closely with", "Partnered with"
            - "Led a team of X", "Managed cross-functional teams"
            - "Coordinated with stakeholders", "Facilitated team meetings"
            - Examples of mentoring, training, or knowledge sharing
            - Cross-departmental projects and initiatives
            - Team achievements vs. individual accomplishments

            SCORING CRITERIA (1-10):
            - 9-10: Strong evidence of collaboration, team leadership, mentoring
            - 7-8: Good teamwork examples, some collaborative achievements
            - 5-6: Some team mentions, but mostly individual focus
            - 3-4: Minimal collaboration evidence, very individual-focused
            - 1-2: No teamwork indicators, purely individual achievements

            Respond in this exact JSON format:
            {{
              "section_name": "teamwork_collaboration",
              "ats_score": 0,
              "feedback": ["detailed analysis of teamwork and collaboration indicators"],
              "weak_sentences": ["sentences that could better show collaboration"],
              "strong_sentences": ["sentences that demonstrate good teamwork"],
              "improved_content": ["rewritten content emphasizing collaboration"],
              "examples": ["examples of strong collaborative language for this role"]
            }}
            """
            
        elif section_name == "buzzwords_cliches":
            return f"""
            You are an expert resume analyst specializing in identifying and eliminating buzzwords, clichés, and overused phrases.

            Resume Data: {resume_json}

            TASK: Identify buzzwords, clichés, and overused phrases that hurt ATS performance and professional credibility.

            COMMON BUZZWORDS TO IDENTIFY:
            - "Hard-working", "Team player", "Detail-oriented"
            - "Results-driven", "Go-getter", "Self-starter"
            - "Think outside the box", "Hit the ground running"
            - "Synergy", "Leverage", "Utilize" (instead of "use")
            - "Best of breed", "Cutting-edge", "Game-changer"
            - "Dynamic", "Innovative" (without context)
            - "Excellent communication skills" (without examples)

            ANALYSIS CRITERIA:
            1. Identify overused, generic phrases that add no value
            2. Look for unsupported claims without evidence
            3. Find vague language that could apply to anyone
            4. Check for corporate jargon that obscures meaning
            5. Assess specificity vs. generic statements

            SCORING CRITERIA (1-10):
            - 9-10: No buzzwords, all specific and meaningful language
            - 7-8: Minimal buzzwords, mostly concrete language
            - 5-6: Some buzzwords mixed with good content
            - 3-4: Many buzzwords, generic language
            - 1-2: Predominantly buzzwords and clichés

            Respond in this exact JSON format:
            {{
              "section_name": "buzzwords_cliches",
              "ats_score": 0,
              "feedback": ["detailed analysis of buzzwords and clichés usage"],
              "issues_found": ["specific buzzwords and clichés identified"],
              "corrections": ["better alternatives to the buzzwords"],
              "improved_content": ["rewritten content without buzzwords"],
              "examples": ["examples of specific, meaningful alternatives"]
            }}
            """
            
        elif section_name == "unnecessary_sections":
            return f"""
            You are an expert resume analyst specializing in resume structure and section relevance.

            Resume Data: {resume_json}

            TASK: Evaluate the relevance and necessity of all resume sections for ATS optimization and recruiter appeal.

            SECTION RELEVANCE ANALYSIS:
            1. Essential sections: Contact Info, Summary/Objective, Work Experience, Education, Skills
            2. Valuable sections: Projects, Certifications, Languages (if relevant)
            3. Questionable sections: Hobbies, Interests, References, Personal Information
            4. Context-dependent: Awards, Volunteer Experience, Publications

            SPECIFIC EVALUATION CRITERIA:
            1. Does each section add professional value?
            2. Is the content relevant to the target role?
            3. Are sections properly prioritized by importance?
            4. Is there any outdated or irrelevant information?
            5. Are there missing sections that should be included?
            6. Is the resume length appropriate for the experience level?

            SECTION-SPECIFIC GUIDELINES:
            - Hobbies/Interests: Only include if directly relevant to job
            - References: Usually unnecessary ("available upon request")
            - Objectives: Often redundant if there's a good summary
            - Personal info: Age, marital status, photo (avoid in most countries)
            - Volunteer work: Include if relevant or shows leadership

            SCORING CRITERIA (1-10):
            - 9-10: All sections highly relevant, perfect structure
            - 7-8: Mostly relevant sections, minor improvements needed
            - 5-6: Some irrelevant content, needs restructuring
            - 3-4: Many irrelevant sections, poor prioritization
            - 1-2: Poorly structured, many unnecessary sections

            Respond in this exact JSON format:
            {{
              "section_name": "unnecessary_sections",
              "ats_score": 0,
              "feedback": ["detailed analysis of section relevance and structure"],
              "issues_found": ["unnecessary or poorly positioned sections"],
              "missing_information": ["important sections that should be added"],
              "recommendations": ["suggestions for section improvement and reorganization"]
            }}
            """
            
        elif section_name == "contact_details":
            return f"""
            You are an expert resume analyst specializing in contact information optimization and professional presentation.

            Resume Data: {resume_json}

            TASK: Evaluate the completeness, professionalism, and ATS-friendliness of contact information.

            CONTACT INFORMATION ANALYSIS:
            1. Required: Full name, professional email, phone number
            2. Highly recommended: LinkedIn profile, location (city, state)
            3. Optional but valuable: GitHub (for tech roles), portfolio website
            4. Avoid: Full address, personal social media, unprofessional emails

            SPECIFIC EVALUATION CRITERIA:
            1. Email professionalism (firstname.lastname@email.com preferred)
            2. Phone number format and completeness
            3. LinkedIn profile presence and URL cleanliness
            4. Location information (city/state sufficient)
            5. GitHub/portfolio relevance to role
            6. Overall contact section formatting and clarity

            COMMON ISSUES:
            - Unprofessional email addresses (hotguy2000@email.com)
            - Missing country code for international numbers
            - Broken or long LinkedIn URLs
            - Too much personal information (full address, age)
            - Missing essential contact methods

            SCORING CRITERIA (1-10):
            - 9-10: Complete, professional contact info, all relevant links
            - 7-8: Good contact info, minor improvements possible
            - 5-6: Basic contact info present, some issues
            - 3-4: Incomplete or unprofessional contact info
            - 1-2: Major contact information problems

            Respond in this exact JSON format:
            {{
              "section_name": "contact_details",
              "ats_score": 0,
              "feedback": ["detailed analysis of contact information quality"],
              "contact_completeness": {{
                "email": true,
                "phone": true,
                "linkedin": false,
                "github": false,
                "portfolio": false,
                "location": true
              }},
              "issues_found": ["problems with current contact information"],
              "recommendations": ["suggestions for improving contact section"]
            }}
            """
        elif section_name == "grammar_spelling":
            return f"""
            You are an expert resume analyst and professional editor specializing in grammar, spelling, and language quality.

            Resume Data: {resume_json}

            TASK: Conduct a thorough grammar and spelling analysis of the entire resume content.

            SPECIFIC ANALYSIS CRITERIA:
            1. Grammar errors: Subject-verb agreement, tense consistency, sentence structure
            2. Spelling mistakes: Typos, commonly misspelled words, technical terms
            3. Punctuation issues: Comma usage, apostrophes, periods in bullet points
            4. Capitalization: Proper nouns, job titles, company names, section headers
            5. Language consistency: American vs. British English, technical terminology
            6. Sentence construction: Run-on sentences, fragments, clarity issues

            COMMON RESUME GRAMMAR ISSUES:
            - Inconsistent tense usage (mixing past and present tense)
            - Missing articles (a, an, the) where needed
            - Incorrect apostrophe usage (it's vs. its)
            - Capitalization inconsistencies
            - Bullet point punctuation inconsistencies
            - Spelling errors in technical terms or company names

            SCORING CRITERIA (1-10):
            - 9-10: Perfect grammar and spelling throughout
            - 7-8: Minor errors, generally well-written
            - 5-6: Several errors but mostly readable
            - 3-4: Many errors affecting readability
            - 1-2: Numerous errors, poor language quality

            Respond in this exact JSON format:
            {{
              "section_name": "grammar_spelling",
              "ats_score": 0,
              "feedback": ["detailed analysis of grammar and spelling quality"],
              "grammar_errors": ["specific grammar mistakes found"],
              "spelling_errors": ["spelling mistakes identified"],
              "corrections": ["corrected versions of problematic text"],
              "improved_content": ["improved sentences with better grammar and clarity"]
            }}
            """
            
        elif section_name == "formatting_layout":
            return f"""
            You are an expert resume analyst specializing in formatting, layout, and visual presentation for ATS compatibility.

            Resume Data: {resume_json}

            TASK: Analyze the formatting and layout structure for ATS readability and professional presentation.

            SPECIFIC ANALYSIS CRITERIA:
            1. Section organization and logical flow
            2. Consistency in formatting (fonts, bullet points, spacing)
            3. ATS-friendly structure (clear headers, simple formatting)
            4. Professional appearance and readability
            5. Proper use of white space and visual hierarchy
            6. Consistency in date formats, bullet styles, and alignment

            ATS-FRIENDLY FORMATTING GUIDELINES:
            - Use standard fonts (Arial, Calibri, Times New Roman)
            - Avoid complex formatting (tables, columns, graphics)
            - Use consistent bullet points throughout
            - Clear section headers in standard format
            - Proper spacing between sections
            - Left-aligned text for better ATS parsing

            COMMON FORMATTING ISSUES:
            - Inconsistent bullet point styles
            - Poor section organization
            - Overly complex layouts
            - Inconsistent spacing and alignment
            - Mixed formatting styles within sections
            - Headers that may confuse ATS systems

            SCORING CRITERIA (1-10):
            - 9-10: Perfect formatting, ATS-friendly, professional
            - 7-8: Good formatting with minor inconsistencies
            - 5-6: Decent formatting but some issues
            - 3-4: Poor formatting, ATS compatibility issues
            - 1-2: Major formatting problems, unprofessional appearance

            Respond in this exact JSON format:
            {{
              "section_name": "formatting_layout",
              "ats_score": 0,
              "feedback": ["detailed analysis of formatting and layout quality"],
              "formatting_issues": ["specific formatting problems identified"],
              "recommendations": ["suggestions for improving formatting and layout"],
              "examples": ["examples of better formatting approaches"]
            }}
            """
            
        elif section_name == "ats_keywords":
            return f"""
            You are an expert resume analyst specializing in ATS keyword optimization and industry-specific terminology.

            Resume Data: {resume_json}

            TASK: Analyze keyword usage and optimization for ATS systems and recruiter searches.

            SPECIFIC ANALYSIS CRITERIA:
            1. Industry-specific keywords and technical terms
            2. Job title variations and role-related terminology
            3. Skills and competency keywords
            4. Technology, tools, and software mentions
            5. Certification and qualification keywords
            6. Action verbs that ATS systems favor
            7. Keyword density and natural integration

            KEYWORD OPTIMIZATION STRATEGIES:
            - Include exact job title variations from target roles
            - Use both acronyms and full forms (AI, Artificial Intelligence)
            - Include industry-standard terminology
            - Mention specific technologies, tools, and methodologies
            - Use keywords naturally within context
            - Include soft skills that are commonly searched

            ANALYSIS FOCUS AREAS:
            - Technical skills vs. job requirements
            - Industry buzzwords and standard terminology
            - Certification and education keywords
            - Geographic and location-based terms
            - Experience level indicators
            - Domain-specific language

            SCORING CRITERIA (1-10):
            - 9-10: Excellent keyword optimization, natural integration
            - 7-8: Good keyword usage, minor gaps
            - 5-6: Adequate keywords but missing key terms
            - 3-4: Poor keyword optimization, generic language
            - 1-2: Minimal relevant keywords, poor ATS optimization

            Respond in this exact JSON format:
            {{
              "section_name": "ats_keywords",
              "ats_score": 0,
              "feedback": ["detailed analysis of keyword optimization"],
              "missing_keywords": ["important keywords missing from resume"],
              "relevant_keywords": ["good keywords already present"],
              "recommendations": ["suggestions for keyword improvement"],
              "improved_content": ["examples of keyword-optimized content"]
            }}
            """
            
        elif section_name == "skills_relevance":
            return f"""
            You are an expert resume analyst specializing in skills assessment and relevance evaluation.

            Resume Data: {resume_json}

            TASK: Analyze the skills section for relevance, organization, and completeness.

            SPECIFIC ANALYSIS CRITERIA:
            1. Technical skills relevance to target roles
            2. Skills organization and categorization
            3. Balance between hard and soft skills
            4. Currency and demand of listed skills
            5. Skills progression and expertise levels
            6. Missing critical skills for the field
            7. Outdated or irrelevant skills inclusion

            SKILLS EVALUATION FRAMEWORK:
            - Technical Skills: Programming languages, software, tools, platforms
            - Soft Skills: Leadership, communication, problem-solving
            - Industry Skills: Domain-specific knowledge and expertise
            - Certification Skills: Validated competencies
            - Language Skills: Proficiency levels and relevance

            SKILLS ORGANIZATION BEST PRACTICES:
            - Group similar skills together
            - Prioritize most relevant skills first
            - Include proficiency levels where appropriate
            - Remove outdated technologies
            - Balance technical and soft skills

            SCORING CRITERIA (1-10):
            - 9-10: Highly relevant, well-organized, comprehensive skills
            - 7-8: Good skills selection with minor improvements needed
            - 5-6: Decent skills but poor organization or some irrelevant items
            - 3-4: Poorly organized, many irrelevant or outdated skills
            - 1-2: Inadequate skills section, major problems

            Respond in this exact JSON format:
            {{
              "section_name": "skills_relevance",
              "ats_score": 0,
              "feedback": ["detailed analysis of skills relevance and organization"],
              "issues_found": ["problems with current skills presentation"],
              "missing_information": ["important skills that should be added"],
              "recommendations": ["suggestions for skills section improvement"],
              "improved_content": ["better ways to organize and present skills"]
            }}
            """
            
        elif section_name == "achievements_vs_responsibilities":
            return f"""
            You are an expert resume analyst specializing in distinguishing achievements from basic job responsibilities.

            Resume Data: {resume_json}

            TASK: Analyze the balance between achievements and responsibilities, identifying areas for improvement.

            SPECIFIC ANALYSIS CRITERIA:
            1. Achievement-focused vs. duty-focused language
            2. Impact-driven statements vs. task descriptions
            3. Results-oriented content vs. process descriptions
            4. Value-added contributions vs. basic job functions
            5. Leadership and initiative examples vs. routine tasks
            6. Problem-solving achievements vs. maintenance activities

            ACHIEVEMENT INDICATORS:
            - Quantifiable results and outcomes
            - Awards, recognition, and promotions
            - Process improvements and innovations
            - Team leadership and mentoring
            - Revenue impact and cost savings
            - Efficiency gains and productivity improvements

            RESPONSIBILITY INDICATORS (TO MINIMIZE):
            - "Responsible for..." statements
            - Daily task descriptions
            - Basic job function listings
            - Routine maintenance activities
            - Generic duty descriptions
            - Process following without improvement

            TRANSFORMATION EXAMPLES:
            - Responsibility: "Managed customer accounts"
            - Achievement: "Managed 50+ customer accounts, increasing retention by 25%"
            - Responsibility: "Developed software applications"
            - Achievement: "Developed 3 software applications that reduced processing time by 40%"

            SCORING CRITERIA (1-10):
            - 9-10: Strong focus on achievements, quantified results
            - 7-8: Good mix with more achievements than responsibilities
            - 5-6: Balanced but could emphasize more achievements
            - 3-4: More responsibilities than achievements
            - 1-2: Predominantly responsibilities, minimal achievements

            Respond in this exact JSON format:
            {{
              "section_name": "achievements_vs_responsibilities",
              "ats_score": 0,
              "feedback": ["detailed analysis of achievements vs responsibilities balance"],
              "weak_sentences": ["responsibility-focused statements that need improvement"],
              "strong_sentences": ["achievement-focused statements that work well"],
              "improved_content": ["transformed statements emphasizing achievements"],
              "examples": ["examples of strong achievement-focused language"]
            }}
            """
            
        elif section_name == "education_clarity":
            return f"""
            You are an expert resume analyst specializing in education section optimization and clarity.

            Resume Data: {resume_json}

            TASK: Analyze the education section for completeness, relevance, and proper presentation.

            SPECIFIC ANALYSIS CRITERIA:
            1. Degree information completeness (degree type, major, institution)
            2. Date format consistency and logical chronology
            3. GPA inclusion (include if 3.5+ and recent graduate)
            4. Relevant coursework, honors, and achievements
            5. Education prioritization vs. experience level
            6. Missing educational credentials
            7. International degree recognition and clarity

            EDUCATION SECTION BEST PRACTICES:
            - Most recent education first (reverse chronological)
            - Include degree type, major, institution, location, graduation year
            - Add relevant coursework for entry-level positions
            - Include academic honors, scholarships, distinctions
            - Remove high school if college degree is present
            - Consider GPA inclusion based on relevance and strength

            COMMON EDUCATION ISSUES:
            - Incomplete degree information
            - Inconsistent date formatting
            - Missing graduation dates
            - Irrelevant educational details
            - Poor prioritization of multiple degrees
            - Unclear international credentials

            SCORING CRITERIA (1-10):
            - 9-10: Complete, well-organized, relevant education information
            - 7-8: Good education section with minor improvements needed
            - 5-6: Adequate education info but some clarity issues
            - 3-4: Incomplete or poorly organized education section
            - 1-2: Major problems with education presentation

            Respond in this exact JSON format:
            {{
              "section_name": "education_clarity",
              "ats_score": 0,
              "feedback": ["detailed analysis of education section clarity and completeness"],
              "issues_found": ["problems in education section presentation"],
              "missing_information": ["important education details that should be added"],
              "recommendations": ["suggestions for education section improvement"],
              "corrections": ["corrected education entries with proper formatting"]
            }}
            """
            
        else:
            # Default fallback for any other section
            return f"""
            You are an expert resume analyst specializing in comprehensive resume evaluation.

            Resume Data: {resume_json}

            TASK: Analyze the resume focusing on {section_name.replace('_', ' ')} and provide detailed feedback.

            ANALYSIS CRITERIA:
            1. Evaluate the specific aspect requested
            2. Identify strengths and weaknesses
            3. Provide actionable improvement suggestions
            4. Consider ATS optimization factors
            5. Assess professional presentation quality

            SCORING CRITERIA (1-10):
            - 9-10: Excellent performance in this area
            - 7-8: Good performance with minor improvements needed
            - 5-6: Average performance, several improvements possible
            - 3-4: Below average, significant improvements needed
            - 1-2: Poor performance, major overhaul required

            Respond in this exact JSON format:
            {{
              "section_name": "{section_name}",
              "ats_score": 0,
              "feedback": ["detailed analysis of the requested aspect"],
              "issues_found": ["problems identified in this area"],
              "recommendations": ["suggestions for improvement"]
            }}

            """

