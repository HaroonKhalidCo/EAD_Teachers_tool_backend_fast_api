#!/usr/bin/env python3
"""
Setup script to create .env file for the EAD Teachers Tool Backend
"""

import os

def create_env_file():
    """Create .env file with required environment variables"""
    
    env_content = """# Google Gemini API Key
GOOGLE_API_KEY=your_google_api_key_here

# Server Configuration
HOST=0.0.0.0
PORT=8001

# Environment
ENVIRONMENT=development
"""
    
    # Check if .env already exists
    if os.path.exists('.env'):
        print("⚠️  .env file already exists!")
        response = input("Do you want to overwrite it? (y/N): ")
        if response.lower() != 'y':
            print("❌ Setup cancelled. .env file not modified.")
            return
    
    # Create .env file
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ .env file created successfully!")
    print("\n📝 Next steps:")
    print("1. Edit the .env file and replace 'your_google_api_key_here' with your actual Google API key")
    print("2. Get your API key from: https://makersuite.google.com/app/apikey")
    print("3. Run the application with: uvicorn app.main:app --reload --port 8001")

if __name__ == "__main__":
    print("🚀 EAD Teachers Tool Backend - Environment Setup")
    print("=" * 50)
    create_env_file() 