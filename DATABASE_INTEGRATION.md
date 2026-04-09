# Railway MySQL Integration Guide

This guide explains how to connect your Flask Sign Transcriber application to a Railway MySQL database while maintaining local SQLite development.

## Table of Contents
1. [Quick Start](#quick-start)
2. [Local Development Setup](#local-development-setup)
3. [Railway MySQL Setup](#railway-mysql-setup)
4. [Environment Variables](#environment-variables)
5. [Deployment Steps](#deployment-steps)
6. [Common Errors & Debugging](#common-errors--debugging)
7. [Production Best Practices](#production-best-practices)

---

## Quick Start

### For Local Development (SQLite)
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Initialize database
python init_db.py

# 3. Run app
python app.py
```

### For Railway Deployment (MySQL)
```bash
# 1. Set DATABASE_URL on Railway dashboard
# 2. Deploy your code to Railway
# 3. Run initialization command from Railway CLI
# 4. App automatically uses MySQL connection
```

---

## Local Development Setup

### 1. Install Dependencies
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or on Windows: .venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 2. Configure Local Environment
The `.env` file is already configured for local development:
```
FLASK_ENV=development
DATABASE_URL=  # Leave empty to use SQLite
SQLITE_DB_PATH=instance/sign.db
```

### 3. Initialize Database
```bash
python init_db.py
```

Expected output:
```
============================================================
Sign Language Transcriber - Database Initialization
============================================================

📊 Database Configuration:
Type: SQLite (Local)
URI: sqlite:///instance/sign.db

🔗 Testing database connection...
✅ Database connection successful
🗄️  Creating database tables...
✅ Database tables created successfully
✅ Admin user created
   Username: admin
   Password: admin123
   ⚠️  IMPORTANT: Change this password immediately in production!
✅ Seeded 10 new sign entries

✅ Initialization Complete!
```

### 4. Run Application
```bash
python app.py
```

Open browser: `http://localhost:5000`

---

## Railway MySQL Setup

### Step 1: Create Railway Project
1. Go to [Railway.app](https://railway.app)
2. Create a new project
3. Add MySQL plugin from marketplace

### Step 2: Get MySQL Connection String
1. In Railway dashboard, click on MySQL plugin
2. Go to "Connect" tab
3. Find the **Database URL** field
4. Copy the connection string (looks like: `mysql://root:password@containers-us-west-xyz.railway.app:3306/railway`)

### Step 3: Configure Environment Variables on Railway
In Railway dashboard:
1. Go to **Variables** tab
2. Add new variable:
   - **Key**: `DATABASE_URL`
   - **Value**: Paste your MySQL connection string, but **modify it first**:
     
     Change from:
     ```
     mysql://root:password@containers-us-west-xyz.railway.app:3306/railway
     ```
     
     To (add `+pymysql`):
     ```
     mysql+pymysql://root:password@containers-us-west-xyz.railway.app:3306/railway
     ```

3. Also add:
   - **Key**: `FLASK_ENV`
     - **Value**: `production`
   - **Key**: `SECRET_KEY`
     - **Value**: Generate using: `python3 -c "import secrets; print(secrets.token_hex(32))"`

### Step 4: Deploy Code to Railway

#### Option A: Using Railway CLI
```bash
# Install Railway CLI (if not already installed)
npm i -g @railway/cli

# Login to Railway
railway login

# Link project
railway link

# Deploy
railway up
```

#### Option B: Using GitHub Integration
1. Push code to GitHub repository
2. In Railway dashboard, connect your GitHub repo
3. Railway automatically deploys on every push to `main` branch

### Step 5: Run Database Initialization
Once deployed, run the init script:

```bash
# Using Railway CLI
railway run python init_db.py
```

Or via Railway dashboard's `Deployments` tab, open a shell and run:
```bash
python init_db.py
```

---

## Environment Variables

### Local Development (.env file)
```bash
# Flask
FLASK_ENV=development
FLASK_APP=app.py

# Database (SQLite - no DATABASE_URL needed)
SQLITE_DB_PATH=instance/sign.db

# Security (development only!)
SECRET_KEY=dev-secret-key-local-only
SESSION_COOKIE_SECURE=False

# Other
UPLOAD_FOLDER=uploads
TESTING=False
```

### Railway Production (.env variables in dashboard)
```
DATABASE_URL=mysql+pymysql://user:password@host:port/database
FLASK_ENV=production
SECRET_KEY=<generate-strong-key>
SESSION_COOKIE_SECURE=true
```

### Generate Secure SECRET_KEY
```bash
# Linux/Mac
python3 -c "import secrets; print(secrets.token_hex(32))"

# Output example:
# 8f47e3b2c9d5a1f6e8c3b7d2a9ff4c6e8b3d7f9c2e5a8d1f4c7e9b3d6f9a2c5
```

---

## Deployment Steps

### Complete Deployment Checklist

- [ ] **Create Railway project** with MySQL plugin
- [ ] **Get MySQL connection string** from Railway dashboard
- [ ] **Convert to PyMySQL format** (add `+pymysql`)
- [ ] **Set environment variables** in Railway:
  - `DATABASE_URL`: Your MySQL connection string
  - `FLASK_ENV`: `production`
  - `SECRET_KEY`: Generate new strong key
- [ ] **Push code to GitHub** (or use Railway CLI)
- [ ] **Wait for deployment** to complete
- [ ] **Run init_db.py** via Railway CLI or dashboard shell:
  ```bash
  railway run python init_db.py
  # or in Railway shell:
  python init_db.py
  ```
- [ ] **Test application** by visiting your Railway domain
- [ ] **Login** with admin credentials (from init output)
- [ ] **Change default admin password** immediately

### Verify Database Connection

In Railway dashboard shell:
```bash
python -c "from config import SQLALCHEMY_DATABASE_URI; print(SQLALCHEMY_DATABASE_URI)"
```

Should show your MySQL connection string (masked password is OK).

---

## Common Errors & Debugging

### Error 1: "No module named 'pymysql'"
```
ModuleNotFoundError: No module named 'pymysql'
```

**Solution:**
```bash
pip install PyMySQL==1.1.0
pip freeze > requirements.txt
```

### Error 2: "Database connection failed"
```
SQLAlchemy can't connect to database
```

**Debugging steps:**
1. Check DATABASE_URL format in Railway variables
2. Verify it contains `+pymysql` (not just `mysql://`)
3. Test with database explorer:
   ```bash
   python -c "
   from flask import Flask
   from flask_sqlalchemy import SQLAlchemy
   from config import SQLALCHEMY_DATABASE_URI
   print(f'Connection string: {SQLALCHEMY_DATABASE_URI}')
   app = Flask(__name__)
   app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
   db = SQLAlchemy(app)
   with app.app_context():
       from sqlalchemy import text
       result = db.session.execute(text('SELECT 1'))
       print('✅ Connection successful!')
   "
   ```

### Error 3: "Lost connection to MySQL server"
```
(pymysql.err.OperationalError) (2006, "MySQL server has gone away")
```

**Cause:** Connection timeout or pool exhaustion

**Solution:** Already configured in `config.py`:
- `pool_pre_ping=True` - Tests connection before use
- `pool_recycle=3600` - Recycles connections after 1 hour
- `pool_size=10` - Maintains 10 connections

### Error 4: "OperationalError: (1045, "Access denied for user")"
```
Access denied, check credentials
```

**Debugging:**
1. Copy exact connection string from Railway MySQL "Connect" tab
2. Format it correctly: `mysql+pymysql://user:pass@host:port/database`
3. Special characters in password? URL encode them:
   - `@` → `%40`
   - `:` → `%3A`
   - `#` → `%23`

Example: If password is `p@ss:word`, use:
```
mysql+pymysql://root:p%40ss%3Aword@host:3306/database
```

### Error 5: "init_db.py fails on Railway"
```
Error creating tables: ...
```

**Debugging:**
```bash
# Test connection first
railway run python -c "import app; print('Flask imported successfully')"

# Run init with verbose output
railway run python init_db.py

# Check deployed environment
railway run env | grep DATABASE_URL
```

---

## Production Best Practices

### 1. Database Backups
Railway includes daily backups. To access:
1. In Railway dashboard, go to MySQL plugin
2. Click "Backups" tab
3. Download backup files regularly

### 2. Set Strong Passwords
```bash
# No default passwords in production!
# Always use strong admin credentials
# Change default password immediately after setup
```

### 3. Connection Security
Currently configured in `config.py`:
- ✅ Connection pool validation (`pool_pre_ping`)
- ✅ Connection recycling to prevent timeouts
- ✅ HTTPS enforcement on Railway (use custom domain)

### 4. Database User Privileges
Consider creating limited-privilege user for app:
```sql
-- As MySQL admin
CREATE USER 'transcriber'@'%' IDENTIFIED BY 'strong-password';
GRANT ALL PRIVILEGES ON railway.* TO 'transcriber'@'%';
FLUSH PRIVILEGES;
```

Then use in `DATABASE_URL`:
```
mysql+pymysql://transcriber:strong-password@host:port/database
```

### 5. Monitor Database Performance
In Railway dashboard:
- CPU/Memory usage in MySQL plugin
- View slow queries
- Check connection count

### 6. Session Cookie Security
Automatically set in `config.py`:
```python
SESSION_COOKIE_SECURE = IS_PRODUCTION  # True for HTTPS
SESSION_COOKIE_HTTPONLY = True
```

### 7. Health Checks
Add to your routes:
```python
@app.route('/health')
def health():
    """Health check endpoint for monitoring"""
    try:
        from sqlalchemy import text
        db.session.execute(text('SELECT 1'))
        return {'status': 'healthy', 'database': 'connected'}, 200
    except Exception as e:
        return {'status': 'unhealthy', 'error': str(e)}, 500
```

---

## Switching Databases (Local ↔ Production)

### From SQLite to MySQL
```bash
# 1. Make sure no DATABASE_URL in .env
# 2. Set DATABASE_URL on Railway
# 3. Run: python init_db.py
# ✅ Your database is now using MySQL
```

### From MySQL Back to SQLite (for testing)
```bash
# 1. Unset DATABASE_URL in environment
# 2. Run: python init_db.py
# ✅ Your database is now using SQLite
```

---

## File Changes Summary

✅ **Updated Files:**
- `requirements.txt` - Added PyMySQL
- `config.py` - Added MySQL support, connection pooling, env detection
- `.env.example` - Added Railway MySQL instructions
- `.env` - Local development configuration
- `init_db.py` - Enhanced with connection testing and better error handling

✅ **How They Work Together:**
1. `.env` or `.env.example` → Contains variables
2. `config.py` → Reads variables, detects environment, configures SQLAlchemy
3. `init_db.py` → Uses config to connect and initialize database
4. `app.py` → Uses config for Flask and SQLAlchemy setup

---

## Next Steps for Presentation

For a university presentation, demo these steps:
1. Show `.env` file explaining local vs production setup
2. Show Railway dashboard MySQL plugin credentials
3. Run `python init_db.py` to show connection testing
4. Show `config.py` to explain how it detects environments
5. Explain connection pooling and why it's important
6. Show error handling with `pool_pre_ping` explanation
7. Deploy to Railway and re-run `init_db.py` to show MySQL in action

---

## Troubleshooting Checklist

Before asking for help, verify:
- [ ] PyMySQL installed: `pip list | grep PyMySQL`
- [ ] DATABASE_URL set correctly on Railway or unset for local
- [ ] Format includes `+pymysql`: `mysql+pymysql://...`
- [ ] init_db.py runs without connection errors
- [ ] Admin user created: Check Railway MySQL or local database
- [ ] Session cookies secure setting matches environment
- [ ] Upload folder exists and is writable
- [ ] No hardcoded database URLs in code

---

## More Resources

- [Railway Documentation](https://docs.railway.app)
- [SQLAlchemy MySQL Guide](https://docs.sqlalchemy.org/en/14/dialects/mysql.html)
- [Flask-SQLAlchemy Documentation](https://flask-sqlalchemy.palletsprojects.com)
- [PyMySQL Documentation](https://pymysql.readthedocs.io)

