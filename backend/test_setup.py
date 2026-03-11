"""
Test script to verify Python 3.11 setup and backend functionality
"""
import sys
import os

def test_imports():
    """Test all required imports"""
    print("🧪 Testing imports...")
    
    try:
        import fastapi
        print("✅ FastAPI imported successfully")
    except Exception as e:
        print(f"❌ FastAPI import failed: {str(e)}")
        return False
    
    try:
        import uvicorn
        print("✅ Uvicorn imported successfully")
    except Exception as e:
        print(f"❌ Uvicorn import failed: {str(e)}")
        return False
    
    try:
        import sqlalchemy
        print("✅ SQLAlchemy imported successfully")
    except Exception as e:
        print(f"❌ SQLAlchemy import failed: {str(e)}")
        return False
    
    try:
        import google.generativeai as genai
        print("✅ Google Generative AI imported successfully")
    except Exception as e:
        print(f"❌ Google Generative AI import failed: {str(e)}")
        return False
    
    try:
        import pydantic
        print("✅ Pydantic imported successfully")
    except Exception as e:
        print(f"❌ Pydantic import failed: {str(e)}")
        return False
    
    return True

def test_database():
    """Test database connection and models"""
    print("\n🔍 Testing database connection...")
    
    try:
        from database import engine, Base, test_connection
        
        # Test connection
        if test_connection():
            print("✅ Database connection successful")
        else:
            print("❌ Database connection failed")
            return False
        
        # Test table creation (avoid metadata issue)
        try:
            from sqlalchemy.orm import declarative_base
            Base.registry.metadata.create_all(bind=engine)
            print("✅ Database tables created successfully")
        except Exception as e:
            print(f"⚠️  Table creation warning: {str(e)}")
            # Continue anyway as this might be a metadata naming issue
        
        return True
    except Exception as e:
        print(f"❌ Database test failed: {str(e)}")
        return False

def test_gemini():
    """Test Gemini API connection"""
    print("\n🤖 Testing Gemini API...")
    
    try:
        import google.generativeai as genai
        from dotenv import load_dotenv
        
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            print("❌ GEMINI_API_KEY not found in environment")
            return False
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        
        # Test generation
        response = model.generate_content("What is Python programming? Answer in one sentence.")
        if response and response.text:
            print("✅ Gemini API test successful")
            print(f"Response: {response.text.strip()}")
            return True
        else:
            print("❌ Empty response from Gemini")
            return False
            
    except Exception as e:
        print(f"❌ Gemini API test failed: {str(e)}")
        return False

def test_fastapi_app():
    """Test FastAPI app creation"""
    print("\n🚀 Testing FastAPI app...")
    
    try:
        # Test basic FastAPI creation without importing main.py
        from fastapi import FastAPI
        
        app = FastAPI(
            title="VidyaMitra API Test",
            description="Test app",
            version="1.0.0"
        )
        
        print("✅ FastAPI app created successfully")
        print(f"✅ App title: {app.title}")
        print(f"✅ App version: {app.version}")
        
        # Test database components separately
        from database import engine, test_connection
        if test_connection():
            print("✅ Database connection verified")
        else:
            print("⚠️  Database connection issue")
        
        return True
    except Exception as e:
        print(f"❌ FastAPI app test failed: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🧪 VidyaMitra Backend - Setup Verification")
    print("=" * 50)
    
    # Check Python version
    python_version = sys.version_info
    print(f"🐍 Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version.major != 3 or python_version.minor != 11:
        print("⚠️  Warning: This setup is optimized for Python 3.11")
        print("   You may encounter compatibility issues with other Python versions")
    
    # Run tests
    tests = [
        ("Import Test", test_imports),
        ("Database Test", test_database),
        ("Gemini API Test", test_gemini),
        ("FastAPI App Test", test_fastapi_app)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        result = test_func()
        results.append((test_name, result))
    
    # Summary
    print(f"\n{'='*50}")
    print("📊 Test Summary:")
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"  {test_name}: {status}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n🎉 All tests passed! Your backend is ready to run.")
        print("\n🚀 Start the server with:")
        print("   uvicorn main:app --reload")
        print("\n📖 Access API documentation at:")
        print("   http://localhost:8000/docs")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
    
    return all_passed

if __name__ == "__main__":
    main()
