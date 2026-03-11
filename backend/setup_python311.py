"""
Automated Python 3.11 setup script for VidyaMitra backend
"""
import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔧 {description}")
    print(f"Running: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(f"Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        print(f"Error: {e.stderr}")
        return False

def check_python311():
    """Check if Python 3.11 is available"""
    print("🔍 Checking Python 3.11 availability...")
    
    try:
        result = subprocess.run("py -3.11 --version", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Python 3.11 found: {result.stdout.strip()}")
            return True
        else:
            print("❌ Python 3.11 not found")
            return False
    except Exception as e:
        print(f"❌ Error checking Python 3.11: {str(e)}")
        return False

def create_virtual_env():
    """Create Python 3.11 virtual environment"""
    print("📦 Creating Python 3.11 virtual environment...")
    
    venv_path = Path("venv311")
    if venv_path.exists():
        print("⚠️  Virtual environment already exists. Removing it...")
        run_command("rmdir /s /q venv311", "Removing existing virtual environment")
    
    success = run_command("py -3.11 -m venv venv311", "Creating virtual environment")
    return success

def activate_and_install():
    """Activate virtual environment and install dependencies"""
    print("🚀 Activating virtual environment and installing dependencies...")
    
    # Commands to run in the activated environment
    commands = [
        ("venv311\\Scripts\\activate && python --version", "Verifying Python version in venv"),
        ("venv311\\Scripts\\activate && python -m pip install --upgrade pip", "Upgrading pip"),
        ("venv311\\Scripts\\activate && python -m pip install wheel setuptools", "Installing build tools"),
        ("venv311\\Scripts\\activate && python -m pip install fastapi==0.110.0", "Installing FastAPI"),
        ("venv311\\Scripts\\activate && python -m pip install uvicorn==0.29.0", "Installing Uvicorn"),
        ("venv311\\Scripts\\activate && python -m pip install sqlalchemy==2.0.29", "Installing SQLAlchemy"),
        ("venv311\\Scripts\\activate && python -m pip install psycopg2-binary==2.9.9", "Installing PostgreSQL driver"),
        ("venv311\\Scripts\\activate && python -m pip install python-dotenv==1.0.1", "Installing python-dotenv"),
        ("venv311\\Scripts\\activate && python -m pip install passlib[bcrypt]==1.7.4", "Installing Passlib"),
        ("venv311\\Scripts\\activate && python -m pip install python-jose==3.3.0", "Installing python-jose"),
        ("venv311\\Scripts\\activate && python -m pip install google-generativeai", "Installing Google Generative AI"),
        ("venv311\\Scripts\\activate && python -m pip install pydantic==2.6.4", "Installing Pydantic"),
        ("venv311\\Scripts\\activate && python -m pip install pydantic-settings==2.2.1", "Installing Pydantic Settings"),
        ("venv311\\Scripts\\activate && python -m pip install python-multipart==0.0.9", "Installing python-multipart"),
        ("venv311\\Scripts\\activate && python -m pip install aiosqlite==0.20.0", "Installing aiosqlite"),
        ("venv311\\Scripts\\activate && python -m pip install python-docx==1.1.0", "Installing python-docx"),
        ("venv311\\Scripts\\activate && python -m pip install PyPDF2==3.0.1", "Installing PyPDF2"),
        ("venv311\\Scripts\\activate && python -m pip install alembic==1.13.1", "Installing Alembic"),
        ("venv311\\Scripts\\activate && python -m pip freeze > requirements.txt", "Generating requirements.txt")
    ]
    
    success = True
    for command, description in commands:
        if not run_command(command, description):
            success = False
            break
    
    return success

def test_setup():
    """Test the setup by running basic imports"""
    print("🧪 Testing setup...")
    
    test_commands = [
        ("venv311\\Scripts\\activate && python -c \"import fastapi, sqlalchemy, google.generativeai; print('All imports successful!')\"", "Testing imports"),
        ("venv311\\Scripts\\activate && python -c \"from database import engine; print('Database connection successful!')\"", "Testing database connection")
    ]
    
    success = True
    for command, description in test_commands:
        if not run_command(command, description):
            success = False
            break
    
    return success

def main():
    """Main setup function"""
    print("🚀 VidyaMitra Backend - Python 3.11 Setup")
    print("=" * 50)
    
    # Step 1: Check Python 3.11
    if not check_python311():
        print("\n❌ Python 3.11 not found. Please install it first:")
        print("   winget install Python.Python.3.11")
        print("   Or download from: https://www.python.org/downloads/release/python-3119/")
        return False
    
    # Step 2: Create virtual environment
    if not create_virtual_env():
        print("\n❌ Failed to create virtual environment")
        return False
    
    # Step 3: Install dependencies
    if not activate_and_install():
        print("\n❌ Failed to install dependencies")
        return False
    
    # Step 4: Test setup
    if not test_setup():
        print("\n❌ Setup test failed")
        return False
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Activate virtual environment: venv311\\Scripts\\activate")
    print("2. Start the server: uvicorn main:app --reload")
    print("3. Open browser: http://localhost:8000/docs")
    
    return True

if __name__ == "__main__":
    main()
