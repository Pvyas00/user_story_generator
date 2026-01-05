# 📖 User Story Generator - Operational Manual

## Table of Contents
1. [System Overview](#system-overview)
2. [Architecture](#architecture)
3. [Installation & Setup](#installation--setup)
4. [API Endpoints](#api-endpoints)
5. [Data Models](#data-models)
6. [Component Details](#component-details)
7. [Configuration](#configuration)
8. [Deployment](#deployment)
9. [Troubleshooting](#troubleshooting)
10. [Maintenance](#maintenance)

---

## System Overview

### Purpose
Enterprise-grade AI-powered user story generation platform with coverage analysis and multi-format export capabilities.

### Key Features
- ✅ AI-powered requirement analysis
- ✅ Enterprise coverage scoring
- ✅ Intelligent story generation
- ✅ Multi-format export (Word, PDF, PNG)
- ✅ Real-time analytics dashboard
- ✅ Corporate branding support

### Technology Stack
```
Backend:     Flask (Python 3.8+)
AI Service:  Groq API
Frontend:    Vanilla JavaScript, HTML5, CSS3
Documents:   python-docx, ReportLab, PIL
Config:      python-dotenv
```

---

## Architecture

### System Architecture Diagram
```
┌─────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Browser    │  │  Mobile App  │  │  API Client  │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
└─────────┼──────────────────┼──────────────────┼─────────────┘
          │                  │                  │
          └──────────────────┼──────────────────┘
                             │
┌────────────────────────────┼─────────────────────────────────┐
│                     APPLICATION LAYER                         │
│                             │                                 │
│  ┌─────────────────────────▼──────────────────────────────┐  │
│  │              Flask Application (app.py)                │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐            │  │
│  │  │  Routes  │  │  Errors  │  │  Config  │            │  │
│  │  └──────────┘  └──────────┘  └──────────┘            │  │
│  └────────────────────────┬───────────────────────────────┘  │
└───────────────────────────┼──────────────────────────────────┘
                            │
┌───────────────────────────┼──────────────────────────────────┐
│                    BUSINESS LOGIC LAYER                       │
│  ┌────────────────┬───────┴────────┬────────────────┐        │
│  │                │                │                │        │
│  ▼                ▼                ▼                ▼        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │  Groq    │  │  Story   │  │  Story   │  │  Field   │    │
│  │  Client  │  │  Parser  │  │ Exporter │  │Questions │    │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └──────────┘    │
└───────┼─────────────┼─────────────┼────────────────────────┘
        │             │             │
┌───────┼─────────────┼─────────────┼────────────────────────┐
│       │             │             │                         │
│  ┌────▼─────┐  ┌────▼─────┐  ┌────▼─────┐                 │
│  │  Groq    │  │   JSON   │  │   File   │                 │
│  │   API    │  │  Parser  │  │  System  │                 │
│  └──────────┘  └──────────┘  └──────────┘                 │
│                    EXTERNAL LAYER                           │
└─────────────────────────────────────────────────────────────┘
```

### Component Interaction Flow
```
User Request
    ↓
Flask Router (app.py)
    ↓
┌───────────────────────────────────┐
│  Request Type?                    │
├───────────────────────────────────┤
│  /analyze    → GroqClient         │
│  /generate   → GroqClient + Parser│
│  /export     → StoryExporter      │
│  /health     → System Check       │
└───────────────────────────────────┘
    ↓
Response Processing
    ↓
JSON/File Response
    ↓
Client Receives Data
```

---

## Installation & Setup

### Prerequisites
```bash
# Required Software
- Python 3.8 or higher
- pip (Python package manager)
- Git (for version control)
- Text editor (VS Code recommended)

# Optional
- Virtual environment tool (venv/virtualenv)
- Postman (for API testing)
```

### Step-by-Step Installation

#### 1. Clone Repository
```bash
git clone <repository-url>
cd user_story_generator
```

#### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Environment Configuration
Create `.env` file in root directory:
```env
# Required
GROQ_API_KEY=your_groq_api_key_here
SECRET_KEY=your_secret_key_here

# Optional
PORT=5000
FLASK_ENV=development
DEBUG=True
```

#### 5. Verify Installation
```bash
python app.py
```

Expected output:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://0.0.0.0:5000
```

#### 6. Test Application
Open browser: `http://localhost:5000`

---

## API Endpoints

### Base URL
```
Development: http://localhost:5000
Production:  https://your-domain.com
```

---

### 1. Homepage

#### **GET /**
Serves the main application interface.

**Request:**
```http
GET / HTTP/1.1
Host: localhost:5000
```

**Response:**
```html
HTTP/1.1 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html>
...
</html>
```

**Usage Example:**
```bash
curl http://localhost:5000/
```

---

### 2. Analyze Requirement

#### **POST /analyze**
Analyzes requirement text for enterprise coverage.

**Request:**
```http
POST /analyze HTTP/1.1
Host: localhost:5000
Content-Type: application/json

{
  "requirement": "I need a user login system with email and password"
}
```

**Response (Success):**
```json
{
  "coverage_analysis": {
    "present_elements": [
      {
        "element": "Business Goal",
        "details": "User authentication system identified"
      },
      {
        "element": "Actor",
        "details": "End user identified as primary actor"
      }
    ],
    "missing_elements": [
      {
        "element": "Security Requirements",
        "details": "No security specifications mentioned",
        "suggested_content": "Password encryption, session management"
      },
      {
        "element": "Acceptance Criteria",
        "details": "Success criteria not defined",
        "suggested_content": "Define login success/failure scenarios"
      }
    ],
    "editable_recommendations": [
      {
        "element": "Security Requirements",
        "question": "What security measures should be implemented?",
        "suggested_answer": "Password hashing, JWT tokens, rate limiting",
        "field_type": "textarea"
      }
    ],
    "overall_score": 65,
    "enterprise_readiness": "Moderate"
  }
}
```

**Response (Error):**
```json
{
  "error": "Requirement text is required"
}
```

**Status Codes:**
- `200` - Analysis successful
- `400` - Invalid/missing requirement
- `500` - Analysis failed (AI error)

**Usage Examples:**

**cURL:**
```bash
curl -X POST http://localhost:5000/analyze \
  -H "Content-Type: application/json" \
  -d '{"requirement": "User login system"}'
```

**JavaScript:**
```javascript
fetch('http://localhost:5000/analyze', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    requirement: 'User login system'
  })
})
.then(res => res.json())
.then(data => console.log(data));
```

**Python:**
```python
import requests

response = requests.post(
    'http://localhost:5000/analyze',
    json={'requirement': 'User login system'}
)
print(response.json())
```

---

### 3. Generate Story

#### **POST /generate**
Generates complete user story from requirement and answers.

**Request:**
```http
POST /generate HTTP/1.1
Host: localhost:5000
Content-Type: application/json

{
  "requirement": "User login system with email and password",
  "answers": {
    "Security Requirements": "Password hashing with bcrypt, JWT tokens",
    "Acceptance Criteria": "User can login with valid credentials"
  },
  "coverage_analysis": {
    "overall_score": 85,
    "enterprise_readiness": "High"
  }
}
```

**Response (Success):**
```json
{
  "business_goal": "Enable secure user authentication to protect user accounts and provide personalized experience",
  "actor": "End User, System Administrator",
  "trigger": "User navigates to login page and enters credentials",
  "preconditions": [
    "User must have a registered account",
    "System must be operational",
    "Database connection must be active"
  ],
  "functional_flow": [
    "User navigates to login page",
    "User enters email and password",
    "System validates input format",
    "System checks credentials against database",
    "System generates JWT token on success",
    "User is redirected to dashboard"
  ],
  "validations": [
    "Email format must be valid",
    "Password must meet complexity requirements",
    "Account must not be locked",
    "Maximum 5 login attempts allowed"
  ],
  "acceptance_criteria": [
    "User can login with valid credentials",
    "Invalid credentials show error message",
    "Account locks after 5 failed attempts",
    "Session expires after 30 minutes of inactivity"
  ],
  "security": [
    "Passwords hashed using bcrypt",
    "JWT tokens for session management",
    "HTTPS required for all authentication",
    "Rate limiting on login endpoint"
  ],
  "dependencies": [
    "Database service must be running",
    "Email service for password reset",
    "Redis for session storage"
  ],
  "risks": [
    "Brute force attacks on login endpoint",
    "Session hijacking if JWT compromised",
    "Database connection failures"
  ]
}
```

**Response (Error):**
```json
{
  "error": "Failed to generate user story"
}
```

**Status Codes:**
- `200` - Generation successful
- `400` - Invalid/missing requirement
- `500` - Generation failed

**Usage Examples:**

**cURL:**
```bash
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "requirement": "User login system",
    "answers": {"Security": "JWT tokens"},
    "coverage_analysis": {"overall_score": 85}
  }'
```

**JavaScript:**
```javascript
const response = await fetch('http://localhost:5000/generate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    requirement: 'User login system',
    answers: { 'Security': 'JWT tokens' },
    coverage_analysis: { overall_score: 85 }
  })
});
const story = await response.json();
```

---

### 4. Export Story

#### **POST /export/{format_type}**
Exports user story to specified format.

**Path Parameters:**
- `format_type`: `word` | `pdf` | `png`

**Request:**
```http
POST /export/word HTTP/1.1
Host: localhost:5000
Content-Type: application/json

{
  "story_data": {
    "business_goal": "Enable secure user authentication",
    "actor": "End User",
    "trigger": "User navigates to login page",
    "functional_flow": ["Step 1", "Step 2"],
    "acceptance_criteria": ["Criteria 1"]
  },
  "coverage_data": {
    "overall_score": 85,
    "enterprise_readiness": "High"
  }
}
```

**Response (Success):**
```
HTTP/1.1 200 OK
Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document
Content-Disposition: attachment; filename="user_story.docx"

[Binary file data]
```

**Response (Error):**
```json
{
  "error": "Story data is required"
}
```

**Status Codes:**
- `200` - Export successful (file download)
- `400` - Invalid data or format
- `500` - Export failed

**Format-Specific Details:**

| Format | Extension | MIME Type | Use Case |
|--------|-----------|-----------|----------|
| word | .docx | application/vnd.openxmlformats-officedocument.wordprocessingml.document | Editable documents |
| pdf | .pdf | application/pdf | Print-ready, shareable |
| png | .png | image/png | Visual snapshots |

**Usage Examples:**

**cURL (Word):**
```bash
curl -X POST http://localhost:5000/export/word \
  -H "Content-Type: application/json" \
  -d '{"story_data": {...}, "coverage_data": {...}}' \
  --output user_story.docx
```

**JavaScript (PDF):**
```javascript
const response = await fetch('http://localhost:5000/export/pdf', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    story_data: storyData,
    coverage_data: coverageData
  })
});

const blob = await response.blob();
const url = window.URL.createObjectURL(blob);
const a = document.createElement('a');
a.href = url;
a.download = 'user_story.pdf';
a.click();
```

**Python (PNG):**
```python
import requests

response = requests.post(
    'http://localhost:5000/export/png',
    json={
        'story_data': story_data,
        'coverage_data': coverage_data
    }
)

with open('user_story.png', 'wb') as f:
    f.write(response.content)
```

---

### 5. Health Check

#### **GET /health**
System health and configuration status.

**Request:**
```http
GET /health HTTP/1.1
Host: localhost:5000
```

**Response:**
```json
{
  "status": "healthy",
  "groq_configured": true
}
```

**Status Codes:**
- `200` - Always returns 200

**Usage Example:**
```bash
curl http://localhost:5000/health
```

---

## Data Models

### Request Models

#### RequirementAnalysisRequest
```typescript
{
  requirement: string  // Required, 1-5000 characters
}
```

#### StoryGenerationRequest
```typescript
{
  requirement: string,           // Required
  answers?: {                    // Optional
    [element: string]: string
  },
  coverage_analysis?: {          // Optional
    overall_score: number,
    enterprise_readiness: string
  }
}
```

#### ExportRequest
```typescript
{
  story_data: {                  // Required
    business_goal: string,
    actor: string,
    trigger: string,
    preconditions: string[],
    functional_flow: string[],
    validations: string[],
    acceptance_criteria: string[],
    security: string[],
    dependencies: string[],
    risks: string[]
  },
  coverage_data?: {              // Optional
    overall_score: number,
    enterprise_readiness: string,
    present_elements: Array<{
      element: string,
      details: string
    }>,
    missing_elements: Array<{
      element: string,
      details: string
    }>
  }
}
```

### Response Models

#### CoverageAnalysis
```typescript
{
  coverage_analysis: {
    present_elements: Array<{
      element: string,
      details: string
    }>,
    missing_elements: Array<{
      element: string,
      details: string,
      suggested_content: string
    }>,
    editable_recommendations: Array<{
      element: string,
      question: string,
      suggested_answer: string,
      field_type: "textarea"
    }>,
    overall_score: number,        // 0-100
    enterprise_readiness: string  // "Low" | "Moderate" | "High" | "Enterprise-Ready"
  }
}
```

#### StoryData
```typescript
{
  business_goal: string,
  actor: string,
  trigger: string,
  preconditions: string[],
  functional_flow: string[],
  validations: string[],
  acceptance_criteria: string[],
  security: string[],
  dependencies: string[],
  risks: string[]
}
```

#### ErrorResponse
```typescript
{
  error: string  // Descriptive error message
}
```

---

## Component Details

### 1. Flask Application (app.py)

**Purpose:** Main application entry point and request router

**Responsibilities:**
- HTTP request handling
- Route management
- Error handling
- Component orchestration
- Response formatting

**Key Functions:**
```python
index()                  # Serves homepage
analyze_requirement()    # Handles /analyze endpoint
generate_story()         # Handles /generate endpoint
export_story()           # Handles /export endpoint
health_check()           # Handles /health endpoint
```

**Configuration:**
```python
SECRET_KEY: From environment variable
DEBUG: Based on FLASK_ENV
HOST: 0.0.0.0 (all interfaces)
PORT: From environment (default 5000)
```

---

### 2. GroqClient (llm_client.py)

**Purpose:** AI service integration for analysis and generation

**Responsibilities:**
- Groq API communication
- Prompt engineering
- Response parsing
- Error handling
- Rate limit management

**Key Methods:**
```python
analyze_requirement_coverage(requirement: str) -> dict
generate_story(requirement: str, answers: dict, coverage: dict) -> dict
```

**Configuration:**
```python
API_KEY: From GROQ_API_KEY environment variable
MODEL: Groq LLM model (e.g., mixtral-8x7b)
TIMEOUT: 30 seconds
MAX_RETRIES: 3
```

---

### 3. StoryParser (story_parser.py)

**Purpose:** Parse AI responses into structured format

**Responsibilities:**
- Text parsing
- JSON extraction
- Field validation
- Data normalization
- Error recovery

**Key Methods:**
```python
parse_story(story_text: str) -> dict
validate_fields(story_data: dict) -> bool
normalize_data(raw_data: dict) -> dict
```

---

### 4. EnhancedStoryExporter (story_exporter_enhanced.py)

**Purpose:** Multi-format document generation

**Responsibilities:**
- Word document generation
- PDF creation
- PNG image generation
- Template management
- Corporate styling

**Key Methods:**
```python
export_story(story_data: dict, format: str, coverage: dict) -> str
_export_word(story_data: dict, coverage: dict) -> str
_export_pdf(story_data: dict, coverage: dict) -> str
_export_png(story_data: dict) -> str
```

**Supported Formats:**
- Word (.docx) - Editable documents
- PDF (.pdf) - Print-ready format
- PNG (.png) - Visual snapshots

---

## Configuration

### Environment Variables

#### Required Variables
```env
# Groq AI API Key (Required)
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxx

# Flask Secret Key (Required for production)
SECRET_KEY=your-secret-key-minimum-32-characters
```

#### Optional Variables
```env
# Server Configuration
PORT=5000
HOST=0.0.0.0

# Environment Mode
FLASK_ENV=development  # or production
DEBUG=True             # or False

# Logging
LOG_LEVEL=INFO
LOG_FILE=app.log
```

### Application Configuration

#### Flask Settings
```python
app.config['SECRET_KEY']           # Security key
app.config['MAX_CONTENT_LENGTH']   # Max upload size
app.config['JSON_SORT_KEYS']       # JSON key sorting
```

#### Component Settings
```python
# Temp Directory
TEMP_DIR = tempfile.gettempdir()

# Logo Path
LOGO_PATH = 'static/images/anand_rathi_logo.png'

# Export Formats
SUPPORTED_FORMATS = ['word', 'pdf', 'png']
```

---

## Deployment

### Development Deployment

#### Local Development
```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Run development server
python app.py

# Access application
http://localhost:5000
```

#### Development Features
- Auto-reload on code changes
- Detailed error messages
- Debug toolbar
- Console logging

---

### Production Deployment

#### Option 1: Gunicorn (Recommended)
```bash
# Install Gunicorn
pip install gunicorn

# Run with 4 workers
gunicorn --bind 0.0.0.0:5000 --workers 4 app:app

# With configuration file
gunicorn -c gunicorn_config.py app:app
```

**gunicorn_config.py:**
```python
bind = "0.0.0.0:5000"
workers = 4
worker_class = "sync"
timeout = 120
keepalive = 5
errorlog = "error.log"
accesslog = "access.log"
loglevel = "info"
```

#### Option 2: uWSGI
```bash
# Install uWSGI
pip install uwsgi

# Run server
uwsgi --http :5000 --module app:app --processes 4
```

#### Option 3: Docker
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

**Build and Run:**
```bash
docker build -t user-story-generator .
docker run -p 5000:5000 --env-file .env user-story-generator
```

---

### Nginx Reverse Proxy

**nginx.conf:**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /path/to/app/static;
        expires 30d;
    }
}
```

---

## Troubleshooting

### Common Issues

#### 1. Application Won't Start

**Symptom:**
```
ModuleNotFoundError: No module named 'flask'
```

**Solution:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

---

#### 2. API Key Error

**Symptom:**
```json
{
  "error": "Failed to analyze requirement coverage"
}
```

**Solution:**
```bash
# Check .env file exists
ls -la .env

# Verify API key is set
echo $GROQ_API_KEY

# Test API key
curl https://api.groq.com/v1/health \
  -H "Authorization: Bearer $GROQ_API_KEY"
```

---

#### 3. Export Fails

**Symptom:**
```json
{
  "error": "Export failed"
}
```

**Solution:**
```bash
# Check temp directory permissions
ls -ld /tmp

# Verify logo file exists
ls -l static/images/anand_rathi_logo.png

# Check disk space
df -h
```

---

#### 4. Port Already in Use

**Symptom:**
```
OSError: [Errno 48] Address already in use
```

**Solution:**
```bash
# Find process using port 5000
lsof -i :5000

# Kill process
kill -9 <PID>

# Or use different port
PORT=5001 python app.py
```

---

### Debug Mode

Enable detailed logging:
```python
# In app.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

Check logs:
```bash
# View application logs
tail -f app.log

# View error logs
tail -f error.log
```

---

## Maintenance

### Regular Tasks

#### Daily
- Monitor error logs
- Check API usage/limits
- Verify system health endpoint

#### Weekly
- Review application logs
- Update dependencies (security patches)
- Backup configuration files

#### Monthly
- Performance analysis
- Dependency updates
- Security audit

---

### Monitoring

#### Health Check Monitoring
```bash
# Automated health check
*/5 * * * * curl -f http://localhost:5000/health || alert
```

#### Log Monitoring
```bash
# Watch for errors
tail -f error.log | grep ERROR

# Count requests
grep "POST /generate" access.log | wc -l
```

---

### Backup & Recovery

#### Configuration Backup
```bash
# Backup .env file
cp .env .env.backup

# Backup application
tar -czf backup-$(date +%Y%m%d).tar.gz \
  app.py \
  llm_client.py \
  story_parser.py \
  story_exporter_enhanced.py \
  templates/ \
  static/
```

#### Recovery
```bash
# Restore from backup
tar -xzf backup-20240101.tar.gz

# Restore environment
cp .env.backup .env

# Restart application
systemctl restart user-story-generator
```

---

### Performance Optimization

#### Caching
```python
# Add Redis caching
from flask_caching import Cache

cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': 'redis://localhost:6379/0'
})

@cache.cached(timeout=300)
def analyze_requirement():
    # Cached for 5 minutes
    pass
```

#### Database Integration
```python
# Add PostgreSQL for story persistence
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@localhost/db'
db = SQLAlchemy(app)
```

---

### Security Updates

#### Update Dependencies
```bash
# Check for updates
pip list --outdated

# Update specific package
pip install --upgrade flask

# Update all packages
pip install --upgrade -r requirements.txt
```

#### Security Scan
```bash
# Install safety
pip install safety

# Run security check
safety check

# Check for vulnerabilities
pip-audit
```

---

## Support & Contact

### Documentation
- API Documentation: `/docs` (if implemented)
- GitHub Repository: `<repo-url>`
- Issue Tracker: `<issues-url>`

### Getting Help
1. Check this operational manual
2. Review troubleshooting section
3. Check application logs
4. Contact development team

---

## Appendix

### A. File Structure
```
user_story_generator/
├── app.py                          # Main application
├── llm_client.py                   # AI integration
├── story_parser.py                 # Data parser
├── story_exporter_enhanced.py      # Export engine
├── field_questions.py              # Field definitions
├── requirements.txt                # Dependencies
├── .env                            # Environment config
├── templates/
│   └── index.html                  # Frontend template
├── static/
│   ├── style.css                   # Styles
│   ├── app.js                      # Frontend logic
│   └── images/
│       └── anand_rathi_logo.png    # Corporate logo
└── OPERATIONAL_MANUAL.md           # This file
```

### B. Quick Reference

#### Start Application
```bash
python app.py
```

#### Test Endpoints
```bash
# Health check
curl http://localhost:5000/health

# Analyze
curl -X POST http://localhost:5000/analyze \
  -H "Content-Type: application/json" \
  -d '{"requirement": "test"}'
```

#### Stop Application
```bash
# Ctrl+C in terminal
# Or kill process
pkill -f "python app.py"
```

---

**Document Version:** 1.0  
**Last Updated:** 2024  
**Maintained By:** Development Team
