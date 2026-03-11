# 🚀 VidyaMitra - येथून सुरुवात करा (START HERE)

## 📋 तुम्हाला काय करायचे आहे? (What do you want to do?)

### 1️⃣ पहिल्यांदा Setup करायचे आहे? (First Time Setup)
👉 **`QUICK_START_MR.md`** पहा

### 2️⃣ Application चालवायचे आहे? (Run Application)
👉 **`start-all.bat`** run करा

### 3️⃣ समस्या आहे? (Having Problems)
👉 **`TROUBLESHOOTING_MR.md`** पहा

### 4️⃣ Detailed Documentation हवे आहे? (Need Documentation)
👉 **`README_MR.md`** पहा

---

## ⚡ द्रुत सुरुवात (Quick Start)

### पहिल्यांदा (First Time):

```bash
# 1. Backend setup
cd backend
copy .env.example .env
# Edit .env file and add your API keys
pip install -r requirements.txt

# 2. Frontend setup
cd ..
npm install

# 3. Start everything
start-all.bat
```

### पुन्हा चालवायचे (Run Again):

```bash
start-all.bat
```

---

## 🎯 Application URLs

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:8080 | Main application |
| Backend API | http://localhost:8000 | API server |
| API Docs | http://localhost:8000/docs | Interactive API documentation |
| Health Check | http://localhost:8000/health | Server status |

---

## 📚 Documentation Files

| File | Purpose | Language |
|------|---------|----------|
| `START_HERE.md` | हा file - येथून सुरुवात करा | Marathi |
| `QUICK_START_MR.md` | 5 मिनिटांत सुरुवात | Marathi |
| `README_MR.md` | संपूर्ण documentation | Marathi |
| `TROUBLESHOOTING_MR.md` | समस्या निवारण | Marathi |
| `SETUP_GUIDE.md` | Detailed setup guide | English |
| `CONNECTION_FIX_SUMMARY.md` | Technical details | English |

---

## 🛠️ Startup Scripts

| Script | Purpose |
|--------|---------|
| `start-all.bat` | दोन्ही servers start करा |
| `start-backend.bat` | फक्त backend start करा |
| `start-frontend.bat` | फक्त frontend start करा |
| `test-connection.bat` | Connection test करा |

---

## ✅ Pre-requisites

### Software Required:
- ✅ Python 3.9+ installed
- ✅ Node.js 16+ installed
- ✅ pip (Python package manager)
- ✅ npm (Node package manager)

### Check Installation:
```bash
python --version
node --version
npm --version
pip --version
```

---

## 🎬 Step-by-Step Visual Guide

```
┌─────────────────────────────────────────────────────────────┐
│  STEP 1: Backend Setup                                      │
│  ────────────────────────────────────────────────────────   │
│                                                              │
│  cd backend                                                  │
│  copy .env.example .env                                      │
│  pip install -r requirements.txt                             │
│  python main.py                                              │
│                                                              │
│  ✅ Backend running on http://localhost:8000                │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  STEP 2: Frontend Setup (New Terminal)                      │
│  ────────────────────────────────────────────────────────   │
│                                                              │
│  npm install                                                 │
│  npm run dev                                                 │
│                                                              │
│  ✅ Frontend running on http://localhost:8080               │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  STEP 3: Open Browser                                        │
│  ────────────────────────────────────────────────────────   │
│                                                              │
│  http://localhost:8080                                       │
│                                                              │
│  ✅ Application is ready!                                    │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔍 Verification

### Backend Check:
```bash
curl http://localhost:8000/health
```

Expected:
```json
{
  "status": "healthy",
  "service": "VidyaMitra API",
  "version": "1.0.0",
  "database": "connected"
}
```

### Frontend Check:
1. Open http://localhost:8080
2. Press F12 (DevTools)
3. Check Console tab
4. Look for "Connection Test Summary"
5. All checks should be ✅

---

## 🎯 Features to Test

1. **Authentication**
   - Signup with new account
   - Login with credentials
   - Access dashboard

2. **Resume Analysis**
   - Upload PDF/DOCX resume
   - View AI analysis
   - Check skill extraction

3. **Mock Interview**
   - Start interview session
   - Answer questions
   - Get feedback

4. **Skill Quiz**
   - Generate quiz
   - Solve questions
   - View results

5. **Progress Tracking**
   - View dashboard stats
   - Check progress page
   - Monitor achievements

---

## 🆘 Need Help?

### Quick Fixes:

**Backend not starting?**
```bash
cd backend
pip install -r requirements.txt
python main.py
```

**Frontend not starting?**
```bash
npm install
npm run dev
```

**Connection issues?**
```bash
test-connection.bat
```

**Database issues?**
```bash
cd backend
del vidyamitra.db
python main.py
```

### Detailed Help:
- समस्या निवारण: `TROUBLESHOOTING_MR.md`
- Setup मदत: `QUICK_START_MR.md`
- Full docs: `README_MR.md`

---

## 💡 Pro Tips

1. **दोन terminals वापरा:**
   - Terminal 1: Backend logs
   - Terminal 2: Frontend logs

2. **Browser DevTools वापरा:**
   - F12 press करा
   - Console: JavaScript errors
   - Network: API calls
   - Application: LocalStorage (token)

3. **API Docs वापरा:**
   - http://localhost:8000/docs
   - Interactive API testing
   - Request/Response examples

4. **Logs monitor करा:**
   - Backend: Terminal मध्ये
   - Frontend: Browser console मध्ये

---

## 🎉 Ready to Start!

### Option 1: Automatic (Recommended)
```bash
start-all.bat
```

### Option 2: Manual
**Terminal 1:**
```bash
cd backend
python main.py
```

**Terminal 2:**
```bash
npm run dev
```

### Then:
1. Open http://localhost:8080
2. Create account
3. Login
4. Explore features!

---

## 📞 Support

समस्या असल्यास:
1. Backend logs screenshot
2. Browser console errors screenshot
3. Network tab API calls screenshot
4. `TROUBLESHOOTING_MR.md` पहा

---

## 🌟 Project Structure

```
VidyaMitra/
│
├── 📁 backend/              # Backend (FastAPI + Python)
│   ├── main.py             # Entry point
│   ├── database.py         # Database config
│   ├── .env                # Environment variables
│   └── requirements.txt    # Dependencies
│
├── 📁 src/                  # Frontend (React + TypeScript)
│   ├── main.tsx            # Entry point
│   ├── services/           # API services
│   └── pages/              # Page components
│
├── 🚀 start-all.bat        # Start both servers
├── 📖 START_HERE.md        # हा file
├── 📖 QUICK_START_MR.md    # Quick start guide
├── 📖 README_MR.md         # Full documentation
└── 📖 TROUBLESHOOTING_MR.md # Troubleshooting
```

---

## ✨ Next Steps

1. ✅ Read `QUICK_START_MR.md`
2. ✅ Run `start-all.bat`
3. ✅ Open http://localhost:8080
4. ✅ Create account & login
5. ✅ Test all features
6. ✅ Start developing!

---

**Happy Coding! 🚀**

तुमच्या VidyaMitra journey साठी शुभेच्छा!
