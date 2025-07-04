#!/usr/bin/env python3
"""
Run script for the Job Board Flask application
Starts the development server with proper configuration
"""
import os
import sys
from datetime import datetime, UTC

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import Flask app
from app import create_app
from app.models import db, Job, JobService

def create_sample_data():
    """Create sample job data if database is empty"""
    try:
        # Check if we already have jobs
        job_count = Job.query.count()
        if job_count > 0:
            print(f"📊 Database already has {job_count} jobs")
            return
        
        print("🔄 Creating sample job data...")
        
        sample_jobs = [
            {
                'title': 'Senior Actuarial Analyst',
                'company': 'MetLife',
                'location': 'New York, NY',
                'job_type': 'Full-time',
                'description': 'We are seeking a Senior Actuarial Analyst to join our Life Insurance team. The ideal candidate will have 3-5 years of actuarial experience and be working towards their ASA designation.',
                'experience_level': 'Senior',
                'remote_allowed': True,
                'tags': 'ASA, Life Insurance, Pricing, Excel, VBA',
                'salary_range': '$80,000 - $120,000',
                'source_url': 'https://careers.metlife.com/jobs/actuarial-analyst',
                'is_scraped': False,
                'posting_date': datetime.now(UTC)
            },
            {
                'title': 'Actuarial Intern - Summer 2025',
                'company': 'Prudential Financial',
                'location': 'Newark, NJ',
                'job_type': 'Internship',
                'description': 'Join our summer internship program and gain hands-on experience in actuarial science. Perfect for students pursuing actuarial science or related degrees.',
                'experience_level': 'Internship',
                'remote_allowed': False,
                'tags': 'Internship, Student, Training, Life Insurance',
                'salary_range': '$25 - $30/hour',
                'source_url': 'https://careers.prudential.com/internships',
                'is_scraped': False,
                'posting_date': datetime.now(UTC)
            },
            {
                'title': 'Health Actuary',
                'company': 'Aetna',
                'location': 'Hartford, CT',
                'job_type': 'Full-time',
                'description': 'Responsible for pricing health insurance products, conducting experience studies, and supporting regulatory compliance initiatives.',
                'experience_level': 'Mid-Level',
                'remote_allowed': True,
                'tags': 'Health Insurance, FSA, Pricing, Regulatory',
                'salary_range': '$90,000 - $130,000',
                'source_url': 'https://careers.aetna.com/health-actuary',
                'is_scraped': False,
                'posting_date': datetime.now(UTC)
            }
        ]
        
        created_count = 0
        for job_data in sample_jobs:
            try:
                job = JobService.create_job(job_data)
                created_count += 1
                print(f"✅ Created: {job.title} at {job.company}")
            except Exception as e:
                print(f"❌ Failed to create job: {e}")
        
        print(f"🎉 Created {created_count} sample jobs")
        
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")

def print_startup_info(app):
    """Print startup information"""
    print("\n" + "="*60)
    print("🚀 Job Board Application Starting")
    print("="*60)
    print(f"📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 Environment: {app.config.get('ENV', 'development')}")
    print(f"🔧 Debug Mode: {app.config.get('DEBUG', False)}")
    print(f"💾 Database: {app.config.get('SQLALCHEMY_DATABASE_URI', 'Not configured')}")
    print(f"🔑 Secret Key: {'Set' if app.config.get('SECRET_KEY') else 'Not set'}")
    
    # Database stats
    try:
        with app.app_context():
            stats = JobService.get_job_stats()
            print(f"📊 Total Jobs: {stats['total']}")
            print(f"🏢 Companies: {stats['companies']}")
            print(f"🆕 Recent Jobs: {stats['recent']}")
    except Exception as e:
        print(f"⚠️ Could not get database stats: {e}")
    
    print("\n🌍 Server URLs:")
    print("   Frontend: http://localhost:3000")
    print("   Backend:  http://localhost:5000")
    print("   API:      http://localhost:5000/api")
    print("   Health:   http://localhost:5000/api/health")
    print("\n💡 Useful Commands:")
    print("   Ctrl+C    - Stop server")
    print("   /api/jobs - View all jobs")
    print("   /api/scrape - Trigger scraper")
    print("="*60)

def setup_database(app):
    """Setup database tables and initial data"""
    with app.app_context():
        try:
            # Create tables
            print("🔄 Setting up database...")
            db.create_all()
            print("✅ Database tables created")
            
            # Create sample data if needed
            create_sample_data()
            
        except Exception as e:
            print(f"❌ Database setup failed: {e}")
            sys.exit(1)

def main():
    """Main application entry point"""
    try:
        # Create Flask application
        app = create_app()
        
        # Setup database
        setup_database(app)
        
        # Print startup information
        print_startup_info(app)
        
        # Get configuration
        host = os.getenv('FLASK_HOST', '127.0.0.1')
        port = int(os.getenv('FLASK_PORT', 5000))
        debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
        
        # Start the development server
        print(f"\n🚀 Starting server on http://{host}:{port}")
        print("Press Ctrl+C to stop the server\n")
        
        app.run(
            host=host,
            port=port,
            debug=debug,
            use_reloader=debug,
            threaded=True
        )
        
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Failed to start server: {e}")
        sys.exit(1)

def print_help():
    """Print help information"""
    print("""
Job Board Application - Run Script

Usage:
    python run.py [options]

Options:
    --help, -h     Show this help message
    --host HOST    Set host address (default: 127.0.0.1)
    --port PORT    Set port number (default: 5000)
    --debug        Enable debug mode
    --no-debug     Disable debug mode

Environment Variables:
    FLASK_HOST     Host address (default: 127.0.0.1)
    FLASK_PORT     Port number (default: 5000)
    FLASK_DEBUG    Debug mode (default: True)
    FLASK_ENV      Environment (development/production)

Examples:
    python run.py
    python run.py --host 0.0.0.0 --port 8000
    python run.py --debug
    FLASK_PORT=8080 python run.py

Database:
    The application uses SQLite by default (jobboard.db)
    Tables are created automatically on first run
    Sample data is added if database is empty

API Endpoints:
    GET  /api/health          - Health check
    GET  /api/jobs            - Get all jobs
    POST /api/jobs            - Create new job
    GET  /api/jobs/<id>       - Get specific job
    PUT  /api/jobs/<id>       - Update job
    DELETE /api/jobs/<id>     - Delete job
    POST /api/scrape          - Trigger job scraper

For more information, visit: https://github.com/your-repo/job-board
    """)

if __name__ == '__main__':
    # Handle command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] in ['--help', '-h']:
            print_help()
            sys.exit(0)
        elif sys.argv[1] == '--host' and len(sys.argv) > 2:
            os.environ['FLASK_HOST'] = sys.argv[2]
        elif sys.argv[1] == '--port' and len(sys.argv) > 2:
            os.environ['FLASK_PORT'] = sys.argv[2]
        elif sys.argv[1] == '--debug':
            os.environ['FLASK_DEBUG'] = 'True'
        elif sys.argv[1] == '--no-debug':
            os.environ['FLASK_DEBUG'] = 'False'
    
    # Run the application
    main()