#!/usr/bin/env python
"""
Test script to verify role selection in registration
"""

from app import app, db
from models import User

def test_role_registration():
    """Test creating users with different roles"""
    with app.app_context():
        # Test creating a regular user
        test_user = User(
            username='testuser',
            email='test@example.com',
            full_name='Test User',
            role='user'
        )
        test_user.set_password('password123')
        db.session.add(test_user)

        # Test creating an admin user (should work since root exists)
        test_admin = User(
            username='testadmin',
            email='admin@example.com',
            full_name='Test Admin',
            role='admin'
        )
        test_admin.set_password('password123')
        db.session.add(test_admin)

        db.session.commit()

        print("✅ Test users created successfully")
        print("   - testuser (role: user)")
        print("   - testadmin (role: admin)")

        # Verify they exist
        user = User.query.filter_by(username='testuser').first()
        admin = User.query.filter_by(username='testadmin').first()

        print(f"   - User exists: {user is not None}, role: {user.role if user else 'N/A'}")
        print(f"   - Admin exists: {admin is not None}, role: {admin.role if admin else 'N/A'}")

if __name__ == '__main__':
    test_role_registration()