# Railway MySQL Deployment Checklist

Use this checklist to verify your deployment is correctly configured.

## Pre-Deployment (Before Pushing to Railway)

### Code Preparation
- [ ] Python code pushed to GitHub repository
- [ ] `.gitignore` includes `.env` (don't commit local environment)
- [ ] No hardcoded database URLs in code
- [ ] No hardcoded passwords or credentials
- [ ] requirements.txt contains PyMySQL==1.1.0
- [ ] Ran `pip freeze > requirements.txt` if dependencies changed

### Local Testing
- [ ] Virtual environment created: `.venv/`
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Local database initialized: `python init_db.py`
- [ ] Application starts: `python app.py`
- [ ] Can access: http://localhost:5000
- [ ] Can login with admin/admin123
- [ ] Can create transcripts and database operations work

### Documentation
- [ ] Read DATABASE_INTEGRATION.md
- [ ] Read RAILWAY_DEPLOYMENT.md
- [ ] Understand config.py database connection logic

---

## Railway Setup

### Create Railway Project
- [ ] Created account at railway.app
- [ ] Created new project
- [ ] Added MySQL plugin to project
- [ ] MySQL plugin showing green "Connected" status

### Get MySQL Credentials
- [ ] Opened MySQL plugin → "Connect" tab
- [ ] Copied database connection string
- [ ] Connection string format: `mysql://user:password@host:port/database`

### Set Environment Variables on Railway

In Railway Dashboard → **Variables** tab, add:

- [ ] **DATABASE_URL**
  - [ ] Original: `mysql://...`
  - [ ] Modified: `mysql+pymysql://...` (added `+pymysql`)
  - [ ] Verified no typos
  - [ ] Password characters URL-encoded if needed (@ → %40, : → %3A)

- [ ] **FLASK_ENV**
  - [ ] Set to: `production`

- [ ] **SECRET_KEY**
  - [ ] Generated strong key: `python3 -c "import secrets; print(secrets.token_hex(32))"`
  - [ ] Not the default dev key
  - [ ] Copied exactly into Railway

- [ ] **Optional - UPLOAD_FOLDER**
  - [ ] Set to: `uploads` (default)

---

## Deployment

### Deploy Code
- [ ] Code uploaded to GitHub
- [ ] Railway GitHub integration configured (auto-deploy on push)
- [ ] Waiting for deployment to complete (check Railway logs)
- [ ] Deployment shows green checkmark
- [ ] No error logs in Deployments view

### Initialize Database

Choose one method:

**Method A: Railway CLI**
```bash
railway run python init_db.py
```
- [ ] Executed successfully
- [ ] Output shows: "✅ Database connection successful"
- [ ] Output shows: "✅ Database tables created successfully"
- [ ] Output shows: "✅ Admin user created"

**Method B: Railway Dashboard Shell**
1. [ ] Go to Railway Dashboard → Deployments → Running deployment
2. [ ] Click "Shell" button
3. [ ] Run: `python init_db.py`
4. [ ] See same success messages

---

## Post-Deployment Verification

### Test Application URL
- [ ] Found your Railway app domain in dashboard
- [ ] Opened https://your-app-name.railway.app in browser
- [ ] Homepage loads without errors
- [ ] Can click "Login" button

### Test Database Connection
- [ ] Logged in with admin/admin123
- [ ] No "database connection" errors
- [ ] Can navigate dashboard without 500 errors
- [ ] Can view user profile

### Test Health Endpoint
```bash
curl https://your-app-name.railway.app/health
```
- [ ] Returns JSON response
- [ ] Shows: `"status": "healthy"`
- [ ] Shows: `"database": "connected"`

### Verify Database is MySQL (not SQLite)
- [ ] In Railway dashboard: MySQL plugin shows connection activity
- [ ] Database has same tables as local version
- [ ] Admin user exists in Railway MySQL

### Test Basic Operations
- [ ] Can create new user (register page)
- [ ] Can transcribe/upload (if feature available)
- [ ] Can view admin dashboard (if admin)
- [ ] No 500 errors in activity

---

## Common Issues - Troubleshooting

### Issue: Deployment fails with database error
```
❌ Error: can't connect to MySQL server
```
**Solution:**
- [ ] Check DATABASE_URL in Railway variables
- [ ] Verify format is `mysql+pymysql://...` (not just `mysql://`)
- [ ] Check password doesn't have special unescaped characters
- [ ] Run init_db.py fails? Check railway run command output

### Issue: init_db.py fails on Railway
```
❌ Error during initialization: ...
```
**Debugging:**
```bash
# Check variables are set
railway run env | grep DATABASE_URL
railway run env | grep FLASK_ENV

# Test connection directly
railway run python -c "
from config import SQLALCHEMY_DATABASE_URI
print(f'Using: {SQLALCHEMY_DATABASE_URI}')
"

# Run with more output
railway run python init_db.py
```

### Issue: Application works but shows wrong database
**Verify which database:**
```bash
railway run python -c "
from config import SQLALCHEMY_DATABASE_URI
if 'mysql' in SQLALCHEMY_DATABASE_URI.lower():
    print('✅ Using MySQL')
elif 'sqlite' in SQLALCHEMY_DATABASE_URI.lower():
    print('❌ Using SQLite (DATABASE_URL not set!)')
else:
    print('? Unknown:', SQLALCHEMY_DATABASE_URI)
"
```

### Issue: "Lost connection to MySQL server" errors
**Solution:** Already configured in code
- [ ] Verify config.py has `pool_pre_ping=True`
- [ ] Verify config.py has `pool_recycle=3600`
- [ ] These settings prevent connection timeout issues

### Issue: Can't connect to Railway MySQL from local machine
**Note:** Railway MySQL can only be accessed from Railway environment (for security)
- [ ] This is expected and correct
- [ ] Local testing uses SQLite
- [ ] Railway deployment uses MySQL
- [ ] Data does NOT transfer between them

---

## After Successful Deployment

### Maintenance
- [ ] Bookmark your app URL
- [ ] Save admin credentials (write down or password manager)
- [ ] Monitor Railway dashboard for errors
- [ ] Check logs daily for first week
- [ ] Set up Railway notifications (optional)

### Security
- [ ] ✅ Changed default admin password
- [ ] ✅ Verified SECRET_KEY is unique and strong
- [ ] ✅ FLASK_ENV set to production
- [ ] ✅ DATABASE_URL set (not public)

### Backups
- [ ] Note: Railway includes daily automatic backups
- [ ] Access backups: Railway Dashboard → MySQL → Backups tab
- [ ] Optional: Download backup regularly for additional safety

### Next Steps
- [ ] Train users on new system
- [ ] Prepare for demo/presentation
- [ ] Document any deployment-specific notes
- [ ] Plan for future scaling (more users, more data)

---

## Quick Reference Commands

```bash
# Check deployment status
railway status

# View deployment logs
railway logs

# Run initialization on Railway
railway run python init_db.py

# Test database connection
railway run python -c "from config import SQLALCHEMY_DATABASE_URI; print(SQLALCHEMY_DATABASE_URI)"

# Open Railway shell for manual commands
railway shell

# Check environment variables
railway run env | grep -E "DATABASE_URL|FLASK_ENV|SECRET_KEY"

# Download latest backup
# Go to: Railway Dashboard → MySQL → Backups → Download
```

---

## Success Criteria

You'll know deployment is successful when:

✅ Application URL loads without errors  
✅ Can login with admin credentials  
✅ `/health` endpoint returns `"status": "healthy"`  
✅ Database operations work (create, read, update, delete)  
✅ Railway MySQL plugin shows connection activity  
✅ No 500 errors in recent logs  
✅ Performance is acceptable (pages load in <2 seconds)  

---

## Rollback Plan

If something goes wrong:

1. **Quick Fix** (database still accessible)
   ```bash
   railway run python init_db.py  # Re-run initialization
   ```

2. **Revert Code** (if you pushed bad code)
   ```bash
   git revert HEAD  # Revert last commit
   git push
   # Railway auto-redeploys
   ```

3. **Factory Reset** (nuclear option)
   - Go to Railway Dashboard
   - Delete deployment
   - Delete MySQL plugin
   - Create new MySQL plugin
   - Redeploy from GitHub
   - Run init_db.py again

4. **Use Backup** (if data corrupted)
   - Go to Railway MySQL → Backups
   - Download and restore locally for analysis
   - Contact Railway support if needed

---

## Getting Help

If stuck:
1. Check `DATABASE_INTEGRATION.md` - Comprehensive troubleshooting
2. Review demo script in `INTEGRATION_SUMMARY.md`
3. Check Railway logs: Railway Dashboard → Deployments
4. Review `config.py` comments
5. Test locally first to isolate the issue
6. Visit [Railway Docs](https://docs.railway.app)

---

**Last Updated:** 2026-04-09
**For:** Sign Language Transcriber Flask Application
**Version:** 1.0

