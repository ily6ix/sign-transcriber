# Railway Deployment Quick Reference

## 30-Second Setup

### 1. Create Railway MySQL Database
```
Go to railway.app → New Project → Add MySQL
```

### 2. Get Connection String
```
Railway Dashboard → MySQL → Connect tab → Copy Database URL
Convert: mysql:// → mysql+pymysql://
Example:
  FROM: mysql://root:pass@containers-us-west-123.railway.app:3306/railway
  TO:   mysql+pymysql://root:pass@containers-us-west-123.railway.app:3306/railway
```

### 3. Set Environment Variables on Railway
| Variable | Value | Example |
|----------|-------|---------|
| `DATABASE_URL` | Your MySQL connection string | `mysql+pymysql://root:pass@host:port/database` |
| `FLASK_ENV` | `production` | `production` |
| `SECRET_KEY` | Generate: `python3 -c "import secrets; print(secrets.token_hex(32))"` | `8f47e3b2c9d5a1f6e8c3b7d2a9ff4c6e8b3d7f9c2e5a8d1f4c7e9b3d6f9a2c5` |

### 4. Deploy Code
```bash
# Option A: GitHub Integration (Recommended)
git push origin main  # Railway auto-deploys

# Option B: Railway CLI
railway up
```

### 5. Initialize Database
```bash
# Via Railway CLI
railway run python init_db.py

# Or via Railway Dashboard shell
python init_db.py
```

### 6. Test Application
- Visit your Railway domain (shown in dashboard)
- Login with `admin` / `admin123`
- **Change password immediately!**

---

## Environment Variables Template

Copy to Railway dashboard **Variables** tab:

```
DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@YOUR_HOST:3306/railway
FLASK_ENV=production
SECRET_KEY=YOUR_GENERATED_SECRET_KEY_HERE
SESSION_COOKIE_SECURE=true
UPLOAD_FOLDER=uploads
```

---

## Common Issues

| Error | Solution |
|-------|----------|
| `pymysql not found` | PyMySQL already in requirements.txt ✓ |
| `Connection refused` | Check DATABASE_URL format (must have `+pymysql`) |
| `Access denied` | Verify MySQL password, check for special characters |
| `Table doesn't exist` | Run: `railway run python init_db.py` |
| `Port already in use` | Railway handles port allocation automatically |

---

## Verification Steps

### Verify Deployment
```bash
# Check environment variables
railway run env | grep DATABASE_URL

# Test connection
railway run python -c "
from config import SQLALCHEMY_DATABASE_URI
print('✅ Using:', SQLALCHEMY_DATABASE_URI)
"

# Check database
railway run python -c "
from app import app, db
from models import User
with app.app_context():
    users = User.query.all()
    print(f'✅ Found {len(users)} users')
"
```

### Monitor Application
- View logs: Railway dashboard → Deployments → View logs
- Check health: `https://your-app.railway.app/health` (if endpoint added)
- Monitor database: Railway dashboard → MySQL → Plugin metrics

---

## Rollback Database Connection

If you need to switch back to SQLite:
```bash
# 1. Remove DATABASE_URL from Railway variables
# 2. Redeploy
# App will use default SQLite at instance/sign.db
```

---

## Files You Modified

✅ `requirements.txt` - Added PyMySQL  
✅ `config.py` - MySQL support + connection pooling  
✅ `.env` - Local development config  
✅ `.env.example` - Setup instructions  
✅ `init_db.py` - Connection testing + error handling  
✅ `DATABASE_INTEGRATION.md` - Comprehensive guide (THIS FILE)  
✅ `RAILWAY_DEPLOYMENT.md` - Quick reference (THIS FILE)  

---

## For Presentation Demo

**Live Demo Script:**
```
1. "Show I have a Flask app" → run app.py locally
2. "Switch to MySQL" → set DATABASE_URL to Railway MySQL
3. "Run init script" → python init_db.py (shows connection testing)
4. "Check database" → Select from users table via Railway dashboard
5. "Login and use app" → Shows it works with MySQL
6. "Switch back to SQLite" → Unset DATABASE_URL, restart
7. "Explain how it works" → Show config.py logic
```

---

## Security Checklist for Production

- [ ] Changed default admin password
- [ ] Generated strong SECRET_KEY
- [ ] Set FLASK_ENV=production
- [ ] DATABASE_URL includes `+pymysql`
- [ ] SESSION_COOKIE_SECURE=true on Railway
- [ ] No hardcoded paths or credentials in code
- [ ] Backup MySQL database regularly (Railway includes daily backups)
- [ ] Monitor application logs in Railway dashboard

---

## Support

If stuck:
1. Check `DATABASE_INTEGRATION.md` (comprehensive guide)
2. Review error logs in Railway dashboard
3. Verify all environment variables are set
4. Test connection locally with same DATABASE_URL
5. Check PyMySQL installation: `pip show PyMySQL`

