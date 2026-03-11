import json
import logging
from typing import Dict, List, Any
from services.gemini_service import generate_structured_response, generate_ai_response

class InterviewAgent:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Interview questions by role and difficulty
        self.interview_questions = {
            "software_engineer": {
                "technical": [
                    "Explain the difference between REST and GraphQL APIs.",
                    "How would you optimize database queries for a large-scale application?",
                    "Describe the software development lifecycle you follow.",
                    "How do you ensure code quality in your projects?",
                    "Explain the concept of microservices architecture.",
                    "How would you handle a production bug that affects users?",
                    "Describe your experience with version control systems.",
                    "How do you approach debugging complex issues?",
                    "Explain the importance of testing in software development.",
                    "How do you stay updated with new technologies?"
                ],
                "behavioral": [
                    "Tell me about a challenging project you worked on.",
                    "How do you handle conflicts with team members?",
                    "Describe a time when you had to learn a new technology quickly.",
                    "How do you prioritize tasks when working on multiple projects?",
                    "Tell me about a time you made a mistake and how you fixed it.",
                    "How do you handle tight deadlines?",
                    "Describe your ideal work environment.",
                    "How do you contribute to team culture?",
                    "Tell me about a time you mentored someone.",
                    "How do you handle constructive criticism?"
                ],
                "problem_solving": [
                    "Design a URL shortening service like bit.ly.",
                    "How would you implement a real-time chat application?",
                    "Design a system for handling millions of requests per day.",
                    "How would you detect and prevent SQL injection attacks?",
                    "Design a recommendation system for an e-commerce platform.",
                    "How would you implement a caching layer?",
                    "Design a user authentication system.",
                    "How would you handle data migration for a large application?",
                    "Design a logging system for a distributed application.",
                    "How would you implement rate limiting for an API?"
                ]
            },
            "data_scientist": {
                "technical": [
                    "Explain the difference between supervised and unsupervised learning.",
                    "How do you handle missing data in a dataset?",
                    "Describe the bias-variance tradeoff.",
                    "How do you evaluate the performance of a machine learning model?",
                    "Explain the concept of feature engineering.",
                    "How would you handle imbalanced datasets?",
                    "Describe the difference between precision and recall.",
                    "How do you prevent overfitting in neural networks?",
                    "Explain the concept of ensemble methods.",
                    "How do you deploy machine learning models to production?"
                ],
                "behavioral": [
                    "Tell me about a data science project that had business impact.",
                    "How do you communicate complex technical concepts to non-technical stakeholders?",
                    "Describe a time when your analysis led to unexpected insights.",
                    "How do you ensure data privacy and ethics in your work?",
                    "Tell me about a time when you had to work with messy data.",
                    "How do you approach feature selection?",
                    "Describe your experience with A/B testing.",
                    "How do you collaborate with engineering teams?",
                    "Tell me about a time when your model failed in production.",
                    "How do you stay updated with the latest ML research?"
                ],
                "problem_solving": [
                    "How would you build a customer churn prediction model?",
                    "Design a system for real-time fraud detection.",
                    "How would you analyze user engagement data?",
                    "Design a recommendation algorithm for a streaming service.",
                    "How would you detect anomalies in time series data?",
                    "Design a system for sentiment analysis of customer reviews.",
                    "How would you build a system for image classification?",
                    "Design an A/B testing framework for a website.",
                    "How would you optimize a machine learning pipeline?",
                    "Design a system for personalizing user experiences."
                ]
            },
            "product_manager": {
                "technical": [
                    "How do you prioritize features in a product roadmap?",
                    "Describe your experience with A/B testing and product analytics.",
                    "How do you work with engineering teams to define technical requirements?",
                    "Explain how you measure product success.",
                    "How do you handle technical debt in product decisions?",
                    "Describe your experience with API design.",
                    "How do you approach product scalability?",
                    "Explain your understanding of system architecture.",
                    "How do you evaluate new technologies for product use?",
                    "Describe your experience with product documentation."
                ],
                "behavioral": [
                    "Tell me about a product you launched from concept to completion.",
                    "How do you handle conflicting stakeholder requirements?",
                    "Describe a time when you had to make a tough product decision.",
                    "How do you gather and incorporate user feedback?",
                    "Tell me about a product that failed and what you learned.",
                    "How do you work with cross-functional teams?",
                    "Describe your approach to market research.",
                    "How do you handle competing priorities?",
                    "Tell me about a time you influenced without authority.",
                    "How do you define and track product metrics?"
                ],
                "problem_solving": [
                    "How would you improve user engagement for a mobile app?",
                    "Design a product to solve remote team collaboration challenges.",
                    "How would you enter a new market with an existing product?",
                    "Design a monetization strategy for a freemium product.",
                    "How would you reduce user churn for a SaaS product?",
                    "Design a product for the elderly population.",
                    "How would you improve the onboarding experience?",
                    "Design a system for managing customer feedback.",
                    "How would you prioritize features for a MVP?",
                    "Design a product to address climate change challenges."
                ]
            }
        }
    
    def generate_interview_questions(self, job_role: str, num_questions: int = 10) -> List[str]:
        """Generate interview questions for a specific job role using Gemini AI."""
        # Normalize job role
        job_role_normalized = job_role.lower().replace(" ", "_").replace("-", "_")
        
        # Map common variations to our predefined roles
        role_mapping = {
            "software_engineer": ["software_engineer", "software_developer", "developer", "engineer", "sde"],
            "data_scientist": ["data_scientist", "data_analyst", "ml_engineer", "machine_learning"],
            "product_manager": ["product_manager", "pm", "product_owner", "product"]
        }
        
        # Find matching role
        matched_role = "software_engineer"  # Default
        for key, variations in role_mapping.items():
            if any(var in job_role_normalized for var in variations):
                matched_role = key
                break
        
        # Try to use Gemini for dynamic question generation
        try:
            prompt = f"""
You are an expert interviewer for {job_role} positions. Generate {num_questions} diverse and challenging interview questions.

Please include a mix of:
- Technical questions
- Behavioral questions  
- Problem-solving questions
- Scenario-based questions

Make the questions specific to the {job_role} role and current industry standards.

Return the response as a JSON array of strings, where each string is a complete interview question.
"""
            
            response_schema = {
                "questions": ["array of strings"]
            }
            
            result = generate_structured_response(prompt, response_schema)
            
            if result and "questions" in result:
                questions = result["questions"]
                if isinstance(questions, list) and len(questions) >= num_questions:
                    return questions[:num_questions]
        
        except Exception as e:
            self.logger.error(f"Error generating questions with Gemini: {str(e)}")
        
        # Fallback to predefined questions
        questions = []
        role_questions = self.interview_questions.get(matched_role, self.interview_questions["software_engineer"])
        
        # Collect all available questions
        all_questions = []
        all_questions.extend(role_questions.get("technical", []))
        all_questions.extend(role_questions.get("behavioral", []))
        all_questions.extend(role_questions.get("problem_solving", []))
        
        # If we don't have enough questions, repeat some
        if len(all_questions) < num_questions:
            # Duplicate questions if needed
            while len(all_questions) < num_questions:
                all_questions.extend(role_questions.get("technical", [])[:3])
                all_questions.extend(role_questions.get("behavioral", [])[:3])
                all_questions.extend(role_questions.get("problem_solving", [])[:3])
        
        # Shuffle and select
        import random
        random.shuffle(all_questions)
        
        return all_questions[:num_questions]
    
    def analyze_answer(self, question: str, answer: str, job_role: str = "software_engineer") -> Dict[str, Any]:
        """Analyze an interview answer and provide feedback using Gemini AI."""
        
        # Define the expected response structure
        response_schema = {
            "clarity": {
                "score": "integer (0-100)",
                "assessment": "string",
                "suggestions": ["array of strings"]
            },
            "confidence": {
                "score": "integer (0-100)",
                "assessment": "string", 
                "suggestions": ["array of strings"]
            },
            "accuracy": {
                "score": "integer (0-100)",
                "assessment": "string",
                "suggestions": ["array of strings"]
            },
            "overall": {
                "score": "integer (0-100)",
                "assessment": "string",
                "improvement_tips": ["array of strings"]
            }
        }
        
        # Create comprehensive prompt for Gemini
        prompt = f"""
You are an expert interviewer evaluating a candidate's response for a {job_role} position.

Question: {question}

Candidate's Answer: {answer}

Please provide detailed feedback on the following aspects:

1. CLARITY: How clear and well-structured is the answer? (0-100 score)
2. CONFIDENCE: How confident and articulate is the candidate? (0-100 score)
3. ACCURACY: How technically accurate and relevant is the answer? (0-100 score)

For each aspect, provide:
- A score from 0-100
- An assessment (excellent/good/needs improvement)
- Specific suggestions for improvement

Also provide an overall assessment and improvement tips.

Consider the context of a {job_role} role and current industry standards.
"""
        
        try:
            # Get structured response from Gemini
            feedback = generate_structured_response(prompt, response_schema)
            
            if not feedback:
                # Fallback to basic analysis if Gemini fails
                return self._fallback_analysis(question, answer)
            
            # Validate and clean the response
            clarity_score = max(0, min(100, int(feedback.get("clarity", {}).get("score", 70))))
            confidence_score = max(0, min(100, int(feedback.get("confidence", {}).get("score", 70))))
            accuracy_score = max(0, min(100, int(feedback.get("accuracy", {}).get("score", 70))))
            
            overall_score = (clarity_score + confidence_score + accuracy_score) // 3
            
            return {
                "clarity": {
                    "score": clarity_score,
                    "assessment": feedback.get("clarity", {}).get("assessment", "Good"),
                    "suggestions": feedback.get("clarity", {}).get("suggestions", [])
                },
                "confidence": {
                    "score": confidence_score,
                    "assessment": feedback.get("confidence", {}).get("assessment", "Good"),
                    "suggestions": feedback.get("confidence", {}).get("suggestions", [])
                },
                "accuracy": {
                    "score": accuracy_score,
                    "assessment": feedback.get("accuracy", {}).get("assessment", "Good"),
                    "suggestions": feedback.get("accuracy", {}).get("suggestions", [])
                },
                "overall": {
                    "score": overall_score,
                    "assessment": feedback.get("overall", {}).get("assessment", "Good performance"),
                    "improvement_tips": feedback.get("overall", {}).get("improvement_tips", [])
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing answer with Gemini: {str(e)}")
            return self._fallback_analysis(question, answer)
    
    def _fallback_analysis(self, question: str, answer: str) -> Dict[str, Any]:
        """Fallback analysis method when Gemini is not available."""
        # Basic analysis based on answer length and content
        answer_length = len(answer.split())
        
        # Simple scoring based on length
        if answer_length < 20:
            clarity_score = 40
            confidence_score = 30
            accuracy_score = 50
        elif answer_length < 50:
            clarity_score = 60
            confidence_score = 50
            accuracy_score = 60
        else:
            clarity_score = 75
            confidence_score = 70
            accuracy_score = 75
        
        overall_score = (clarity_score + confidence_score + accuracy_score) // 3
        
        return {
            "clarity": {
                "score": clarity_score,
                "assessment": "Good" if clarity_score >= 70 else "Needs improvement",
                "suggestions": ["Provide more structured answers", "Use clear examples"]
            },
            "confidence": {
                "score": confidence_score,
                "assessment": "Good" if confidence_score >= 70 else "Needs improvement",
                "suggestions": ["Speak more confidently", "Practice your responses"]
            },
            "accuracy": {
                "score": accuracy_score,
                "assessment": "Good" if accuracy_score >= 70 else "Needs improvement",
                "suggestions": ["Review technical concepts", "Provide more specific details"]
            },
            "overall": {
                "score": overall_score,
                "assessment": "Good performance" if overall_score >= 70 else "Room for improvement",
                "improvement_tips": [
                    "Practice more mock interviews",
                    "Study the fundamentals",
                    "Work on communication skills"
                ]
            }
        }
    
    def _get_overall_assessment(self, score: float) -> str:
        """Get overall assessment based on score."""
        if score >= 90:
            return "Excellent performance! You demonstrated strong knowledge and communication skills."
        elif score >= 75:
            return "Good performance! You showed solid understanding with room for minor improvements."
        elif score >= 60:
            return "Fair performance. You have a basic understanding but need to work on several areas."
        else:
            return "Needs improvement. Focus on strengthening your fundamentals and practice more."
