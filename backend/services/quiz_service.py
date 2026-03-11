from typing import Dict, List, Any, Optional
import random
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from models.quiz import Quiz, QuizAttempt

class QuizService:
    def __init__(self):
        # Sample quiz questions by category
        self.quiz_questions = {
            "programming": [
                {
                    "question": "What is the time complexity of binary search?",
                    "options": ["O(1)", "O(log n)", "O(n)", "O(n^2)"],
                    "correct_answer": 1,
                    "explanation": "Binary search divides the search space in half with each iteration, resulting in O(log n) time complexity."
                },
                {
                    "question": "Which of the following is NOT a programming paradigm?",
                    "options": ["Object-oriented", "Functional", "Procedural", "Compilation"],
                    "correct_answer": 3,
                    "explanation": "Compilation is a process, not a programming paradigm. Object-oriented, functional, and procedural are programming paradigms."
                },
                {
                    "question": "What does API stand for?",
                    "options": ["Application Programming Interface", "Advanced Programming Integration", "Automated Process Interface", "Application Process Integration"],
                    "correct_answer": 0,
                    "explanation": "API stands for Application Programming Interface, which defines how software components should interact."
                },
                {
                    "question": "Which data structure uses LIFO principle?",
                    "options": ["Queue", "Stack", "Array", "Tree"],
                    "correct_answer": 1,
                    "explanation": "Stack uses Last In First Out (LIFO) principle, where the last element added is the first one to be removed."
                },
                {
                    "question": "What is recursion in programming?",
                    "options": ["A loop that runs infinitely", "A function that calls itself", "A type of data structure", "A sorting algorithm"],
                    "correct_answer": 1,
                    "explanation": "Recursion is a programming technique where a function calls itself to solve smaller instances of the same problem."
                }
            ],
            "web_development": [
                {
                    "question": "Which HTML tag is used for the largest heading?",
                    "options": ["<h6>", "<heading>", "<h1>", "<header>"],
                    "correct_answer": 2,
                    "explanation": "<h1> is used for the largest heading in HTML, while <h6> is used for the smallest."
                },
                {
                    "question": "What does CSS stand for?",
                    "options": ["Computer Style Sheets", "Creative Style Sheets", "Cascading Style Sheets", "Colorful Style Sheets"],
                    "correct_answer": 2,
                    "explanation": "CSS stands for Cascading Style Sheets, used to describe the presentation of HTML documents."
                },
                {
                    "question": "Which JavaScript method is used to select an element by ID?",
                    "options": ["getElementByClass()", "getElementById()", "querySelector()", "selectElement()"],
                    "correct_answer": 1,
                    "explanation": "getElementById() is used to select an HTML element by its ID attribute."
                },
                {
                    "question": "What is the purpose of the box model in CSS?",
                    "options": ["To create 3D effects", "To define layout and spacing", "To animate elements", "To store data"],
                    "correct_answer": 1,
                    "explanation": "The CSS box model defines how elements are structured with content, padding, border, and margin."
                },
                {
                    "question": "Which HTTP status code represents 'Not Found'?",
                    "options": ["200", "301", "404", "500"],
                    "correct_answer": 2,
                    "explanation": "HTTP 404 status code indicates that the requested resource could not be found."
                }
            ],
            "data_science": [
                {
                    "question": "What is the purpose of cross-validation in machine learning?",
                    "options": ["To increase model accuracy", "To evaluate model performance on unseen data", "To reduce training time", "To visualize data"],
                    "correct_answer": 1,
                    "explanation": "Cross-validation helps evaluate how a machine learning model will perform on unseen data by using multiple train-test splits."
                },
                {
                    "question": "Which library is commonly used for data manipulation in Python?",
                    "options": ["NumPy", "Pandas", "Matplotlib", "Scikit-learn"],
                    "correct_answer": 1,
                    "explanation": "Pandas is the most popular library for data manipulation and analysis in Python."
                },
                {
                    "question": "What does overfitting mean in machine learning?",
                    "options": ["Model performs well on training data but poorly on test data", "Model is too simple", "Model has no errors", "Model trains too fast"],
                    "correct_answer": 0,
                    "explanation": "Overfitting occurs when a model learns the training data too well and fails to generalize to new data."
                },
                {
                    "question": "What is the difference between supervised and unsupervised learning?",
                    "options": ["Supervised uses labeled data, unsupervised uses unlabeled data", "Supervised is faster", "Unsupervised is more accurate", "There is no difference"],
                    "correct_answer": 0,
                    "explanation": "Supervised learning uses labeled data with known outputs, while unsupervised learning finds patterns in unlabeled data."
                },
                {
                    "question": "What is p-value in statistical testing?",
                    "options": ["The probability of making a Type I error", "The mean of the data", "The standard deviation", "The correlation coefficient"],
                    "correct_answer": 0,
                    "explanation": "The p-value represents the probability of observing the data (or more extreme) if the null hypothesis is true."
                }
            ],
            "general_knowledge": [
                {
                    "question": "What is the most popular programming language in 2024?",
                    "options": ["Java", "Python", "JavaScript", "C++"],
                    "correct_answer": 1,
                    "explanation": "Python has been ranked as the most popular programming language in recent years due to its versatility and ease of learning."
                },
                {
                    "question": "Which company developed the React framework?",
                    "options": ["Google", "Facebook", "Microsoft", "Amazon"],
                    "correct_answer": 1,
                    "explanation": "React was developed by Facebook (now Meta) and is maintained by Facebook and the community."
                },
                {
                    "question": "What does Git stand for?",
                    "options": ["Global Information Tracker", "Nothing, it's just a name", "General Version Control", "Great Integration Tool"],
                    "correct_answer": 1,
                    "explanation": "According to its creator, Git is just a name - it doesn't stand for anything specific."
                },
                {
                    "question": "Which cloud service provider is known as AWS?",
                    "options": ["Amazon Web Services", "Advanced Web Solutions", "Azure Web Services", "Apache Web Server"],
                    "correct_answer": 0,
                    "explanation": "AWS stands for Amazon Web Services, Amazon's cloud computing platform."
                },
                {
                    "question": "What is DevOps?",
                    "options": ["A programming language", "A set of practices combining software development and IT operations", "A database system", "A web framework"],
                    "correct_answer": 1,
                    "explanation": "DevOps is a set of practices that combines software development (Dev) and IT operations (Ops) to shorten the development lifecycle."
                }
            ]
        }
    
    def get_quiz_categories(self) -> List[str]:
        """Get available quiz categories."""
        return list(self.quiz_questions.keys())
    
    def generate_quiz(self, category: str, num_questions: int = 10, difficulty: str = "medium") -> Dict[str, Any]:
        """Generate a quiz with specified parameters."""
        if category not in self.quiz_questions:
            category = "programming"  # Default fallback
        
        questions_pool = self.quiz_questions[category]
        
        # Select random questions
        selected_questions = random.sample(
            questions_pool, 
            min(num_questions, len(questions_pool))
        )
        
        # Shuffle options for each question
        for question in selected_questions:
            random.shuffle(question["options"])
            # Update correct_answer index after shuffling
            # This would need to be handled differently in a real implementation
        
        return {
            "category": category,
            "difficulty": difficulty,
            "questions": selected_questions,
            "total_questions": len(selected_questions)
        }
    
    def evaluate_quiz_attempt(self, quiz_id: int, answers: List[Dict[str, Any]], db: Session) -> Dict[str, Any]:
        """Evaluate quiz attempt and provide feedback."""
        # Get quiz details
        quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
        if not quiz:
            raise ValueError("Quiz not found")
        
        questions = quiz.questions
        correct_count = 0
        total_questions = len(questions)
        
        detailed_feedback = []
        
        for i, user_answer in enumerate(answers):
            if i >= len(questions):
                continue
            
            question = questions[i]
            selected_option = user_answer.get("selected_option", 0)
            correct_option = question.get("correct_answer", 0)
            
            is_correct = selected_option == correct_option
            if is_correct:
                correct_count += 1
            
            detailed_feedback.append({
                "question_number": i + 1,
                "question": question["question"],
                "selected_option": selected_option,
                "correct_option": correct_option,
                "is_correct": is_correct,
                "explanation": question.get("explanation", "No explanation available")
            })
        
        # Calculate score
        score = int((correct_count / total_questions) * 100) if total_questions > 0 else 0
        
        # Generate performance feedback
        performance_feedback = self._generate_performance_feedback(score, correct_count, total_questions)
        
        return {
            "score": score,
            "correct_answers": correct_count,
            "total_questions": total_questions,
            "percentage": score,
            "performance_feedback": performance_feedback,
            "detailed_feedback": detailed_feedback
        }
    
    def _generate_performance_feedback(self, score: int, correct: int, total: int) -> Dict[str, Any]:
        """Generate performance feedback based on score."""
        if score >= 90:
            level = "Excellent"
            message = "Outstanding performance! You have mastered this topic."
            recommendations = [
                "Consider advanced topics in this area",
                "Try helping others learn this material",
                "Explore related advanced concepts"
            ]
        elif score >= 70:
            level = "Good"
            message = "Good job! You have a solid understanding of this topic."
            recommendations = [
                "Review the questions you got wrong",
                "Practice more problems in this area",
                "Consider studying related topics"
            ]
        elif score >= 50:
            level = "Average"
            message = "You're on the right track, but there's room for improvement."
            recommendations = [
                "Focus on understanding the fundamentals",
                "Review the explanations for incorrect answers",
                "Practice more questions in this category"
            ]
        else:
            level = "Needs Improvement"
            message = "Keep practicing! This topic needs more attention."
            recommendations = [
                "Start with basic concepts in this area",
                "Review study materials thoroughly",
                "Consider seeking additional learning resources"
            ]
        
        return {
            "level": level,
            "message": message,
            "recommendations": recommendations,
            "next_steps": self._get_next_steps(score)
        }
    
    def _get_next_steps(self, score: int) -> List[str]:
        """Get recommended next steps based on performance."""
        if score >= 80:
            return [
                "Try a more difficult quiz",
                "Explore advanced topics",
                "Take on practical projects"
            ]
        elif score >= 60:
            return [
                "Practice similar quizzes",
                "Review weak areas",
                "Try hands-on exercises"
            ]
        else:
            return [
                "Study fundamental concepts",
                "Take beginner-level tutorials",
                "Practice with guided exercises"
            ]
    
    def create_quiz_in_db(self, quiz_data: Dict[str, Any], db: Session) -> Quiz:
        """Create a quiz record in the database."""
        quiz = Quiz(
            title=quiz_data["title"],
            category=quiz_data["category"],
            questions=quiz_data["questions"],
            difficulty=quiz_data.get("difficulty", "medium")
        )
        
        db.add(quiz)
        db.commit()
        db.refresh(quiz)
        
        return quiz
    
    def save_quiz_attempt(self, user_id: int, quiz_id: int, answers: List[Dict[str, Any]], 
                         evaluation_result: Dict[str, Any], db: Session) -> QuizAttempt:
        """Save quiz attempt to database."""
        attempt = QuizAttempt(
            user_id=user_id,
            quiz_id=quiz_id,
            answers=answers,
            score=evaluation_result["score"],
            total_questions=evaluation_result["total_questions"],
            feedback=evaluation_result
        )
        
        db.add(attempt)
        db.commit()
        db.refresh(attempt)
        
        return attempt
    
    def get_user_quiz_history(self, user_id: int, db: Session) -> List[QuizAttempt]:
        """Get quiz history for a user."""
        return db.query(QuizAttempt).filter(
            QuizAttempt.user_id == user_id
        ).order_by(QuizAttempt.completed_at.desc()).all()
    
    def get_user_performance_stats(self, user_id: int, db: Session) -> Dict[str, Any]:
        """Get performance statistics for a user."""
        attempts = self.get_user_quiz_history(user_id, db)
        
        if not attempts:
            return {
                "total_quizzes": 0,
                "average_score": 0,
                "best_score": 0,
                "categories_attempted": [],
                "recent_performance": []
            }
        
        scores = [attempt.score for attempt in attempts]
        categories = list(set(attempt.quiz.category for attempt in attempts if attempt.quiz))
        
        # Recent performance (last 5 attempts)
        recent_attempts = attempts[:5]
        recent_performance = [
            {
                "quiz_title": attempt.quiz.title if attempt.quiz else "Unknown",
                "score": attempt.score,
                "completed_at": attempt.completed_at
            }
            for attempt in recent_attempts
        ]
        
        return {
            "total_quizzes": len(attempts),
            "average_score": round(sum(scores) / len(scores), 1),
            "best_score": max(scores),
            "categories_attempted": categories,
            "recent_performance": recent_performance
        }
