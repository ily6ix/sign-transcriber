#!/usr/bin/env python
"""
Quick verification script to run on Railway
Tests that admin can access database in real-time
Run with: railway run python verify_railway_admin_access.py
"""

import os
from app import app, db
from models import User, Transcript, SignDataset, AuditLog
from sqlalchemy import text, func

def verify_admin_access():
    with app.app_context():
        # Get database type
        db_url = os.getenv('DATABASE_URL', 'SQLite')
        is_railway = 'mysql' in str(db_url).lower()
        
        print("\n🔍 RAILWAY ADMIN ACCESS VERIFICATION\n")
        print(f"Database: {'🔶 Railway MySQL' if is_railway else '🔵 SQLite'}")
        
        try:
            # Test connection
            db.session.execute(text('SELECT 1'))
            db.session.commit()
            print("Connection: ✅ Connected\n")
            
            # Get current data
            users_count = User.query.count()
            admins_count = User.query.filter_by(role='admin').count()
            transcripts_count = Transcript.query.count()
            datasets_count = SignDataset.query.count()
            logs_count = AuditLog.query.count()
            
            print("📊 Current Database State:")
            print(f"  Users: {users_count} ({admins_count} admins)")
            print(f"  Transcripts: {transcripts_count}")
            print(f"  Datasets: {datasets_count}")
            print(f"  Audit Logs: {logs_count}\n")
            
            # Test real-time queries
            print("🔄 Testing Real-Time Queries:")
            
            # Query 1: Recent users
            recent = User.query.order_by(User.created_at.desc()).limit(3).all()
            print(f"  ✅ Recent users: {len(recent)} retrieved")
            
            # Query 2: Transcript stats
            from_db = db.session.query(
                Transcript.status,
                func.count(Transcript.id)
            ).group_by(Transcript.status).all()
            print(f"  ✅ Status distribution: {len(from_db)} statuses")
            
            # Query 3: Dataset types
            by_type = db.session.query(
                SignDataset.gesture_type,
                func.count(SignDataset.id)
            ).group_by(SignDataset.gesture_type).all()
            print(f"  ✅ Dataset types: {len(by_type)} types")
            
            # Query 4: Pagination
            page = User.query.paginate(page=1, per_page=10)
            print(f"  ✅ Pagination: {page.total} users, {page.pages} pages\n")
            
            print("✅ VERIFICATION PASSED")
            print("Admin can access Railway database in real-time!\n")
            return True
            
        except Exception as e:
            print(f"❌ VERIFICATION FAILED: {e}\n")
            print("Troubleshooting:")
            print(f"  1. Check DATABASE_URL: {os.getenv('DATABASE_URL', 'Not set')}")
            print("  2. Verify Railway MySQL is running")
            print("  3. Check app logs: railway logs")
            return False

if __name__ == '__main__':
    import sys
    success = verify_admin_access()
    sys.exit(0 if success else 1)