# 📘 RUNBOOK - Healthcare RAG Assistant Operations Guide

**Version:** 0.4.0  
**Last Updated:** February 2026

## 🎯 Purpose

This runbook provides operational procedures for deploying, running, and maintaining the Healthcare Guidelines RAG Assistant.

---

## 📋 Table of Contents

1. [System Requirements](#system-requirements)
2. [Installation](#installation)
3. [Starting the System](#starting-the-system)
4. [Stopping the System](#stopping-the-system)
5. [Monitoring](#monitoring)
6. [Troubleshooting](#troubleshooting)
7. [Maintenance](#maintenance)
8. [Backup & Recovery](#backup--recovery)

---

## 🖥️ System Requirements

### Hardware
- **CPU:** 2+ cores recommended
- **RAM:** 4GB minimum, 8GB recommended
- **Storage:** 2GB minimum (includes model weights)
- **Network:** Internet required for Groq API calls

### Software
- **Python:** 3.10 or higher
- **OS:** Windows 10/11, macOS 10.15+, Ubuntu 20.04+
- **Browser:** Chrome, Firefox, or Edge (for Streamlit UI)

---

## 📦 Installation

### 1. Extract Project Files
```bash
# Extract the submission ZIP to desired location
cd /path/to/Healthcare_RAG_Kit
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

**Expected time:** 3-5 minutes

### 4. Configure Environment
```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your Groq API key
# Get key from: https://console.groq.com/keys
```

**.env file:**
```
LLM_PROVIDER=groq
GROQ_API_KEY=your_actual_api_key_here
```

### 5. Build Index (First Time Only)
```bash
python scripts/pipeline.py
```

**Expected output:**
```
Loading embedding model: sentence-transformers/all-MiniLM-L6-v2
✅ Model loaded. Embedding dimension: 384
Processing 69 documents...
Built index with 345 chunks -> index/faiss_index.bin
Index built.
```

**Expected time:** 30-60 seconds

---

## 🚀 Starting the System

### Option 1: API Server Only
```bash
# Start FastAPI server
uvicorn app.server:app --host 0.0.0.0 --port 9070 --reload
```

**Access points:**
- API Docs: http://localhost:9070/docs
- Health Check: http://localhost:9070/
- ReDoc: http://localhost:9070/redoc

### Option 2: API + Web Interface

**Terminal 1 (Backend):**
```bash
uvicorn app.server:app --host 0.0.0.0 --port 9070 --reload
```

**Terminal 2 (Frontend):**
```bash
streamlit run streamlit_app.py
```

**Access:**
- Streamlit UI: http://localhost:8501
- API Backend: http://localhost:9070/docs

### Option 3: Production Mode (No Auto-Reload)
```bash
# More stable for production
uvicorn app.server:app --host 0.0.0.0 --port 9070 --workers 2
```

---

## 🛑 Stopping the System

### Graceful Shutdown
```bash
# In the terminal running the server
Ctrl+C

# Wait for message:
# INFO:     Shutting down
# INFO:     Finished server process
```

### Force Kill (if needed)

**Windows:**
```powershell
# Find process using port 9070
netstat -ano | findstr :9070

# Kill process (replace PID with actual number)
taskkill /PID <PID> /F
```

**macOS/Linux:**
```bash
# Find process
lsof -i :9070

# Kill process
kill -9 <PID>
```

---

## 📊 Monitoring

### Health Check
```bash
# Quick health check
curl http://localhost:9070/

# Expected response:
# {
#   "status": "running",
#   "service": "Healthcare Guidelines RAG Assistant",
#   "version": "0.4.0",
#   "index_loaded": true,
#   "num_chunks": 345
# }
```

### System Stats
```bash
# Get system statistics
curl http://localhost:9070/stats

# Returns:
# - total_chunks
# - embedding_model
# - llm_model
# - performance metrics
```

### Log Monitoring
```bash
# Server logs appear in terminal
# Look for:
✅ "Application startup complete" - Server ready
✅ "Loading FAISS index" - Index loading
❌ "Error loading index" - Index not found
❌ "GROQ_API_KEY missing" - API key issue
```

---

## 🔧 Troubleshooting

### Common Issues

#### Issue 1: Server Won't Start

**Symptom:**
```
ERROR: [Errno 10048] error while attempting to bind on address
```

**Cause:** Port 9070 already in use

**Solution:**
```bash
# Option A: Kill existing process
netstat -ano | findstr :9070
taskkill /PID <PID> /F

# Option B: Use different port
uvicorn app.server:app --port 9071
```

---

#### Issue 2: Index Not Found

**Symptom:**
```
❌ Error loading index: [Errno 2] No such file or directory: 'index/faiss_index.bin'
```

**Solution:**
```bash
# Rebuild index
python scripts/pipeline.py
```

---

#### Issue 3: Import Errors

**Symptom:**
```
ModuleNotFoundError: No module named 'faiss'
```

**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

---

#### Issue 4: Groq API Errors

**Symptom:**
```
ValueError: GROQ_API_KEY missing in .env file
```

**Solution:**
```bash
# 1. Check .env file exists
ls .env

# 2. Verify content
cat .env  # macOS/Linux
type .env  # Windows

# 3. Ensure format is correct
GROQ_API_KEY=gsk_xxxxxxxxxxxxx
# (No quotes, no spaces around =)
```

---

#### Issue 5: Slow Response Times

**Symptom:** Queries take >10 seconds

**Possible causes:**
1. **Groq API rate limit** - Wait 1 minute and retry
2. **Network issues** - Check internet connection
3. **First query after startup** - Model initialization (normal)

**Solution:**
```bash
# Test API directly
curl -X POST http://localhost:9070/qa \
  -H "Content-Type: application/json" \
  -d '{"question":"When should hand hygiene be performed?","top_k":5}'
  
# Check response time in headers
```

---

#### Issue 6: Streamlit Connection Error

**Symptom:**
```
ConnectionError: Cannot connect to API
```

**Solution:**
```bash
# 1. Ensure backend is running
curl http://localhost:9070/

# 2. Check URL in streamlit_app.py
# Should be: API_URL = "http://localhost:9070"

# 3. Restart Streamlit
Ctrl+C
streamlit run streamlit_app.py
```

---

## 🔄 Maintenance

### Daily Checks
```bash
# 1. Verify server is running
curl http://localhost:9070/

# 2. Test query
python test_api.py

# 3. Check logs for errors
# (in server terminal)
```

### Weekly Tasks

- **Monitor Groq API usage** (if on paid plan)
- **Review low-confidence queries** in evaluation reports
- **Backup index files** (optional)

### Monthly Tasks

- **Update dependencies** (if needed)
```bash
  pip list --outdated
  pip install --upgrade <package>
```

- **Review system performance**
```bash
  python evaluation/eval_comprehensive.py
```

---

## 💾 Backup & Recovery

### What to Backup
```
Essential files:
├── index/faiss_index.bin      (FAISS index)
├── index/metadata.npz         (Metadata)
├── .env                       (API keys - SECURE!)
├── corpus/guidelines/         (Source documents)
└── evaluation/queries_custom.csv (Test queries)
```

### Backup Procedure
```bash
# Create backup directory
mkdir backup_$(date +%Y%m%d)

# Copy essential files
cp -r index/ backup_$(date +%Y%m%d)/
cp .env backup_$(date +%Y%m%d)/
cp -r corpus/ backup_$(date +%Y%m%d)/
```

### Recovery Procedure
```bash
# 1. Restore index files
cp -r backup_20260203/index/* index/

# 2. Restore .env
cp backup_20260203/.env .env

# 3. Restart server
uvicorn app.server:app --port 9070
```

### Rebuild from Scratch
```bash
# If index corrupted, rebuild from corpus
python scripts/pipeline.py

# Verify
python test_index.py
```

---

## 📞 Support

### Self-Service

1. **Check this runbook** for common issues
2. **Review README.md** for setup instructions
3. **Check logs** in server terminal
4. **Test with `test_api.py`**

### Escalation

If issues persist:
1. Document error messages
2. Note steps to reproduce
3. Check `evaluation/reports/` for system state
4. Contact system administrator

---

## 🔐 Security Notes

### API Key Protection

- ✅ **DO:** Store in `.env` file (not in code)
- ✅ **DO:** Add `.env` to `.gitignore`
- ❌ **DON'T:** Commit API keys to version control
- ❌ **DON'T:** Share `.env` file

### Production Deployment

If deploying to production:
- Use environment variables (not `.env` file)
- Enable HTTPS
- Add authentication
- Implement rate limiting
- Use dedicated server (not localhost)

---

## 📈 Performance Baselines

**Expected Performance (Local Machine):**
- **Retrieval time:** 100-200ms
- **LLM generation:** 2-5 seconds
- **Total response:** 3-6 seconds
- **Precision@5:** 93%+
- **Validation rate:** 75%+

**If performance degrades:**
1. Check internet connection (for Groq API)
2. Verify CPU isn't overloaded
3. Restart server
4. Rebuild index if needed

---

## 📝 Changelog

| Date | Version | Changes |
|------|---------|---------|
| Feb 2026 | 0.4.0 | Initial runbook creation |

---

**For detailed technical documentation, see:**
- `README.md` - Setup and usage
- `API_DOCUMENTATION.md` - API reference
- `TROUBLESHOOTING.md` - Extended troubleshooting