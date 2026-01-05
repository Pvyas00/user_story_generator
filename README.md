# 🚀 AI User Story Generator

An enterprise-grade AI-powered application that transforms business requirements into comprehensive user stories with visual context support.

## ✨ Features

### 🎯 **Core Functionality**
- **AI-Powered Analysis** - Intelligent requirement coverage analysis
- **Enterprise-Ready Stories** - Complete 10-element user stories
- **Visual Context** - Image/document attachment support
- **Professional Export** - Word, PDF, PNG formats
- **Real-time Validation** - Input validation and error handling

### 📎 **File Attachment Support**
- **Supported Formats:** JPEG, PNG, PDF, DOCX
- **File Size Limit:** 5MB per file, 25MB total
- **Visual Preview:** Image thumbnails and file icons
- **Drag & Drop:** Easy file attachment interface

### 📄 **Export Options**
- **Microsoft Word** - Professional corporate formatting
- **PDF Document** - Print-ready format
- **PNG Image** - Visual story representation

## 🛠️ **Technology Stack**

### **Backend**
- **Flask** - Python web framework
- **Groq API** - AI language model integration
- **python-docx** - Word document generation
- **ReportLab** - PDF creation
- **Pillow** - Image processing

### **Frontend**
- **HTML5/CSS3** - Modern responsive design
- **Vanilla JavaScript** - No framework dependencies
- **File API** - Native browser file handling

## 📋 **Prerequisites**

- Python 3.8+
- Groq API Key
- Modern web browser

## 🚀 **Quick Start**

### 1. **Clone Repository**
```bash
git clone <repository-url>
cd user_story_generator
```

### 2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 3. **Environment Setup**
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your credentials
GROQ_API_KEY=your_groq_api_key_here
SECRET_KEY=your_secure_secret_key
```

### 4. **Run Application**
```bash
python app.py
```

### 5. **Access Application**
Open browser: `http://localhost:5000`

## 🔧 **Configuration**

### **Environment Variables**
```env
# Groq API Configuration
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-8b-instant
GROQ_TEMPERATURE=0.3
GROQ_MAX_TOKENS=3000

# Flask Configuration
SECRET_KEY=your_secret_key_here
FLASK_ENV=development
PORT=5000
```

### **File Upload Limits**
- **Individual File:** 5MB maximum
- **Total Upload:** 25MB per request
- **Supported Types:** .jpg, .jpeg, .png, .pdf, .docx

## 📖 **Usage Guide**

### **Step 1: Enter Requirement**
1. Type your business requirement (1-3 lines)
2. Click 📎 button to attach supporting files
3. Click "Analyze Requirement"

### **Step 2: Review Coverage**
- View covered enterprise elements
- See missing elements analysis
- Fill in recommended information

### **Step 3: Generate Story**
- Click "Generate Enterprise Story"
- Review complete 10-element user story
- Export in desired format

## 🏗️ **Project Structure**

```
user_story_generator/
├── app.py                      # Main Flask application
├── llm_client.py              # Groq AI integration
├── story_parser.py            # Data validation & parsing
├── story_exporter_enhanced.py # Document generation
├── field_questions.py         # Field definitions
├── constants.py               # Fallback data
├── templates/
│   └── index.html            # Frontend interface
├── static/
│   ├── app.js               # JavaScript functionality
│   ├── style.css            # Styling
│   └── images/              # Assets
├── prompts/
│   ├── analyze_requirement.txt    # AI analysis prompt
│   └── generate_story.txt         # AI generation prompt
├── requirements.txt          # Python dependencies
├── .env.example             # Environment template
└── README.md               # This file
```

## 🎨 **Enterprise Elements**

The application generates user stories with all 10 essential enterprise elements:

1. **🎯 Business Goal** - Why this feature exists
2. **👤 Actor** - Who will use this feature
3. **⚡ Trigger** - What initiates this action
4. **📋 Preconditions** - Required system state
5. **🔄 Functional Flow** - Step-by-step process
6. **✅ Validations** - Data/input checks
7. **🎯 Acceptance Criteria** - Success conditions
8. **🔒 Security** - Protection measures
9. **🔗 Dependencies** - External requirements
10. **⚠️ Risks** - Potential issues & mitigation

## 🔒 **Security Features**

- **API Key Protection** - Environment variable storage
- **File Validation** - Type and size restrictions
- **Input Sanitization** - XSS prevention
- **Secure Headers** - CSRF protection
- **Error Handling** - No sensitive data exposure

## 🚀 **Production Deployment**

### **Using Gunicorn**
```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 app:app
```

### **Environment Setup**
```bash
export GROQ_API_KEY="your_actual_api_key"
export SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
export FLASK_ENV="production"
```

### **Health Check**
Visit `/health` endpoint to verify configuration.

## 🐛 **Troubleshooting**

### **Common Issues**

**API Key Error (401)**
```
Solution: Check GROQ_API_KEY in .env file
Verify key is active in Groq console
```

**File Upload Not Working**
```
Solution: Check file size (<5MB) and format
Ensure JavaScript is enabled
```

**Export Fails**
```
Solution: Check temp directory permissions
Verify all dependencies installed
```

## 📝 **API Endpoints**

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Serve main interface |
| `/analyze` | POST | Analyze requirement coverage |
| `/generate` | POST | Generate user story |
| `/export/<format>` | POST | Export document |
| `/health` | GET | Health check |

## 🤝 **Contributing**

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## 📄 **License**

This project is licensed under the MIT License.

## 🆘 **Support**

For issues and questions:
- Check troubleshooting section
- Review console logs
- Verify environment configuration

## 🔄 **Version History**

- **v1.0.0** - Initial release with core functionality
- **v1.1.0** - Added file attachment support
- **v1.2.0** - Enhanced export features
- **v1.3.0** - Security improvements

---

**Built with ❤️ for enterprise-grade user story generation**