# VidyaMitra - Frontend-Backend Connection Setup Guide

## समस्या (Problem)
Frontend आणि Backend properly connected नाहीत, त्यामुळे UI मध्ये static data दिसत आहे.

## समाधान (Solution)

### 1. Backend Setup

#### Step 1: Backend Dependencies Install करा
```bash
cd backend
pip install -r requirements.txt
```

#### Step 2: Environment Variables Setup करा
Backend folder मध्ये `.env` file तयार करा:

```bash
# backend/.env
DATABASE_URL=sqlite:///./vidyamitra.db
SECRET_KEY=your-super-secret-key-change-this-in-production
GEMINI_API_KEY=your-gemini-api-key-here
DEBUG=True
```

#### Step 3: Backend Server Start करा
```bash
cd backend
python main.py
```

किंवा

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend चालू झाल्यावर हे URLs काम करतील:
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

---

### 2. Frontend Setup

#### Step 1: Frontend Dependencies Install करा
```bash
npm install
```

#### Step 2: Frontend Server Start करा
```bash
npm run dev
```

Frontend चालू झाल्यावर: http://localhost:8080

---

### 3. Connection Verification

#### Backend Running आहे का check करा:
```bash
curl http://localhost:8000/health
```

Response असावा:
```json
{
  "status": "healthy",
  "service": "VidyaMitra API",
  "version": "1.0.0",
  "database": "connected"
}
```

---

### 4. Common Issues & Solutions

#### Issue 1: Backend चालू नाही
**Solution:**
- Check if port 8000 already in use आहे
- Backend folder मध्ये `.env` file आहे का check करा
- Dependencies properly install झाल्या का verify करा

#### Issue 2: CORS Error
**Solution:**
- Backend `main.py` मध्ये frontend URL (http://localhost:8080) CORS origins मध्ये आहे
- Already configured आहे, पण तरीही issue असेल तर backend restart करा

#### Issue 3: Database Connection Failed
**Solution:**
- `.env` file मध्ये `DATABASE_URL` properly set आहे का check करा
- SQLite साठी: `sqlite:///./vidyamitra.db`
- Database file create होण्यासाठी backend एकदा run करा

#### Issue 4: API Calls Failing
**Solution:**
- Browser console मध्ये errors check करा (F12)
- Network tab मध्ये API calls status check करा
- Backend logs मध्ये errors check करा

---

### 5. Testing the Connection

1. Backend start करा: `cd backend && python main.py`
2. Frontend start करा: `npm run dev`
3. Browser मध्ये http://localhost:8080 open करा
4. Login/Signup page वर जा
5. Account create करा किंवा login करा
6. Dashboard वर real data दिसायला हवा

---

### 6. Development Workflow

**दोन्ही servers एकाच वेळी चालवा:**

Terminal 1 (Backend):
```bash
cd backend
python main.py
```

Terminal 2 (Frontend):
```bash
npm run dev
```

---

## API Endpoints

### Authentication
- POST `/auth/register` - नवीन user registration
- POST `/auth/login` - User login
- GET `/auth/me` - Current user info

### Resume
- POST `/resume/upload` - Resume upload
- GET `/resume/` - User च्या सर्व resumes
- GET `/resume/{id}/analysis` - Resume analysis
- DELETE `/resume/{id}` - Resume delete

### Interview
- POST `/interview/start` - Mock interview start
- POST `/interview/{id}/answer` - Answer submit
- GET `/interview/{id}` - Interview details

### Quiz
- GET `/quiz/generate` - Quiz generate
- POST `/quiz/submit` - Quiz submit
- GET `/quiz/results/{id}` - Quiz results

### Progress
- GET `/progress/` - User progress
- GET `/progress/stats` - Progress statistics

### Recommendations
- GET `/recommendations/` - Career recommendations
- GET `/recommendations/roadmap` - Learning roadmap

---

## Next Steps

1. ✅ Backend server start करा
2. ✅ Frontend server start करा
3. ✅ Connection verify करा
4. ✅ Test basic features (login, signup)
5. ✅ Test resume upload
6. ✅ Test other features

---

## Support

Issues असतील तर:
1. Backend logs check करा
2. Browser console errors check करा
3. Network tab मध्ये API calls check करा
4. `/health` endpoint test करा
