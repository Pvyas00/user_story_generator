# Production Configuration Guide

## Environment Setup

1. **Set Environment Variables:**
   ```bash
   export GROQ_API_KEY="your_actual_groq_api_key"
   export SECRET_KEY="your_secure_random_secret_key"
   export FLASK_ENV="production"
   export PORT="5000"
   ```

2. **Generate Secure Secret Key:**
   ```python
   import secrets
   print(secrets.token_hex(32))
   ```

## Security Checklist

- [ ] API keys are set via environment variables
- [ ] Secret key is randomly generated and secure
- [ ] Debug mode is disabled in production
- [ ] .env file is not committed to version control
- [ ] Proper logging is configured
- [ ] HTTPS is enabled
- [ ] Input validation is in place

## Deployment Commands

### Using Gunicorn (Recommended)
```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 app:app
```

### Using Flask Development Server (Not for Production)
```bash
python app.py
```

## Health Check
Visit `/health` endpoint to verify configuration:
- Should return `{"status": "healthy", "groq_configured": true}`

## Monitoring
- Check application logs for errors
- Monitor API usage and rate limits
- Set up alerts for failed requests