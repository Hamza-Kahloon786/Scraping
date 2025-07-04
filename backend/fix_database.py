"""
Quick fix for SQLAlchemy 2.x compatibility issues
Run this script to fix the database connection problems
"""
import os
import re

def fix_database_py():
    """Fix the database.py file"""
    database_file = os.path.join("app", "database.py")
    
    if not os.path.exists(database_file):
        print(f"❌ {database_file} not found")
        return False
    
    try:
        with open(database_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix the check_database_connection function
        old_pattern = r"db\.session\.execute\('SELECT 1'\)"
        new_pattern = "from sqlalchemy import text\n        db.session.execute(text('SELECT 1'))"
        
        if old_pattern in content:
            # Add import at the top if not already there
            if "from sqlalchemy import text" not in content:
                content = content.replace(
                    "def check_database_connection():",
                    "def check_database_connection():\n    \"\"\"Test database connection\"\"\"\n    try:\n        # Try to execute a simple query (SQLAlchemy 2.x compatible)\n        from sqlalchemy import text\n        db.session.execute(text('SELECT 1'))\n        print(\"✅ Database connection successful!\")\n        return True\n    except Exception as e:\n        print(f\"❌ Database connection failed: {e}\")\n        return False"
                )
                
                # Remove the old function implementation
                content = re.sub(
                    r'def check_database_connection\(\):\s*"""Test database connection"""\s*try:\s*# Try to execute a simple query\s*db\.session\.execute\(\'SELECT 1\'\)\s*print\("✅ Database connection successful!"\)\s*return True\s*except Exception as e:\s*print\(f"❌ Database connection failed: \{e\}"\)\s*return False',
                    '',
                    content,
                    flags=re.DOTALL
                )
        else:
            # Replace the execute statement
            content = content.replace(
                "db.session.execute('SELECT 1')",
                "from sqlalchemy import text\n        db.session.execute(text('SELECT 1'))"
            )
        
        with open(database_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Fixed {database_file}")
        return True
        
    except Exception as e:
        print(f"❌ Error fixing {database_file}: {e}")
        return False

def fix_routes_py():
    """Fix the routes.py file"""
    routes_file = os.path.join("app", "routes.py")
    
    if not os.path.exists(routes_file):
        print(f"❌ {routes_file} not found")
        return False
    
    try:
        with open(routes_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix the health check function
        if "db.session.execute('SELECT 1')" in content:
            content = content.replace(
                "# Test database connection\n        db.session.execute('SELECT 1')",
                "# Test database connection\n        from sqlalchemy import text\n        db.session.execute(text('SELECT 1'))"
            )
        
        with open(routes_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Fixed {routes_file}")
        return True
        
    except Exception as e:
        print(f"❌ Error fixing {routes_file}: {e}")
        return False

def create_fixed_database_py():
    """Create a completely new database.py file"""
    database_content = '''"""
Database configuration and utilities
"""
from flask import current_app
from app.models import db, Job
from datetime import datetime, timedelta
import random
from sqlalchemy import text

def init_db():
    """Initialize the database with tables"""
    try:
        db.create_all()
        print("✅ Database tables created successfully!")
        return True
    except Exception as e:
        print(f"❌ Error creating database tables: {e}")
        return False

def seed_sample_data():
    """Add sample job data for testing"""
    
    # Check if we already have data
    if Job.query.count() > 0:
        print("📊 Database already contains job data. Skipping sample data creation.")
        return
    
    sample_jobs = [
        {
            'title': 'Senior Actuarial Analyst',
            'company': 'MetLife Insurance',
            'location': 'New York, NY',
            'job_type': 'Full-time',
            'tags': 'Life Insurance, Pricing, Python, SQL',
            'description': 'Looking for an experienced actuarial analyst to join our life insurance team.',
            'experience_level': 'Senior',
            'remote_allowed': False,
            'posting_date': datetime.utcnow() - timedelta(days=2)
        },
        {
            'title': 'Entry Level Actuary',
            'company': 'Progressive Insurance',
            'location': 'Columbus, OH',
            'job_type': 'Full-time',
            'tags': 'Auto Insurance, Entry Level, Excel, Statistics',
            'description': 'Great opportunity for new graduates to start their actuarial career.',
            'experience_level': 'Entry Level',
            'remote_allowed': True,
            'posting_date': datetime.utcnow() - timedelta(days=5)
        },
        {
            'title': 'Actuarial Consultant',
            'company': 'Milliman',
            'location': 'Seattle, WA',
            'job_type': 'Full-time',
            'tags': 'Consulting, Health Insurance, Modeling, ASA',
            'description': 'Join our consulting team to work with various healthcare clients.',
            'experience_level': 'Mid-Level',
            'remote_allowed': True,
            'posting_date': datetime.utcnow() - timedelta(days=1)
        },
        {
            'title': 'Pricing Actuary Intern',
            'company': 'State Farm',
            'location': 'Bloomington, IL',
            'job_type': 'Internship',
            'tags': 'Internship, Pricing, Property Insurance, Student',
            'description': 'Summer internship program for actuarial science students.',
            'experience_level': 'Internship',
            'remote_allowed': False,
            'posting_date': datetime.utcnow() - timedelta(days=7)
        },
        {
            'title': 'Chief Actuary',
            'company': 'Anthem Health',
            'location': 'Indianapolis, IN',
            'job_type': 'Full-time',
            'tags': 'Leadership, Health Insurance, FSA, Executive',
            'description': 'Lead our actuarial team and drive strategic initiatives.',
            'experience_level': 'Executive',
            'remote_allowed': False,
            'posting_date': datetime.utcnow() - timedelta(days=3)
        }
    ]
    
    try:
        for job_data in sample_jobs:
            job = Job(**job_data)
            db.session.add(job)
        
        db.session.commit()
        print(f"✅ Added {len(sample_jobs)} sample jobs to the database!")
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error adding sample data: {e}")

def clear_all_jobs():
    """Clear all job data from database"""
    try:
        num_deleted = Job.query.delete()
        db.session.commit()
        print(f"🗑️ Deleted {num_deleted} jobs from database.")
        return num_deleted
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error clearing jobs: {e}")
        return 0

def get_database_stats():
    """Get basic database statistics"""
    try:
        total_jobs = Job.query.count()
        
        # Jobs by type
        job_types = db.session.query(Job.job_type, db.func.count(Job.id)).group_by(Job.job_type).all()
        
        # Recent jobs (last 7 days)
        recent_date = datetime.utcnow() - timedelta(days=7)
        recent_jobs = Job.query.filter(Job.posting_date >= recent_date).count()
        
        # Scraped vs manual jobs
        scraped_jobs = Job.query.filter(Job.is_scraped == True).count()
        manual_jobs = Job.query.filter(Job.is_scraped == False).count()
        
        stats = {
            'total_jobs': total_jobs,
            'job_types': dict(job_types),
            'recent_jobs': recent_jobs,
            'scraped_jobs': scraped_jobs,
            'manual_jobs': manual_jobs
        }
        
        return stats
        
    except Exception as e:
        print(f"❌ Error getting database stats: {e}")
        return None

def check_database_connection():
    """Test database connection"""
    try:
        # Try to execute a simple query (SQLAlchemy 2.x compatible)
        db.session.execute(text('SELECT 1'))
        print("✅ Database connection successful!")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False
'''
    
    try:
        os.makedirs("app", exist_ok=True)
        with open(os.path.join("app", "database.py"), 'w', encoding='utf-8') as f:
            f.write(database_content)
        print("✅ Created new database.py file")
        return True
    except Exception as e:
        print(f"❌ Error creating database.py: {e}")
        return False

def main():
    """Main fix function"""
    print("🔧 SQLAlchemy 2.x Compatibility Fix")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not os.path.exists("app"):
        print("❌ 'app' directory not found. Please run this script from the backend directory.")
        return
    
    # Try to fix existing files first
    success = True
    
    print("1. Fixing database.py...")
    if not fix_database_py():
        print("🔄 Creating new database.py...")
        success = create_fixed_database_py()
    
    print("2. Fixing routes.py...")
    fix_routes_py()
    
    if success:
        print("\n✅ Fix completed successfully!")
        print("🚀 Now try running: python init_db.py")
    else:
        print("\n⚠️ Some fixes may have failed. Check the error messages above.")

if __name__ == "__main__":
    main()