from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database import SessionLocal, settings
from models.user import User
from models.resume import Resume
from models.interview import Interview
from models.quiz import QuizAttempt
from models.progress import Progress

class ProgressService:
    def __init__(self):
        pass
    
    def track_resume_score(self, user_id: int, resume_score: int, db: Session) -> Progress:
        """Track resume score improvement."""
        progress = Progress(
            user_id=user_id,
            metric_type="resume_score",
            metric_value=resume_score,
            metric_data={"score_type": "resume_analysis"}
        )
        
        db.add(progress)
        db.commit()
        db.refresh(progress)
        
        return progress
    
    def track_quiz_score(self, user_id: int, quiz_score: int, db: Session, quiz_category: str = None) -> Progress:
        """Track quiz performance."""
        metric_data = {"score_type": "quiz_performance"}
        if quiz_category:
            metric_data["category"] = quiz_category
        
        progress = Progress(
            user_id=user_id,
            metric_type="quiz_score",
            metric_value=quiz_score,
            metric_data=metric_data
        )
        
        db.add(progress)
        db.commit()
        db.refresh(progress)
        
        return progress
    
    def track_interview_score(self, user_id: int, interview_score: int, db: Session, job_role: str = None) -> Progress:
        """Track interview practice performance."""
        metric_data = {"score_type": "interview_performance"}
        if job_role:
            metric_data["job_role"] = job_role
        
        progress = Progress(
            user_id=user_id,
            metric_type="interview_score",
            metric_value=interview_score,
            metric_data=metric_data
        )
        
        db.add(progress)
        db.commit()
        db.refresh(progress)
        
        return progress
    
    def get_user_progress_summary(self, user_id: int, db: Session) -> Dict[str, Any]:
        """Get comprehensive progress summary for a user."""
        # Get all progress records
        progress_records = db.query(Progress).filter(
            Progress.user_id == user_id
        ).order_by(Progress.created_at.desc()).all()
        
        if not progress_records:
            return {
                "total_activities": 0,
                "average_scores": {},
                "improvement_trends": {},
                "achievements": [],
                "recommendations": []
            }
        
        # Group by metric type
        resume_scores = [p.metric_value for p in progress_records if p.metric_type == "resume_score"]
        quiz_scores = [p.metric_value for p in progress_records if p.metric_type == "quiz_score"]
        interview_scores = [p.metric_value for p in progress_records if p.metric_type == "interview_score"]
        
        # Calculate averages
        average_scores = {}
        if resume_scores:
            average_scores["resume"] = round(sum(resume_scores) / len(resume_scores), 1)
        if quiz_scores:
            average_scores["quiz"] = round(sum(quiz_scores) / len(quiz_scores), 1)
        if interview_scores:
            average_scores["interview"] = round(sum(interview_scores) / len(interview_scores), 1)
        
        # Calculate improvement trends
        improvement_trends = self._calculate_improvement_trends(progress_records)
        
        # Get achievements
        achievements = self._get_achievements(user_id, db)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(average_scores, improvement_trends)
        
        return {
            "total_activities": len(progress_records),
            "average_scores": average_scores,
            "improvement_trends": improvement_trends,
            "achievements": achievements,
            "recommendations": recommendations,
            "latest_activity": progress_records[0].created_at if progress_records else None
        }
    
    def _calculate_improvement_trends(self, progress_records: List[Progress]) -> Dict[str, Any]:
        """Calculate improvement trends for different metrics."""
        trends = {}
        
        # Group by metric type and sort by date
        by_type = {}
        for record in progress_records:
            if record.metric_type not in by_type:
                by_type[record.metric_type] = []
            by_type[record.metric_type].append(record)
        
        for metric_type, records in by_type.items():
            records.sort(key=lambda x: x.created_at)
            
            if len(records) < 2:
                trends[metric_type] = {
                    "trend": "insufficient_data",
                    "improvement": 0,
                    "recent_average": records[0].metric_value if records else 0
                }
                continue
            
            # Calculate trend
            recent_scores = [r.metric_value for r in records[-3:]]  # Last 3 records
            earlier_scores = [r.metric_value for r in records[:-3]]  # Earlier records
            
            recent_avg = sum(recent_scores) / len(recent_scores)
            earlier_avg = sum(earlier_scores) / len(earlier_scores) if earlier_scores else recent_avg
            
            improvement = recent_avg - earlier_avg
            trend = "improving" if improvement > 5 else "declining" if improvement < -5 else "stable"
            
            trends[metric_type] = {
                "trend": trend,
                "improvement": round(improvement, 1),
                "recent_average": round(recent_avg, 1),
                "earlier_average": round(earlier_avg, 1),
                "data_points": len(records)
            }
        
        return trends
    
    def _get_achievements(self, user_id: int, db: Session) -> List[Dict[str, Any]]:
        """Get user achievements based on their progress."""
        achievements = []
        
        # Get counts of different activities
        resume_count = db.query(Resume).filter(Resume.user_id == user_id).count()
        interview_count = db.query(Interview).filter(Interview.user_id == user_id).count()
        quiz_attempt_count = db.query(QuizAttempt).filter(QuizAttempt.user_id == user_id).count()
        
        # Resume achievements
        if resume_count >= 1:
            achievements.append({
                "type": "resume",
                "title": "Resume Analyzer",
                "description": "Analyzed your first resume",
                "earned_at": datetime.utcnow()
            })
        
        if resume_count >= 3:
            achievements.append({
                "type": "resume",
                "title": "Resume Expert",
                "description": "Analyzed 3 or more resumes",
                "earned_at": datetime.utcnow()
            })
        
        # Interview achievements
        if interview_count >= 1:
            achievements.append({
                "type": "interview",
                "title": "Interview Beginner",
                "description": "Completed your first mock interview",
                "earned_at": datetime.utcnow()
            })
        
        if interview_count >= 5:
            achievements.append({
                "type": "interview",
                "title": "Interview Pro",
                "description": "Completed 5 or more mock interviews",
                "earned_at": datetime.utcnow()
            })
        
        # Quiz achievements
        if quiz_attempt_count >= 1:
            achievements.append({
                "type": "quiz",
                "title": "Quiz Taker",
                "description": "Completed your first quiz",
                "earned_at": datetime.utcnow()
            })
        
        if quiz_attempt_count >= 10:
            achievements.append({
                "type": "quiz",
                "title": "Quiz Master",
                "description": "Completed 10 or more quizzes",
                "earned_at": datetime.utcnow()
            })
        
        # High score achievements
        high_quiz_scores = db.query(QuizAttempt).filter(
            QuizAttempt.user_id == user_id,
            QuizAttempt.score >= 80
        ).count()
        
        if high_quiz_scores >= 3:
            achievements.append({
                "type": "performance",
                "title": "High Performer",
                "description": "Scored 80% or higher in 3 quizzes",
                "earned_at": datetime.utcnow()
            })
        
        return achievements
    
    def _generate_recommendations(self, average_scores: Dict[str, float], 
                                improvement_trends: Dict[str, Any]) -> List[str]:
        """Generate personalized recommendations based on progress."""
        recommendations = []
        
        # Resume recommendations
        resume_avg = average_scores.get("resume", 0)
        if resume_avg < 60:
            recommendations.append("Your resume scores are below average. Consider improving your resume structure and adding more specific achievements.")
        elif resume_avg >= 80:
            recommendations.append("Great resume! Consider updating it regularly with new skills and experiences.")
        
        # Quiz recommendations
        quiz_avg = average_scores.get("quiz", 0)
        if quiz_avg < 70:
            recommendations.append("Focus on studying the fundamentals. Practice more quizzes to improve your knowledge.")
        elif quiz_avg >= 85:
            recommendations.append("Excellent quiz performance! Try more advanced topics or help others learn.")
        
        # Interview recommendations
        interview_avg = average_scores.get("interview", 0)
        if interview_avg < 65:
            recommendations.append("Practice more mock interviews to improve your communication and technical skills.")
        elif interview_avg >= 80:
            recommendations.append("Strong interview skills! You're ready for real interviews.")
        
        # Trend-based recommendations
        for metric_type, trend_data in improvement_trends.items():
            if trend_data["trend"] == "declining":
                if metric_type == "quiz_score":
                    recommendations.append("Your quiz scores have been declining. Review recent topics and practice more.")
                elif metric_type == "interview_score":
                    recommendations.append("Interview performance needs attention. Practice with different question types.")
                elif metric_type == "resume_score":
                    recommendations.append("Resume quality has decreased. Consider updating with recent achievements.")
        
        # General recommendations
        if not recommendations:
            recommendations.append("Keep up the great work! Continue practicing and learning new skills.")
        
        return recommendations[:5]  # Return top 5 recommendations
    
    def get_detailed_progress(self, user_id: int, metric_type: Optional[str] = None, 
                            days_back: Optional[int] = 30, db: Session = None) -> Dict[str, Any]:
        """Get detailed progress for specific metrics."""
        if not db:
            raise ValueError("Database session is required")
        
        # Calculate date filter
        start_date = datetime.utcnow() - timedelta(days=days_back)
        
        # Build query
        query = db.query(Progress).filter(
            Progress.user_id == user_id,
            Progress.created_at >= start_date
        )
        
        if metric_type:
            query = query.filter(Progress.metric_type == metric_type)
        
        progress_records = query.order_by(Progress.created_at.asc()).all()
        
        if not progress_records:
            return {
                "metric_type": metric_type or "all",
                "period_days": days_back,
                "data_points": 0,
                "timeline": [],
                "statistics": {}
            }
        
        # Build timeline data
        timeline = []
        for record in progress_records:
            timeline.append({
                "date": record.created_at.strftime("%Y-%m-%d"),
                "metric_type": record.metric_type,
                "value": record.metric_value,
                "metric_data": record.metric_data
            })
        
        # Calculate statistics
        values = [r.metric_value for r in progress_records]
        statistics = {
            "average": round(sum(values) / len(values), 1),
            "min": min(values),
            "max": max(values),
            "latest": values[-1] if values else 0,
            "improvement": round(values[-1] - values[0], 1) if len(values) > 1 else 0
        }
        
        return {
            "metric_type": metric_type or "all",
            "period_days": days_back,
            "data_points": len(progress_records),
            "timeline": timeline,
            "statistics": statistics
        }
    
    def get_leaderboard(self, metric_type: str, limit: int = 10, db: Session = None) -> List[Dict[str, Any]]:
        """Get leaderboard for a specific metric."""
        if not db:
            raise ValueError("Database session is required")
        
        # Get latest scores for each user
        latest_scores = db.query(
            Progress.user_id,
            Progress.metric_type,
            func.max(Progress.created_at).label('latest_date'),
            func.max(Progress.metric_value).label('latest_score')
        ).filter(
            Progress.metric_type == metric_type
        ).group_by(
            Progress.user_id, Progress.metric_type
        ).subquery()
        
        # Join with users to get usernames
        leaderboard_data = db.query(
            User.username,
            User.full_name,
            latest_scores.c.latest_score
        ).join(
            latest_scores, User.id == latest_scores.c.user_id
        ).order_by(
            latest_scores.c.latest_score.desc()
        ).limit(limit).all()
        
        leaderboard = []
        for i, (username, full_name, score) in enumerate(leaderboard_data, 1):
            leaderboard.append({
                "rank": i,
                "username": username,
                "full_name": full_name,
                "score": score,
                "metric_type": metric_type
            })
        
        return leaderboard
