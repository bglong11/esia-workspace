# Docling Integration Guide

Complete guide for integrating Docling with ESIA Fact Extractor SaaS.

---

## 🎯 Architecture Overview

```
User Upload (FastAPI)
       ↓
   Job Created in DB
       ↓
Task Queued in Redis
       ↓
Celery Worker picks up task
       ↓
Docling Extracts PDF → Text (GPU)
       ↓
Qwen2.5:7B Extracts Facts → JSON (GPU)
       ↓
Results Stored in DB
       ↓
User Views in Browser
```

---

## 📋 Prerequisites

### 1. **Redis** (Message Broker)

**Installation:**

```bash
# Ubuntu/Debian
sudo apt install redis-server
sudo systemctl start redis

# macOS
brew install redis
brew services start redis

# Windows (via WSL or Docker)
docker run -d -p 6379:6379 redis:latest

# Verify
redis-cli ping
# Should return: PONG
```

### 2. **Docling** (Your Standalone Program)

Ensure your docling script:
- ✅ Accepts PDF path as argument
- ✅ Outputs text to stdout OR saves to file
- ✅ Has proper error handling
- ✅ Can run on GPU

**Example expected interface:**

```bash
# Option A: Output to stdout
python docling_standalone.py input.pdf > output.txt

# Option B: Output to file
python docling_standalone.py input.pdf output.txt
```

### 3. **GPU Access** (for Docling)

Make sure your Celery worker can access the GPU:

```bash
# Check CUDA availability
python -c "import torch; print(torch.cuda.is_available())"

# Check GPU
nvidia-smi
```

---

## 🛠️ Installation

### Step 1: Install Python Dependencies

```bash
cd saas/backend
pip install -r requirements_with_docling.txt
```

### Step 2: Install Docling

Follow Docling's official installation:
```bash
# In a separate environment or same environment
pip install docling
# Follow specific GPU setup instructions from docling docs
```

### Step 3: Configure Environment Variables

Create `.env` file in `saas/backend/`:

```bash
# Database
DATABASE_URL=sqlite:///./esia_saas.db

# Redis
REDIS_URL=redis://localhost:6379/0

# Ollama (for LLM)
OLLAMA_BASE_URL=http://localhost:11434

# Docling
DOCLING_SCRIPT_PATH=/path/to/your/docling_standalone.py
```

---

## 🚀 Running the Application

You need to run **3 services**:

### Terminal 1: Redis (if not running as service)

```bash
redis-server
```

### Terminal 2: Celery Worker (GPU machine)

```bash
cd saas/backend

# Start Celery worker
celery -A celery_app worker \
    --loglevel=info \
    --concurrency=1 \
    --pool=solo

# Options explained:
# --concurrency=1  : One task at a time (for GPU)
# --pool=solo      : Single process (better for GPU)
```

**On Windows:**
```powershell
celery -A celery_app worker --loglevel=info --pool=solo
```

### Terminal 3: FastAPI Server

```bash
cd saas/backend
python main_with_celery.py
```

Then open: **http://localhost:8000**

---

## 🔧 Adapting Your Docling Script

### Option 1: Docling Outputs to Stdout (Recommended)

If your script prints extracted text:

```python
# docling_standalone.py
import sys
from docling import extract_pdf  # Your docling import

def main():
    pdf_path = sys.argv[1]
    text = extract_pdf(pdf_path)  # Your docling function
    print(text)  # Output to stdout

if __name__ == "__main__":
    main()
```

**tasks.py uses it like this:**
```python
result = subprocess.run(
    ['python', docling_script_path, file_path],
    capture_output=True,
    text=True,
    timeout=600
)
extracted_text = result.stdout
```

### Option 2: Docling Saves to File

If your script saves to a file:

```python
# docling_standalone.py
import sys
from docling import extract_pdf

def main():
    pdf_path = sys.argv[1]
    output_path = sys.argv[2]
    text = extract_pdf(pdf_path)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)

if __name__ == "__main__":
    main()
```

**Update tasks.py (line 45-55):**
```python
# Uncomment Option B in tasks.py
output_file = file_path.replace('.pdf', '_docling.md')
result = subprocess.run(
    ['python', docling_script_path, file_path, output_file],
    check=True,
    timeout=600
)
with open(output_file, 'r', encoding='utf-8') as f:
    extracted_text = f.read()
```

### Option 3: Import Docling Directly

If you want to import docling as a library:

**Update tasks.py:**
```python
# Instead of subprocess, import directly
from your_docling_module import extract_pdf

# In the task:
extracted_text = extract_pdf(file_path)
```

---

## 🧪 Testing

### Test 1: Upload a PDF

1. Start all services (Redis, Celery, FastAPI)
2. Open http://localhost:8000
3. Upload a PDF
4. Watch the Celery terminal for progress logs
5. Check results in browser

### Test 2: Monitor Celery Tasks

```bash
# Check active tasks
celery -A celery_app inspect active

# Check worker stats
celery -A celery_app inspect stats

# Purge all tasks (careful!)
celery -A celery_app purge
```

