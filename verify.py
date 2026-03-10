#!/usr/bin/env python
"""
SignaTranslate - Project Verification Checklist
Verify all components are in place and functional
"""

import os
import sys
from pathlib import Path

class ProjectVerifier:
    def __init__(self):
        self.checks = []
        self.passed = 0
        self.failed = 0
        
    def check_file(self, filepath, description):
        """Check if file exists"""
        exists = Path(filepath).exists()
        status = "✅" if exists else "❌"
        self.checks.append(f"{status} {description}")
        if exists:
            self.passed += 1
        else:
            self.failed += 1
        return exists
    
    def check_directory(self, dirpath, description):
        """Check if directory exists"""
        exists = Path(dirpath).exists()
        status = "✅" if exists else "❌"
        self.checks.append(f"{status} {description}")
        if exists:
            self.passed += 1
        else:
            self.failed += 1
        return exists
    
    def check_imports(self):
        """Check if key modules can be imported"""
        imports = [
            ("flask", "Flask framework"),
            ("flask_sqlalchemy", "SQLAlchemy ORM"),
            ("flask_login", "Flask-Login auth"),
            ("flask_wtf", "Flask-WTF forms"),
        ]
        
        for module, description in imports:
            try:
                __import__(module)
                self.checks.append(f"✅ {description} - Import OK")
                self.passed += 1
            except ImportError:
                self.checks.append(f"❌ {description} - Import Failed")
                self.failed += 1
    
    def verify_project(self):
        """Run all verification checks"""
        print("=" * 60)
        print("SignaTranslate - Project Verification")
        print("=" * 60)
        print()
        
        # Python files
        print("🐍 Python Application Files:")
        self.check_file("app.py", "Main Flask application")
        self.check_file("config.py", "Configuration module")
        self.check_file("models.py", "Database models")
        self.check_file("forms.py", "Form validation")
        self.check_file("sign_detector.py", "Sign detection module")
        self.check_file("init_db.py", "Database initialization")
        print()
        
        # Directories
        print("📁 Directory Structure:")
        self.check_directory("templates", "Templates directory")
        self.check_directory("static", "Static files directory")
        self.check_directory("templates/auth", "Auth templates")
        self.check_directory("templates/user", "User templates")
        self.check_directory("templates/admin", "Admin templates")
        self.check_directory("templates/errors", "Error templates")
        self.check_directory("static/css", "CSS directory")
        self.check_directory("static/js", "JavaScript directory")
        print()
        
        # Template files
        print("🌐 HTML Templates:")
        templates = [
            "templates/index.html",
            "templates/base.html",
            "templates/auth/login.html",
            "templates/auth/register.html",
            "templates/user/dashboard.html",
            "templates/user/transcribe.html",
            "templates/user/view_transcript.html",
            "templates/admin/dashboard.html",
            "templates/admin/manage_users.html",
            "templates/admin/create_user.html",
            "templates/admin/edit_user.html",
            "templates/admin/manage_transcripts.html",
            "templates/admin/analytics.html",
            "templates/errors/404.html",
            "templates/errors/403.html",
            "templates/errors/500.html",
        ]
        for template in templates:
            self.check_file(template, f"Template: {Path(template).name}")
        print()
        
        # Static files
        print("🎨 Static Files:")
        self.check_file("static/css/style.css", "Main CSS stylesheet")
        self.check_file("static/js/script.js", "Main JavaScript file")
        print()
        
        # Configuration files
        print("⚙️ Configuration Files:")
        self.check_file("requirements.txt", "Python dependencies")
        self.check_file(".env.example", "Environment template")
        self.check_file(".gitignore", "Git exclusions")
        self.check_file("startup.sh", "Startup script")
        print()
        
        # Documentation
        print("📚 Documentation:")
        self.check_file("README.md", "Project README")
        self.check_file("README_FULL.md", "Full documentation")
        self.check_file("SETUP_GUIDE.md", "Setup guide")
        self.check_file("PROJECT_SUMMARY.md", "Project summary")
        print()
        
        # Module imports
        print("🔌 Python Module Imports:")
        try:
            from app import app
            self.checks.append("✅ Flask application - OK")
            self.passed += 1
        except Exception as e:
            self.checks.append(f"❌ Flask application - {str(e)[:30]}")
            self.failed += 1
        
        try:
            from models import db, User, Transcript
            self.checks.append("✅ Database models - OK")
            self.passed += 1
        except Exception as e:
            self.checks.append(f"❌ Database models - {str(e)[:30]}")
            self.failed += 1
        
        try:
            from forms import RegistrationForm, LoginForm
            self.checks.append("✅ Form validation - OK")
            self.passed += 1
        except Exception as e:
            self.checks.append(f"❌ Form validation - {str(e)[:30]}")
            self.failed += 1
        
        try:
            from sign_detector import initialize_detector
            self.checks.append("✅ Sign detector module - OK")
            self.passed += 1
        except Exception as e:
            self.checks.append(f"❌ Sign detector module - {str(e)[:30]}")
            self.failed += 1
        
        print()
        
        # Print results
        print("=" * 60)
        print("✅ VERIFICATION RESULTS:")
        print("=" * 60)
        print()
        
        for check in self.checks:
            print(check)
        
        print()
        print("=" * 60)
        print(f"Passed: {self.passed} | Failed: {self.failed}")
        print("=" * 60)
        print()
        
        if self.failed == 0:
            print("🎉 ALL CHECKS PASSED! Project is ready.")
            print()
            print("🚀 Next steps:")
            print("   1. python init_db.py     # Initialize database")
            print("   2. python app.py         # Start development server")
            print("   3. Open http://localhost:5000")
            print()
            return 0
        else:
            print(f"⚠️  {self.failed} checks failed. Review above for details.")
            print()
            return 1

if __name__ == "__main__":
    verifier = ProjectVerifier()
    exit_code = verifier.verify_project()
    sys.exit(exit_code)
