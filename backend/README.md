# VidyaMitra Backend API

An AI-driven career assistant platform backend built with Python and FastAPI.

## Features

- **Authentication**: JWT-based user registration and login system
- **Resume Analysis**: Upload and analyze resumes with AI-powered insights using Google Gemini
- **Skill Gap Detection**: Compare skills with job market requirements
- **Career Roadmap Generation**: Personalized learning paths and recommendations
- **Mock Interviews**: AI-powered interview practice with feedback
- **Quiz System**: Interactive quizzes for skill assessment
- **Progress Tracking**: Comprehensive progress monitoring and analytics

## Tech Stack

- **Framework**: FastAPI
- **Database**: SQLite (development) / PostgreSQL (production)
- **Authentication**: JWT tokens with bcrypt password hashing
- **AI/ML**: Google Gemini API for AI-powered analysis
- **File Processing**: PyPDF2, python-docx for resume parsing
- **Documentation**: Auto-generated OpenAPI/Swagger docs

## Project Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── database.py             # Database configuration and connection
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── models/                # SQLAlchemy database models
│   ├── __init__.py
│   ├── user.py
│   ├── resume.py
│   ├── interview.py
│   ├── quiz.py
│   └── progress.py
├── schemas/               # Pydantic models for request/response
│   ├── __init__.py
│   ├── user.py
│   ├── resume.py
│   ├── interview.py
│   ├── quiz.py
│   └── progress.py
├── routers/               # API route handlers
│   ├── __init__.py
│   ├── auth_router.py
│   ├── resume_router.py
│   ├── interview_router.py
│   ├── quiz_router.py
│   ├── recommendation_router.py
│   └── progress_router.py
├── services/              # Business logic and utilities
│   ├── __init__.py
│   ├── auth.py
│   ├── resume_service.py
│   ├── quiz_service.py
│   └── progress_service.py
└── ai_agents/             # AI-powered analysis agents
    ├── __init__.py
    ├── resume_analyzer.py
    ├── skill_mapper.py
    ├── interview_agent.py
    └── recommendation_agent.py
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd VidyaMitra/backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Create uploads directory**
   ```bash
   mkdir -p uploads/resumes
   ```

## Running the Application

### Development Mode

```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Using Uvicorn Directly

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once the server is running, you can access:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI Schema**: `http://localhost:8000/openapi.json`

## API Endpoints

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user info

### Resume Management
- `POST /resume/upload` - Upload and analyze resume
- `GET /resume/` - Get user resumes
- `GET /resume/{id}` - Get specific resume
- `GET /resume/{id}/analysis` - Get resume analysis

### Mock Interviews
- `POST /interview/start` - Start mock interview
- `POST /interview/submit-answer` - Submit interview answer
- `GET /interview/{id}/status` - Get interview status
- `POST /interview/{id}/complete` - Complete interview

### Quiz System
- `GET /quiz/categories` - Get quiz categories
- `POST /quiz/generate` - Generate new quiz
- `POST /quiz/submit` - Submit quiz answers
- `GET /quiz/history` - Get quiz history

### Recommendations
- `POST /recommendations/skill-gap` - Analyze skill gaps
- `POST /recommendations/roadmap` - Generate career roadmap
- `GET /recommendations/market-trends` - Get market trends

### Progress Tracking
- `GET /progress/summary` - Get progress summary
- `GET /progress/detailed` - Get detailed progress
- `GET /progress/leaderboard` - Get leaderboard
- `GET /progress/achievements` - Get achievements

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Database connection string | `sqlite:///./vidyamitra.db` |
| `SECRET_KEY` | JWT secret key | (change in production) |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | `30` |
| `GEMINI_API_KEY` | Google Gemini API key | (required for AI features) |
| `DEBUG` | Debug mode | `True` |

## Getting Google Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated API key
5. Add it to your `.env` file:
   ```
   GEMINI_API_KEY=your-actual-api-key-here
   ```

## Database Setup

### SQLite (Development)
The application uses SQLite by default. The database file will be created automatically.

### PostgreSQL (Production)
1. Install PostgreSQL
2. Create database:
   ```sql
   CREATE DATABASE vidyamitra;
   ```
3. Update `.env` file:
   ```
   DATABASE_URL=postgresql://username:password@localhost/vidyamitra
   ```

## Testing

Run tests with:
```bash
pytest
```

## Deployment

### Using Docker
1. Build the image:
   ```bash
   docker build -t vidyamitra-backend .
   ```

2. Run the container:
   ```bash
   docker run -p 8000:8000 vidyamitra-backend
   ```

### Production Considerations
- Use PostgreSQL instead of SQLite
- Set strong `SECRET_KEY`
- Enable HTTPS
- Configure proper CORS origins
- Set up proper logging
- Use environment variables for sensitive data

## API Usage Examples

### Register a new user
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "testuser",
    "password": "securepassword",
    "full_name": "Test User"
  }'
```

### Login
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=securepassword"
```

### Upload resume
```bash
curl -X POST "http://localhost:8000/resume/upload" \
  -H "Authorization: Bearer <your-token>" \
  -F "file=@resume.pdf"
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions, please open an issue in the repository.
