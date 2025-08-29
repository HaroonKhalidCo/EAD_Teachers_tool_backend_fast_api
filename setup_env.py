#!/usr/bin/env python3
"""
Setup script to create .env file with required environment variables
"""

import os

def create_env_file():
    """Create .env file with template values"""
    
    env_content = """# API Keys
GOOGLE_API_KEY=your_google_api_key_here

# Server Configuration
HOST=0.0.0.0
PORT=8000
ENVIRONMENT=development

# Security Configuration
SECRET_KEY=your_secret_key_here_change_in_production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS Configuration (for production)
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60

# Database (if needed later)
DATABASE_URL=sqlite:///./app.db

# Logging
LOG_LEVEL=INFO
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ .env file created successfully!")
    print("⚠️  Please update the values with your actual configuration")
    print("🔑 Make sure to set a strong SECRET_KEY for production")

if __name__ == "__main__":
    create_env_file() 