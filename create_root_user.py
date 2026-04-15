#!/usr/bin/env python
"""
Create Root Admin User Script
Creates the root admin user in the database.
Run this on Railway after deployment.
"""

from app import app, db
from models import User

def create_root_user():
    """Create root admin user if it doesn't exist"""
    with app.app_context():
        try:
            if User.query.filter_by(username='root').first():
                print("⚠️  Root user already exists, skipping creation...")
                return True

            root = User(
                username='root',
                email='root@sign.com',
                full_name='Root Administrator',
                role='admin'
            )
            root.set_password('root123')
            db.session.add(root)
            db.session.commit()

            print("✅ Root admin user created successfully!")
            print("   Username: root")
            print("   Password: root123")
            print("   Email: root@sign.com")
            print("   ⚠️  IMPORTANT: Change this password immediately in production!")
            return True
        except Exception as e:
            print(f"❌ Error creating root user: {e}")
            db.session.rollback()
            return False

if __name__ == '__main__':
    create_root_user()