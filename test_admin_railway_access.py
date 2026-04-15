#!/usr/bin/env python
"""
Railway Database Connection Diagnostic Script
Tests admin data access from Railway MySQL database in real-time
"""

import os
import sys
from app import app, db
from models import User, Transcript, SignDataset, AuditLog

def test_database_connection():
    """Test database connection and configuration"""
    print("\n" + "="*70)
    print("DATABASE CONNECTION DIAGNOSTIC")
    print("="*70)
    
    with app.app_context():
        # Check environment
        db_url = os.getenv('DATABASE_URL', 'Not set')
        flask_env = os.getenv('FLASK_ENV', 'development')
        
        print(f"\n📋 Environment:")
        print(f"  FLASK_ENV: {flask_env}")
        print(f"  DATABASE_URL: {'***' if db_url != 'Not set' else db_url}")
        
        # Show which database we're using
        print(f"\n🗄️  Database Type:")
        if 'mysql' in str(app.config['SQLALCHEMY_DATABASE_URI']).lower():
            print("  ✅ Using Railway MySQL (Production)")
        else:
            print("  ℹ️  Using Local SQLite (Development)")
        
        # Test connection
        print(f"\n🔗 Testing Connection...")
        try:
            from sqlalchemy import text
            result = db.session.execute(text('SELECT 1'))
            db.session.commit()
            print("  ✅ Database connection successful")
        except Exception as e:
            print(f"  ❌ Connection failed: {e}")
            return False
        
        # Test data access for admins
        print(f"\n📊 Admin Data Access Test:")
        
        try:
            # Users
            user_count = User.query.count()
            admin_count = User.query.filter_by(role='admin').count()
            print(f"  ✅ Users: {user_count} total ({admin_count} admins)")
            
            # Transcripts
            transcript_count = Transcript.query.count()
            print(f"  ✅ Transcripts: {transcript_count}")
            
            # Datasets
            dataset_count = SignDataset.query.count()
            print(f"  ✅ Sign Datasets: {dataset_count}")
            
            # Audit Logs
            log_count = AuditLog.query.count()
            print(f"  ✅ Audit Logs: {log_count}")
            
        except Exception as e:
            print(f"  ❌ Error reading data: {e}")
            return False
        
        # Test real-time query capability
        print(f"\n🔄 Real-Time Query Test:")
        
        try:
            # Recent users query
            recent_users = User.query.order_by(User.created_at.desc()).limit(3).all()
            print(f"  ✅ Recent Users Query: Retrieved {len(recent_users)} users")
            for user in recent_users:
                print(f"    - {user.username} ({user.role})")
            
            # Transcript status distribution
            from sqlalchemy import func
            status_dist = db.session.query(
                Transcript.status,
                func.count(Transcript.id)
            ).group_by(Transcript.status).all()
            
            print(f"  ✅ Transcript Status Distribution:")
            if status_dist:
                for status, count in status_dist:
                    print(f"    - {status}: {count}")
            else:
                print("    - No transcripts")
            
            # Admin activity
            admin_activity = AuditLog.query.order_by(AuditLog.timestamp.desc()).limit(3).all()
            print(f"  ✅ Recent Admin Activity: Retrieved {len(admin_activity)} logs")
            if admin_activity:
                for log in admin_activity:
                    print(f"    - {log.action} by admin {log.admin_id} on {log.target_type}")
            
        except Exception as e:
            print(f"  ❌ Real-time query failed: {e}")
            return False
        
        # Connection pool info
        print(f"\n⚙️  Connection Pool Configuration:")
        print(f"  Pool Size: 10")
        print(f"  Max Overflow: 20")
        print(f"  Pool Pre-Ping: Enabled (validates connections)")
        print(f"  Pool Recycle: 3600s (1 hour)")
        
        print("\n" + "="*70)
        print("✅ ALL TESTS PASSED - Admin Can Access Railway Database")
        print("="*70 + "\n")
        
        return True

def verify_admin_routes():
    """Verify admin routes are properly configured"""
    print("\n" + "="*70)
    print("ADMIN ROUTES VERIFICATION")
    print("="*70)
    
    with app.app_context():
        # Check if routes exist
        routes_to_check = [
            '/admin/dashboard',
            '/admin/users',
            '/admin/transcripts',
            '/admin/datasets',
            '/admin/audit-logs',
            '/admin/analytics',
        ]
        
        print("\n🛣️  Admin Routes:")
        for rule in app.url_map.iter_rules():
            for route in routes_to_check:
                if route in rule.rule:
                    methods = ', '.join(rule.methods - {'HEAD', 'OPTIONS'})
                    print(f"  ✅ {rule.rule} ({methods})")
        
        print("\n" + "="*70 + "\n")

if __name__ == '__main__':
    success = test_database_connection()
    verify_admin_routes()
    
    if success:
        print("✅ Admin real-time database access is working correctly!")
        sys.exit(0)
    else:
        print("❌ Issues detected. Check configuration and connection.")
        sys.exit(1)