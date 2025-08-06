import openai
import os
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class EnhancedOpenAIService:
    """Enhanced OpenAI service for hybrid ATS checker with GPT-3.5 turbo support"""
    
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        openai.api_key = self.api_key
        self.model = "gpt-3.5-turbo"  # Using GPT-3.5 turbo as requested
    
    async def analyze_section_with_gpt(self, section: str, resume_data: Dict[str, Any], 
                                     prompt: str) -> Dict[str, Any]:
        """Analyze a specific section using GPT-3.5 turbo"""
        
        try:
            # Prepare the analysis prompt
            analysis_prompt = f"""
            You are an expert ATS (Applicant Tracking System) analyst. 
            
            {prompt}
            
            Resume Data:
            {json.dumps(resume_data, indent=2)}
            
            Please provide a detailed analysis including:
            1. Strengths and weaknesses
            2. Specific recommendations for improvement
            3. Examples of better content
            4. ATS optimization tips
            5. Score out of 10 with justification
            
            Focus on {section} specifically.
            """
            
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert ATS analyst specializing in resume optimization."},
                    {"role": "user", "content": analysis_prompt}
                ],
                max_tokens=1000,
                temperature=0.3
            )
            
            analysis_text = response.choices[0].message.content
            
            # Parse the analysis into structured format
            structured_analysis = self._parse_gpt_analysis(analysis_text, section)
            
            return {
                "analysis": structured_analysis,
                "raw_response": analysis_text,
                "model_used": self.model,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"GPT analysis failed for section {section}: {str(e)}")
            return {
                "error": f"GPT analysis failed: {str(e)}",
                "analysis": {
                    "strengths": [],
                    "weaknesses": [],
                    "recommendations": [],
                    "examples": [],
                    "score": 0,
                    "justification": "Analysis failed due to technical error"
                }
            }
    
    async def generate_section_content(self, section: str, description: str, 
                                     resume_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate content for a specific section using GPT-3.5 turbo"""
        
        try:
            # Prepare the generation prompt
            generation_prompt = f"""
            You are an expert resume writer specializing in ATS optimization.
            
            Generate content for the {section} section based on this description:
            {description}
            
            """
            
            if resume_data:
                generation_prompt += f"""
                Context from existing resume:
                {json.dumps(resume_data, indent=2)}
                
                Please ensure the new content is consistent with the existing resume style and information.
                """
            
            generation_prompt += """
            Requirements:
            1. Use strong action verbs
            2. Include quantifiable achievements where possible
            3. Optimize for ATS keyword matching
            4. Keep content concise and impactful
            5. Avoid buzzwords and clichés
            6. Focus on achievements rather than just responsibilities
            
            Provide the generated content in a clear, professional format.
            """
            
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert resume writer specializing in ATS optimization."},
                    {"role": "user", "content": generation_prompt}
                ],
                max_tokens=800,
                temperature=0.4
            )
            
            generated_content = response.choices[0].message.content
            
            return {
                "generated_content": generated_content,
                "section": section,
                "model_used": self.model,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Content generation failed for section {section}: {str(e)}")
            return {
                "error": f"Content generation failed: {str(e)}",
                "generated_content": "Unable to generate content due to technical error"
            }
    
    async def suggest_relevant_skills(self, resume_data: Dict[str, Any], 
                                   target_role: str = None) -> Dict[str, Any]:
        """Suggest relevant skills based on resume data and target role"""
        
        try:
            prompt = f"""
            You are an expert career advisor specializing in skill optimization for ATS systems.
            
            Based on this resume data:
            {json.dumps(resume_data, indent=2)}
            
            """
            
            if target_role:
                prompt += f"Target role: {target_role}\n\n"
            
            prompt += """
            Please suggest:
            1. Technical skills that would enhance the resume
            2. Soft skills that are relevant
            3. Industry-specific keywords
            4. Emerging technologies to consider
            5. Skills that are in high demand
            
            Focus on skills that would improve ATS keyword matching and make the candidate more competitive.
            """
            
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert career advisor specializing in skill optimization."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=600,
                temperature=0.3
            )
            
            suggestions_text = response.choices[0].message.content
            
            # Parse suggestions into structured format
            structured_suggestions = self._parse_skill_suggestions(suggestions_text)
            
            return {
                "suggestions": structured_suggestions,
                "raw_response": suggestions_text,
                "model_used": self.model,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Skill suggestions failed: {str(e)}")
            return {
                "error": f"Skill suggestions failed: {str(e)}",
                "suggestions": {
                    "technical_skills": [],
                    "soft_skills": [],
                    "keywords": [],
                    "emerging_technologies": [],
                    "high_demand_skills": []
                }
            }
    
    async def optimize_section(self, section: str, current_content: str, 
                             resume_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Optimize a specific section for ATS compatibility"""
        
        try:
            prompt = f"""
            You are an expert ATS optimization specialist.
            
            Current content for {section}:
            {current_content}
            
            """
            
            if resume_data:
                prompt += f"""
                Full resume context:
                {json.dumps(resume_data, indent=2)}
                
                """
            
            prompt += """
            Please optimize this content for ATS systems by:
            1. Improving keyword density
            2. Using stronger action verbs
            3. Adding quantifiable achievements
            4. Removing buzzwords and clichés
            5. Ensuring proper formatting
            6. Making content more impactful
            
            Provide the optimized version with explanations of changes made.
            """
            
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert ATS optimization specialist."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.3
            )
            
            optimization_text = response.choices[0].message.content
            
            # Parse optimization into structured format
            structured_optimization = self._parse_optimization(optimization_text)
            
            return {
                "optimization": structured_optimization,
                "raw_response": optimization_text,
                "model_used": self.model,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Section optimization failed for {section}: {str(e)}")
            return {
                "error": f"Section optimization failed: {str(e)}",
                "optimization": {
                    "optimized_content": current_content,
                    "changes_made": [],
                    "explanations": ["Optimization failed due to technical error"]
                }
            }
    
    def _parse_gpt_analysis(self, analysis_text: str, section: str) -> Dict[str, Any]:
        """Parse GPT analysis response into structured format"""
        
        # Simple parsing - in a real implementation, you might use more sophisticated parsing
        analysis = {
            "strengths": [],
            "weaknesses": [],
            "recommendations": [],
            "examples": [],
            "score": 0,
            "justification": ""
        }
        
        # Extract score if present
        if "score" in analysis_text.lower():
            try:
                # Look for score patterns like "score: 8/10" or "8 out of 10"
                import re
                score_match = re.search(r'(\d+)/10|(\d+)\s+out\s+of\s+10|score[:\s]*(\d+)', analysis_text.lower())
                if score_match:
                    score = int(score_match.group(1) or score_match.group(2) or score_match.group(3))
                    analysis["score"] = min(10, max(0, score))
            except:
                pass
        
        # Extract other components (simplified)
        lines = analysis_text.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if any(keyword in line.lower() for keyword in ['strength', 'strong']):
                current_section = 'strengths'
            elif any(keyword in line.lower() for keyword in ['weakness', 'weak', 'improve']):
                current_section = 'weaknesses'
            elif any(keyword in line.lower() for keyword in ['recommend', 'suggestion']):
                current_section = 'recommendations'
            elif any(keyword in line.lower() for keyword in ['example', 'instance']):
                current_section = 'examples'
            elif line and current_section and line.startswith(('-', '•', '*', '1.', '2.')):
                analysis[current_section].append(line.lstrip('-•*1234567890. '))
        
        return analysis
    
    def _parse_skill_suggestions(self, suggestions_text: str) -> Dict[str, Any]:
        """Parse skill suggestions into structured format"""
        
        suggestions = {
            "technical_skills": [],
            "soft_skills": [],
            "keywords": [],
            "emerging_technologies": [],
            "high_demand_skills": []
        }
        
        # Simple parsing - extract skills from the text
        lines = suggestions_text.split('\n')
        current_category = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if 'technical' in line.lower():
                current_category = 'technical_skills'
            elif 'soft' in line.lower():
                current_category = 'soft_skills'
            elif 'keyword' in line.lower():
                current_category = 'keywords'
            elif 'emerging' in line.lower():
                current_category = 'emerging_technologies'
            elif 'demand' in line.lower():
                current_category = 'high_demand_skills'
            elif line and current_category and line.startswith(('-', '•', '*', '1.', '2.')):
                suggestions[current_category].append(line.lstrip('-•*1234567890. '))
        
        return suggestions
    
    def _parse_optimization(self, optimization_text: str) -> Dict[str, Any]:
        """Parse optimization response into structured format"""
        
        optimization = {
            "optimized_content": "",
            "changes_made": [],
            "explanations": []
        }
        
        # Simple parsing - extract optimized content and changes
        lines = optimization_text.split('\n')
        in_optimized_content = False
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if 'optimized' in line.lower() or 'improved' in line.lower():
                in_optimized_content = True
            elif line.startswith(('-', '•', '*', '1.', '2.')):
                if in_optimized_content:
                    optimization["changes_made"].append(line.lstrip('-•*1234567890. '))
                else:
                    optimization["explanations"].append(line.lstrip('-•*1234567890. '))
            elif in_optimized_content and line:
                optimization["optimized_content"] += line + "\n"
        
        return optimization
    
    async def check_grammar_spelling(self, text: str, language: str = "UK") -> Dict[str, Any]:
        """Check grammar and spelling with specific language standards"""
        
        try:
            prompt = f"""
            You are an expert grammar and spelling checker specializing in {language} English.
            
            Please check the following text for:
            1. Grammar errors
            2. Spelling mistakes
            3. Punctuation issues
            4. Style improvements
            5. {language} English specific corrections
            
            Text to check:
            {text}
            
            Provide corrections with explanations for each issue found.
            """
            
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {"role": "system", "content": f"You are an expert grammar and spelling checker for {language} English."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.2
            )
            
            corrections_text = response.choices[0].message.content
            
            return {
                "corrections": self._parse_corrections(corrections_text),
                "raw_response": corrections_text,
                "language": language,
                "model_used": self.model,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Grammar/spelling check failed: {str(e)}")
            return {
                "error": f"Grammar/spelling check failed: {str(e)}",
                "corrections": {
                    "grammar_errors": [],
                    "spelling_errors": [],
                    "punctuation_errors": [],
                    "style_improvements": []
                }
            }
    
    def _parse_corrections(self, corrections_text: str) -> Dict[str, Any]:
        """Parse grammar/spelling corrections into structured format"""
        
        corrections = {
            "grammar_errors": [],
            "spelling_errors": [],
            "punctuation_errors": [],
            "style_improvements": []
        }
        
        # Simple parsing
        lines = corrections_text.split('\n')
        current_category = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if 'grammar' in line.lower():
                current_category = 'grammar_errors'
            elif 'spelling' in line.lower():
                current_category = 'spelling_errors'
            elif 'punctuation' in line.lower():
                current_category = 'punctuation_errors'
            elif 'style' in line.lower():
                current_category = 'style_improvements'
            elif line and current_category and line.startswith(('-', '•', '*', '1.', '2.')):
                corrections[current_category].append(line.lstrip('-•*1234567890. '))
        
        return corrections 