### Test 3: Check Redis Queue

```bash
redis-cli
> KEYS *
> LLEN celery  # Check queue length
```

---

## 📊 Monitoring & Debugging

### View Celery Logs

Celery worker terminal shows:
- Task received
- Task progress
- Docling extraction status
- LLM processing
- Task completion

### View FastAPI Logs

FastAPI terminal shows:
- Upload requests
- Job creation
- API calls

### Check Database

```bash
cd saas/backend
sqlite3 esia_saas.db

sqlite> SELECT * FROM jobs ORDER BY created_at DESC LIMIT 5;
sqlite> SELECT status, COUNT(*) FROM jobs GROUP BY status;
```

---

## ⚡ Performance Optimization

### GPU Memory Management

**Single GPU:** Run one worker with `concurrency=1`

```bash
celery -A celery_app worker --concurrency=1 --pool=solo
```

**Multiple GPUs:** Run separate workers per GPU

```bash
# Terminal 1 (GPU 0)
CUDA_VISIBLE_DEVICES=0 celery -A celery_app worker -n worker1@%h --concurrency=1

# Terminal 2 (GPU 1)
CUDA_VISIBLE_DEVICES=1 celery -A celery_app worker -n worker2@%h --concurrency=1
```

### Batch Processing

For multiple uploads, Celery automatically queues and processes them:
- Uploads are instant (just saves file + creates job)
- Processing happens in background on GPU
- Users can upload multiple files without waiting

---

## 🚨 Troubleshooting

### Error: "Connection refused to Redis"

```bash
# Check if Redis is running
redis-cli ping

# Start Redis
redis-server
```

### Error: "No active workers"

```bash
# Check workers
celery -A celery_app inspect active

# Start worker
celery -A celery_app worker --loglevel=info --pool=solo
```

### Error: "Docling extraction failed"

Check Celery worker logs for:
- Python path issues
- GPU not available
- Docling dependencies missing

**Fix:**
```bash
# Test docling standalone
python /path/to/docling_standalone.py test.pdf

# Check GPU in Celery environment
celery -A celery_app shell
>>> import torch
>>> print(torch.cuda.is_available())
```

### Tasks Stuck in Queue

```bash
# View active tasks
celery -A celery_app inspect active

# Revoke stuck task
celery -A celery_app revoke <task_id> --terminate

# Purge all pending
celery -A celery_app purge
```

---

## 🎯 Production Deployment

### Docker Compose Setup

```yaml
version: '3.8'

services:
  redis:
    image: redis:latest
    ports:
      - "6379:6379"

  fastapi:
    build: ./saas/backend
    ports:
      - "8000:8000"
    environment:
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - redis

  celery_worker:
    build: ./saas/backend
    command: celery -A celery_app worker --loglevel=info --pool=solo
    environment:
      - REDIS_URL=redis://redis:6379/0
    runtime: nvidia  # For GPU access
    depends_on:
      - redis
```

### Systemd Services

Create service files for production:

**`/etc/systemd/system/esia-celery.service`:**
```ini
[Unit]
Description=ESIA Celery Worker
After=network.target redis.target

[Service]
Type=forking
User=your-user
WorkingDirectory=/path/to/saas/backend
ExecStart=/usr/local/bin/celery -A celery_app worker --detach --loglevel=info --pool=solo

[Install]
WantedBy=multi-user.target
```

---

## 📈 Scaling

### Horizontal Scaling

Run multiple Celery workers:

**Worker 1 (GPU Server 1):**
```bash
celery -A celery_app worker -n worker1@gpu1 --concurrency=1
```

**Worker 2 (GPU Server 2):**
```bash
celery -A celery_app worker -n worker2@gpu2 --concurrency=1
```

Both workers pull from the same Redis queue!

### Load Balancing

For FastAPI, use Nginx:

```nginx
upstream fastapi_backend {
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
    server 127.0.0.1:8003;
}

server {
    listen 80;
    location / {
        proxy_pass http://fastapi_backend;
    }
}
```

---

## ✅ Checklist

Before going live:

- [ ] Redis is running and accessible
- [ ] Celery worker can access GPU
- [ ] Docling script path is correct in .env
- [ ] Test upload with sample PDF
- [ ] Monitor logs for errors
- [ ] Check database for results
- [ ] Export CSV works
- [ ] Add error notifications (email/Slack)
- [ ] Set up monitoring (Flower, Prometheus)
- [ ] Configure backups for database

---

## 🎓 Next Steps

1. **Test with your docling script**
2. **Adjust timeout settings** if needed (tasks.py line 42)
3. **Add progress WebSocket** for real-time updates
4. **Set up Flower** for Celery monitoring:
   ```bash
   pip install flower
   celery -A celery_app flower
   # Open http://localhost:5555
   ```
5. **Implement retry logic** for failed tasks
6. **Add email notifications** when jobs complete

---

**Questions?** Check the main [README](README.md) or review the code in:
- `celery_app.py` - Celery configuration
- `tasks.py` - Background tasks
- `main_with_celery.py` - FastAPI with Celery
