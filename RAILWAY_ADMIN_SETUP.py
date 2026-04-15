#!/usr/bin/env python
"""
Railway MySQL Configuration and Setup Guide
This script helps configure and test the Railway MySQL connection
"""

import os
import sys

def print_railway_setup_guide():
    """Print detailed Railway setup instructions"""
    
    guide = """
╔════════════════════════════════════════════════════════════════════════════╗
║               RAILWAY MYSQL SETUP FOR ADMIN DATABASE ACCESS                ║
╚════════════════════════════════════════════════════════════════════════════╝

STEP 1: CREATE RAILWAY MYSQL DATABASE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1. Go to railway.app dashboard
  2. Click "New Project"
  3. Select "MySQL"
  4. Wait for deployment to complete
  5. You'll see your MySQL service in the dashboard

STEP 2: GET DATABASE CONNECTION STRING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1. Click on your MySQL service in Railway
  2. Go to the "Connect" tab
  3. Look for "Database URL" or "Connection String"
  4. Copy the URL (it should look like below):
     
     mysql+pymysql://username:password@host:port/database
     
  5. IMPORTANT: Replace 'mysql://' with 'mysql+pymysql://' if needed

STEP 3: SET RAILWAY ENVIRONMENT VARIABLES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  In your Railway project settings, add these environment variables:

  DATABASE_URL = mysql+pymysql://user:password@host:port/database
  FLASK_ENV = production
  SECRET_KEY = [generate with: python -c "import secrets; print(secrets.token_hex(32))"]

STEP 4: INITIALIZE DATABASE ON RAILWAY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Option A: Using Railway CLI
  ──────────────────────────
    railway run python init_db.py
    railway run python create_root_user.py

  Option B: Using Railway Dashboard Shell
  ────────────────────────────────────────
    1. Go to Railway dashboard
    2. Click your app service
    3. Go to "Shell" tab
    4. Run: python init_db.py
    5. Run: python create_root_user.py

STEP 5: VERIFY ADMIN DATABASE ACCESS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1. Deploy your app
  2. Visit: https://your-app.railway.app/login
  3. Login with admin credentials
  4. Go to: /admin/dashboard
  5. Verify you can see:
     - Total Users
     - Total Transcripts
     - Total Datasets
     - Recent Activity
  6. Click through admin pages to verify real-time data access:
     - /admin/users (all users from Railway MySQL)
     - /admin/transcripts (all transcripts from Railway MySQL)
     - /admin/datasets (all sign datasets from Railway MySQL)
     - /admin/audit-logs (all admin activities)

ADMIN REAL-TIME DATA ACCESS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  
  ✅ Admin Dashboard (/admin/dashboard)
     Real-time stats: Users, Transcripts, Active Users, Flagged Transcripts
  
  ✅ User Management (/admin/users)
     Query: User.query.order_by(User.created_at.desc()).paginate()
     Displays: All users from Railway MySQL with create/edit/delete
  
  ✅ Transcript Management (/admin/transcripts)
     Query: Transcript.query.filter_by(status).paginate()
     Displays: All transcripts with flagging and deletion options
  
  ✅ Dataset Management (/admin/datasets)
     Query: SignDataset.query.filter_by(gesture_type).paginate()
     Displays: All sign language datasets with filtering
  
  ✅ Audit Logs (/admin/audit-logs)
     Query: AuditLog.query.order_by(timestamp.desc()).paginate()
     Displays: All admin activities with filtering by action
  
  ✅ Analytics (/admin/analytics)
     Queries: Complex aggregations and statistics
     Displays: Charts and insights on user activity

CONNECTION POOL CONFIGURATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  
  The app uses optimized connection pooling for Railway MySQL:
  
  • Pool Size: 10 (maintains 10 ready connections)
  • Max Overflow: 20 (allows up to 20 extra connections if needed)
  • Pool Pre-Ping: Enabled (validates connections before use)
  • Pool Recycle: 3600s (automatically recycles stale connections)
  
  This ensures:
  ✓ Fast startup
  ✓ Concurrent requests handled efficiently
  ✓ Automatic reconnection after Railway connection issues
  ✓ Reliable real-time data access

TROUBLESHOOTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  
  Issue: "No data shows in admin pages"
  Solution:
    1. Verify DATABASE_URL environment variable is set
    2. Check connection: railway run python test_admin_railway_access.py
    3. Ensure MySQL service is running in Railway
    4. Check database initialization: railway run python init_db.py
  
  Issue: "Slow data loading from Railway"
  Solution:
    1. Increase connection pool size in config.py
    2. Add indexes to frequently queried columns (already done)
    3. Use pagination in admin pages (already implemented)
    4. Monitor Railway database load vs. app usage
  
  Issue: "Connection drops after idle time"
  Solution:
    Already handled! pool_pre_ping validates connections before use
    and pool_recycle refreshes old connections automatically
  
  Issue: "Admin pages show error"
  Solution:
    1. Check Railway app logs: railway logs
    2. Test local database first: python test_admin_railway_access.py
    3. Verify admin user exists: railway run python -c "from models import User; from app import app; app.app_context().push(); print(User.query.count())"

LOCAL TESTING BEFORE DEPLOYING TO RAILWAY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Test locally with SQLite first:
  ────────────────────────────────
    1. python init_db.py
    2. python create_root_user.py
    3. python app.py
    4. Visit http://localhost:5000
    5. Verify admin access works before Railway deployment
  
  Test with Railway MySQL locally:
  ──────────────────────────────────
    1. Set local environment: export DATABASE_URL="mysql+pymysql://..."
    2. python init_db.py
    3. python create_root_user.py
    4. python test_admin_railway_access.py (verify connection)
    5. python app.py
    6. Test admin pages locally

MONITORING ADMIN DATABASE ACCESS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  View audit logs on Railway:
  ─────────────────────────
    railway run python -c "
    from app import app
    from models import AuditLog
    app.app_context().push()
    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).limit(10)
    for log in logs:
        print(f'{log.timestamp}: {log.admin.username} - {log.action} on {log.target_type}')
    "

  Check admin users:
  ─────────────────
    railway run python -c "
    from app import app
    from models import User
    app.app_context().push()
    admins = User.query.filter_by(role='admin').all()
    for admin in admins:
        print(f'{admin.username}: {admin.full_name}')
    "

╚════════════════════════════════════════════════════════════════════════════╝
"""
    
    print(guide)

if __name__ == '__main__':
    print_railway_setup_guide()
