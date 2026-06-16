#!/bin/bash
# Velvet Hour Audit - Setup Script

echo "🚀 Setting up Velvet Hour Audit..."

# Create virtual environment
echo "📦 Creating Python virtual environment..."
python3 -m venv ../venv
source ../venv/bin/activate

# Install dependencies
echo "📥 Installing Python dependencies..."
pip install -r ../requirements.txt

# Initialize database
echo "🗄️  Initializing database..."
python setup_db.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the backend:"
echo "  cd backend && source venv/bin/activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "To start the frontend:"
echo "  cd frontend && npm install && npm run dev"