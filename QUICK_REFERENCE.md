# VidyaMitra - द्रुत संदर्भ (Quick Reference)

## 🚀 एका नजरेत (At a Glance)

### सुरुवात करा (Start)
```bash
start-all.bat
```

### URLs
- Frontend: http://localhost:8080
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## 📋 Commands Cheat Sheet

### Backend Commands
```bash
# Start backend
cd backend
python main.py

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env

# Reset database
del vidyamitra.db
```

### Frontend Commands
```bash
# Start frontend
npm run dev

# Install dependencies
npm install

# Build for production
npm run build

# Run tests
npm run test
```

### Quick Commands
```bash
# Start both servers
start-all.bat

# Test connection
test-connection.bat

# Start backend only
start-backend.bat

# Start frontend only
start-frontend.bat
```

---

## 🔍 Debugging Quick Guide

### Backend Issues
```bash
# Check if running
curl http://localhost:8000/health

# View logs
# Check terminal where backend is running

# Restart
Ctrl + C
python main.py
```

### Frontend Issues
```bash
# Check browser console
F12 → Console tab

# Check API calls
F12 → Network tab

# Check token
F12 → Application → LocalStorage

# Restart
Ctrl + C
npm run dev
```

### Database Issues
```bash
cd backend
del vidyamitra.db
python main.py
```

---

## 📁 Important Files

### Configuration
| File | Purpose |
|------|---------|
| `backend/.env` | Environment variables |
| `vite.config.ts` | Frontend config + proxy |
| `backend/main.py` | Backend entry point |
| `package.json` | Frontend dependencies |

### Documentation
| File | Purpose |
|------|---------|
| `START_HERE.md` | Main starting point |
| `QUICK_START_MR.md` | 5-minute setup |
| `TROUBLESHOOTING_MR.md` | Problem solving |
| `README_MR.md` | Full documentation |

### Scripts
| File | Purpose |
|------|---------|
| `start-all.bat` | Start both servers |
| `start-backend.bat` | Start backend |
| `start-frontend.bat` | Start frontend |
| `test-connection.bat` | Test connection |

---

## 🎯 Common Tasks

### First Time Setup
```bash
# 1. Backend
cd backend
copy .env.example .env
# Edit .env file
pip install -r requirements.txt

# 2. Frontend
cd ..
npm install

# 3. Start
start-all.bat
```

### Daily Development
```bash
# Just run this
start-all.bat

# Or manually in 2 terminals
# Terminal 1: cd backend && python main.py
# Terminal 2: npm run dev
```

### Testing Features
1. Open http://localhost:8080
2. Create account (Signup)
3. Login
4. Test features:
   - Upload resume
   - Start interview
   - Take quiz
   - View progress

---

## 🔧 Environment Variables

### Required in `backend/.env`
```env
DATABASE_URL=sqlite:///./vidyamitra.db
SECRET_KEY=your-secret-key-min-32-chars
GEMINI_API_KEY=your-gemini-api-key
DEBUG=True
```

### Get Gemini API Key
1. Visit: https://makersuite.google.com/app/apikey
2. Login with Google
3. Create API Key
4. Copy to `.env` file

---

## 🐛 Quick Fixes

### "Module not found"
```bash
cd backend
pip install -r requirements.txt
```

### "Port already in use"
```bash
# Find process
netstat -ano | findstr :8000
# Kill process
taskkill /PID <pid> /F
```

### "CORS Error"
- Backend restart करा
- Frontend restart करा
- Browser cache clear करा

### "Database Error"
```bash
cd backend
del vidyamitra.db
python main.py
```

### "API calls failing"
1. Backend running आहे का check करा
2. Browser console errors पहा
3. Network tab मध्ये status codes पहा

---

## 📊 Status Codes

| Code | Meaning | Action |
|------|---------|--------|
| 200 | Success | ✅ All good |
| 401 | Unauthorized | Login again |
| 403 | Forbidden | Check permissions |
| 404 | Not found | Check URL |
| 500 | Server error | Check backend logs |

---

## 🎨 API Endpoints Quick Reference

### Authentication
```
POST /auth/register    - Signup
POST /auth/login       - Login
GET  /auth/me          - Current user
```

### Resume
```
POST   /resume/upload           - Upload resume
GET    /resume/                 - List resumes
GET    /resume/{id}/analysis    - Get analysis
DELETE /resume/{id}             - Delete resume
```

