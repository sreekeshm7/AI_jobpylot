from typing import Dict, Any, List
from .openai_service import OpenAIService
import json

class ResumeAnalyzer:
    def __init__(self):
        self.openai_service = OpenAIService()
        self.evaluation_sections = [
            "quantifiable_impact",
            "date_format", 
            "weak_verbs",
            "teamwork_collaboration",
            "buzzwords_cliches",
            "unnecessary_sections",
            "contact_details",
            "grammar_spelling",
            "formatting_layout",
            "ats_keywords",
            "skills_relevance",
            "achievements_vs_responsibilities",
            "education_clarity"
        ]
    
    def analyze_complete_resume(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform complete resume analysis across all sections
        """
        try:
            results = {
                "summary_evaluation": self.openai_service.evaluate_summary(resume_data),
                "section_evaluations": {}
            }
            
            # Evaluate each section
            for section in self.evaluation_sections:
                try:
                    results["section_evaluations"][section] = self.openai_service.evaluate_section(
                        resume_data, section
                    )
                except Exception as e:
                    results["section_evaluations"][section] = {
                        "section_name": section,
                        "ats_score": 0,
                        "feedback": [f"Failed to evaluate {section}: {str(e)}"],
                        "error": str(e)
                    }
            
            # Calculate overall score
            results["overall_analysis"] = self._calculate_overall_score(results)
            
            return results
            
        except Exception as e:
            raise Exception(f"Error in complete resume analysis: {str(e)}")
    
    def _calculate_overall_score(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate overall resume score based on all section evaluations
        """
        try:
            scores = []
            
            # Add summary score
            summary_eval = analysis_results.get("summary_evaluation", {})
            if "ats_score" in summary_eval and isinstance(summary_eval["ats_score"], (int, float)):
                scores.append(summary_eval["ats_score"])
            
            # Add section scores
            for section_name, section_data in analysis_results.get("section_evaluations", {}).items():
                if isinstance(section_data, dict) and "ats_score" in section_data:
                    if isinstance(section_data["ats_score"], (int, float)):
                        scores.append(section_data["ats_score"])
            
            if not scores:
                return {"overall_score": 0, "total_sections": 0, "message": "No scores available"}
            
            overall_score = sum(scores) / len(scores)
            
            # Generate overall feedback
            feedback = self._generate_overall_feedback(overall_score, analysis_results)
            
            return {
                "overall_score": round(overall_score, 1),
                "total_sections": len(scores),
                "grade": self._get_grade(overall_score),
                "feedback": feedback,
                "improvement_priority": self._get_improvement_priorities(analysis_results)
            }
            
        except Exception as e:
            return {"error": f"Error calculating overall score: {str(e)}"}
    
    def _get_grade(self, score: float) -> str:
        """Convert numeric score to letter grade"""
        if score >= 9.0:
            return "A+"
        elif score >= 8.5:
            return "A"
        elif score >= 8.0:
            return "A-"
        elif score >= 7.5:
            return "B+"
        elif score >= 7.0:
            return "B"
        elif score >= 6.5:
            return "B-"
        elif score >= 6.0:
            return "C+"
        elif score >= 5.5:
            return "C"
        elif score >= 5.0:
            return "C-"
        elif score >= 4.0:
            return "D"
        else:
            return "F"
    
    def _generate_overall_feedback(self, score: float, analysis_results: Dict[str, Any]) -> List[str]:
        """Generate overall feedback based on analysis results"""
        feedback = []
        
        if score >= 8.5:
            feedback.append("Excellent resume with strong ATS optimization")
        elif score >= 7.0:
            feedback.append("Good resume with minor areas for improvement")
        elif score >= 5.5:
            feedback.append("Average resume that needs several improvements")
        else:
            feedback.append("Resume needs significant improvements for ATS optimization")
        
        # Add specific feedback based on lowest scoring sections
        low_scores = []
        for section_name, section_data in analysis_results.get("section_evaluations", {}).items():
            if isinstance(section_data, dict) and "ats_score" in section_data:
                if isinstance(section_data["ats_score"], (int, float)) and section_data["ats_score"] < 6:
                    low_scores.append((section_name, section_data["ats_score"]))
        
        if low_scores:
            low_scores.sort(key=lambda x: x[1])  # Sort by score
            feedback.append(f"Priority improvements needed in: {', '.join([s[0].replace('_', ' ').title() for s in low_scores[:3]])}")
        
        return feedback
    
    def _get_improvement_priorities(self, analysis_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get prioritized list of improvements"""
        section_scores = []
        
        # Add summary
        summary_eval = analysis_results.get("summary_evaluation", {})
        if "ats_score" in summary_eval and isinstance(summary_eval["ats_score"], (int, float)):
            section_scores.append({
                "section": "Summary",
                "score": summary_eval["ats_score"],
                "feedback": summary_eval.get("score_feedback", summary_eval.get("feedback", []))
            })
        
        # Add other sections
        for section_name, section_data in analysis_results.get("section_evaluations", {}).items():
            if isinstance(section_data, dict) and "ats_score" in section_data:
                if isinstance(section_data["ats_score"], (int, float)):
                    section_scores.append({
                        "section": section_name.replace('_', ' ').title(),
                        "score": section_data["ats_score"],
                        "feedback": section_data.get("feedback", [])
                    })
        
        # Sort by score (lowest first) and return top 5 priorities
        section_scores.sort(key=lambda x: x["score"])
        
        return section_scores[:5]
    
    def generate_improvement_report(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a comprehensive improvement report
        """
        try:
            analysis = self.analyze_complete_resume(resume_data)
            
            # Extract all sentences/issues from different field types
            all_weak_sentences = []
            all_strong_sentences = []
            all_improvements = []
            all_issues = []
            
            # From summary
            summary_eval = analysis.get("summary_evaluation", {})
            if "weak_sentences" in summary_eval and summary_eval["weak_sentences"]:
                all_weak_sentences.extend(summary_eval["weak_sentences"])
            if "strong_sentences" in summary_eval and summary_eval["strong_sentences"]:
                all_strong_sentences.extend(summary_eval["strong_sentences"])
            if "new_summaries" in summary_eval and summary_eval["new_summaries"]:
                all_improvements.extend(summary_eval["new_summaries"])
            
            # From sections - handle different field types
            for section_data in analysis.get("section_evaluations", {}).values():
                if isinstance(section_data, dict):
                    # Weak sentences
                    if "weak_sentences" in section_data and section_data["weak_sentences"]:
                        all_weak_sentences.extend(section_data["weak_sentences"])
                    
                    # Strong sentences
                    if "strong_sentences" in section_data and section_data["strong_sentences"]:
                        all_strong_sentences.extend(section_data["strong_sentences"])
                    
                    # Improvements (various field names)
                    for field in ["improved_content", "corrections", "recommendations"]:
                        if field in section_data and section_data[field]:
                            all_improvements.extend(section_data[field])
                    
                    # Issues (various field names)
                    for field in ["issues_found", "date_issues", "grammar_errors", "spelling_errors", "formatting_issues", "missing_keywords"]:
                        if field in section_data and section_data[field]:
                            all_issues.extend(section_data[field])
            
            return {
                "overall_analysis": analysis.get("overall_analysis", {}),
                "total_weak_points": len(all_weak_sentences),
                "total_strong_points": len(all_strong_sentences),
                "total_issues_found": len(all_issues),
                "improvement_suggestions": len(all_improvements),
                "detailed_analysis": analysis,
                "action_items": self._generate_action_items(analysis)
            }
            
        except Exception as e:
            raise Exception(f"Error generating improvement report: {str(e)}")
    
    def _generate_action_items(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate specific action items for resume improvement"""
        action_items = []
        
        # Get priority improvements
        priorities = analysis.get("overall_analysis", {}).get("improvement_priority", [])
        
        for priority in priorities[:3]:  # Top 3 priorities
            section = priority.get("section", "")
            score = priority.get("score", 0)
            
            if score < 5:
                action_items.append(f"URGENT: Completely revise {section} section (Score: {score}/10)")
            elif score < 7:
                action_items.append(f"HIGH: Improve {section} section (Score: {score}/10)")
            else:
                action_items.append(f"MEDIUM: Fine-tune {section} section (Score: {score}/10)")
        
        return action_items