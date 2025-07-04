"""
Database configuration and utilities
"""
from flask import current_app
from app.models import db, Job
from datetime import datetime, timedelta
import random

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
        # Try to execute a simple query
        from sqlalchemy import text
        db.session.execute(text('SELECT 1'))
        print("✅ Database connection successful!")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False