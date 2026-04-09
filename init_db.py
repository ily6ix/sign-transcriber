#!/usr/bin/env python
"""
Database Initialization Script
Initializes database tables, creates admin user, and seeds sample data.
Supports both SQLite (local) and MySQL (Railway) databases.
"""

import os
import sys
from app import app, db
from models import User, SignDataset
from sqlalchemy import text

def test_database_connection():
    """Test database connection"""
    with app.app_context():
        try:
            print("🔗 Testing database connection...")
            db.session.execute(text('SELECT 1'))
            db.session.commit()
            print("✅ Database connection successful")
            return True
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            print("\n💡 Troubleshooting:")
            print("   - Check DATABASE_URL environment variable")
            print("   - For Railway MySQL: mysql+pymysql://user:pass@host:port/db")
            print("   - For local SQLite: Leave DATABASE_URL unset")
            print("   - Verify .env file is loaded (run: cat .env)")
            return False

def init_database():
    """Initialize database with tables"""
    with app.app_context():
        try:
            print("🗄️  Creating database tables...")
            db.create_all()
            print("✅ Database tables created successfully")
            return True
        except Exception as e:
            print(f"❌ Error creating tables: {e}")
            return False

def create_admin_user():
    """Create default admin user if it doesn't exist"""
    with app.app_context():
        try:
            if User.query.filter_by(username='admin').first():
                print("⚠️  Admin user already exists, skipping creation...")
                return True
            
            admin = User(
                username='admin',
                email='admin@sign.com',
                full_name='Administrator',
                role='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            
            print("✅ Admin user created")
            print("   Username: admin")
            print("   Password: admin123")
            print("   ⚠️  IMPORTANT: Change this password immediately in production!")
            return True
        except Exception as e:
            print(f"❌ Error creating admin user: {e}")
            db.session.rollback()
            return False

def seed_sign_data():
    """Seed sample sign language data"""
    with app.app_context():
        try:
            sample_signs = [
                ('A', 'Letter A in ASL', 'letter'),
                ('B', 'Letter B in ASL', 'letter'),
                ('C', 'Letter C in ASL', 'letter'),
                ('HELLO', 'Greeting sign', 'phrase'),
                ('THANK YOU', 'Expression of gratitude', 'phrase'),
                ('YES', 'Affirmative response', 'phrase'),
                ('NO', 'Negative response', 'phrase'),
                ('PLEASE', 'Polite request', 'phrase'),
                ('I LOVE YOU', 'Expression of affection', 'phrase'),
                ('GOOD MORNING', 'Time-specific greeting', 'phrase'),
            ]
            
            count = 0
            for sign_name, description, gesture_type in sample_signs:
                if not SignDataset.query.filter_by(sign_name=sign_name).first():
                    sign = SignDataset(
                        sign_name=sign_name,
                        description=description,
                        gesture_type=gesture_type
                    )
                    db.session.add(sign)
                    count += 1
            
            if count > 0:
                db.session.commit()
                print(f"✅ Seeded {count} new sign entries")
            else:
                print("⚠️  Sign data already seeded, skipping...")
            return True
        except Exception as e:
            print(f"❌ Error seeding sign data: {e}")
            db.session.rollback()
            return False

def print_database_info():
    """Print current database configuration"""
    from config import SQLALCHEMY_DATABASE_URI
    
    print("\n📊 Database Configuration:")
    print("-" * 50)
    
    if 'mysql' in SQLALCHEMY_DATABASE_URI.lower():
        print("Type: MySQL (Remote)")
        # Mask password in output
        safe_uri = SQLALCHEMY_DATABASE_URI.replace(
            SQLALCHEMY_DATABASE_URI.split('@')[0],
            SQLALCHEMY_DATABASE_URI.split('@')[0].split(':')[0] + ':***'
        )
        print(f"URI: {safe_uri}")
    elif 'sqlite' in SQLALCHEMY_DATABASE_URI.lower():
        print("Type: SQLite (Local)")
        print(f"URI: {SQLALCHEMY_DATABASE_URI}")
    else:
        print(f"URI: {SQLALCHEMY_DATABASE_URI}")
    
    print("-" * 50 + "\n")

def main():
    """Run initialization sequence"""
    print("\n" + "=" * 60)
    print("Sign Language Transcriber - Database Initialization")
    print("=" * 60 + "\n")
    
    # Print database info
    print_database_info()
    
    # Test connection
    if not test_database_connection():
        print("\n❌ Cannot proceed without database connection.")
        sys.exit(1)
    
    print()
    
    # Initialize database
    if not init_database():
        print("\n❌ Cannot proceed without creating tables.")
        sys.exit(1)
    
    print()
    
    # Create admin user
    if not create_admin_user():
        print("\n⚠️  Failed to create admin user, but tables are created.")
    
    print()
    
    # Seed data
    if not seed_sign_data():
        print("\n⚠️  Failed to seed sign data, but tables are created.")
    
    print("\n" + "=" * 60)
    print("✅ Initialization Complete!")
    print("=" * 60 + "\n")
    print("🚀 Next Steps:")
    print("   1. Start the application: python app.py")
    print("   2. Open browser: http://localhost:5000")
    print("   3. Login with admin credentials (see above)")
    print("\n💡 Deployment:")
    print("   - For Railway: Set DATABASE_URL in Railway dashboard")
    print("   - Run this script on Railway after deployment")
    print("\n")

if __name__ == '__main__':
    main()