### Interview
```
POST /interview/start          - Start interview
POST /interview/{id}/answer    - Submit answer
GET  /interview/{id}           - Get interview
```

### Quiz
```
GET  /quiz/generate       - Generate quiz
POST /quiz/submit         - Submit answers
GET  /quiz/results/{id}   - Get results
```

### Progress
```
GET /progress/        - User progress
GET /progress/stats   - Statistics
```

### Recommendations
```
GET /recommendations/         - Get recommendations
GET /recommendations/roadmap  - Learning roadmap
```

---

## 💻 Keyboard Shortcuts

### Browser DevTools
- `F12` - Open DevTools
- `Ctrl + Shift + C` - Inspect element
- `Ctrl + Shift + J` - Console
- `Ctrl + Shift + Delete` - Clear cache

### Terminal
- `Ctrl + C` - Stop server
- `Ctrl + L` - Clear terminal
- `↑` - Previous command

---

## 📱 Browser Console Commands

```javascript
// Test backend connection
fetch('http://localhost:8000/health')
  .then(r => r.json())
  .then(console.log)

// Check token
localStorage.getItem('token')

// Clear token
localStorage.removeItem('token')

// Run connection test
import('./utils/connectionTest.js')
  .then(m => m.testBackendConnection())
```

---

## 🎯 Verification Checklist

### Backend ✅
- [ ] Starts without errors
- [ ] http://localhost:8000/health returns healthy
- [ ] Database file created
- [ ] No error logs

### Frontend ✅
- [ ] Starts without errors
- [ ] http://localhost:8080 opens
- [ ] Console shows connection test
- [ ] No CORS errors

### Features ✅
- [ ] Can signup
- [ ] Can login
- [ ] Dashboard loads
- [ ] Can upload resume
- [ ] Can start interview
- [ ] Can take quiz

---

## 📞 Help Resources

### Quick Help
```bash
# Connection test
test-connection.bat

# View health
curl http://localhost:8000/health

# Check logs
# Backend: Terminal 1
# Frontend: Browser Console (F12)
```

### Documentation
- Quick Start: `QUICK_START_MR.md`
- Troubleshooting: `TROUBLESHOOTING_MR.md`
- Full Docs: `README_MR.md`
- This Guide: `QUICK_REFERENCE.md`

---

## 🔄 Common Workflows

### Development Workflow
```
1. Start servers (start-all.bat)
2. Open browser (localhost:8080)
3. Make changes
4. Auto-reload happens
5. Test changes
6. Repeat
```

### Debugging Workflow
```
1. Identify issue
2. Check logs (terminal + console)
3. Check network tab
4. Fix issue
5. Restart if needed
6. Test again
```

### Testing Workflow
```
1. Start servers
2. Open browser
3. Open DevTools (F12)
4. Test feature
5. Check console for errors
6. Check network for API calls
7. Verify results
```

---

## 💡 Pro Tips

1. **दोन terminals वापरा** - एक backend साठी, एक frontend साठी
2. **DevTools open ठेवा** - Errors लगेच दिसतात
3. **API Docs वापरा** - http://localhost:8000/docs
4. **Logs monitor करा** - Problems लवकर identify होतात
5. **Connection test करा** - Startup वर automatic run होतो

---

## 🎓 Learning Path

### Beginner
1. Read `START_HERE.md`
2. Follow `QUICK_START_MR.md`
3. Test basic features
4. Refer this quick reference

### Intermediate
1. Read `README_MR.md`
2. Explore API docs
3. Understand architecture
4. Customize features

### Advanced
1. Read `CONNECTION_FIX_SUMMARY.md`
2. Modify backend logic
3. Add new features
4. Deploy to production

---

## 📌 Bookmarks

### Essential URLs
```
Frontend:     http://localhost:8080
Backend:      http://localhost:8000
API Docs:     http://localhost:8000/docs
Health:       http://localhost:8000/health
```

### Essential Files
```
Start:        START_HERE.md
Quick Start:  QUICK_START_MR.md
This File:    QUICK_REFERENCE.md
Help:         TROUBLESHOOTING_MR.md
```

### Essential Commands
```
Start All:    start-all.bat
Test:         test-connection.bat
Backend:      cd backend && python main.py
Frontend:     npm run dev
```

---

**🎯 हा page bookmark करा - सर्व काही एका ठिकाणी!**

Print करून desk वर ठेवा! 📄
