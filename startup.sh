#!/bin/bash

# SignaTranslate - Startup Script

echo "🚀 Starting SignaTranslate..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt -q

# Initialize database
echo "🗄️  Initializing database..."
python app.py << EOF
from flask import Flask
from models import db, User
from config import *
app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)
with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin',
            email='admin@signatranslate.com',
            full_name='Administrator',
            role='admin'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("✅ Database initialized with admin user (admin/admin123)")
    else:
        print("✅ Database already initialized")
EOF

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Access the application at: http://localhost:5000"
echo ""
echo "🔐 Default credentials:"
echo "   Username: admin"
echo "   Password: admin123"
echo ""
echo "⚠️  Remember to change the default password in production!"
echo ""
echo "🚀 Starting Flask development server..."
python app.py
