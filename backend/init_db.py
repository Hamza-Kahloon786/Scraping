"""
Database initialization script
Run this script to set up the database with sample data
"""
from app import create_app
from app.database import init_db, seed_sample_data, check_database_connection, get_database_stats

def main():
    """Initialize database and add sample data"""
    print("🚀 Job Board Database Initialization")
    print("=" * 50)
    
    # Create Flask app context
    app = create_app()
    
    with app.app_context():
        # Check database connection
        print("1. Testing database connection...")
        if not check_database_connection():
            print("❌ Cannot connect to database. Please check your configuration.")
            return False
        
        # Initialize database tables
        print("2. Creating database tables...")
        if not init_db():
            print("❌ Failed to create database tables.")
            return False
        
        # Add sample data
        print("3. Adding sample job data...")
        seed_sample_data()
        
        # Show statistics
        print("4. Database statistics:")
        stats = get_database_stats()
        if stats:
            print(f"   📊 Total jobs: {stats['total_jobs']}")
            print(f"   🆕 Recent jobs (7 days): {stats['recent_jobs']}")
            print(f"   🤖 Scraped jobs: {stats['scraped_jobs']}")
            print(f"   ✋ Manual jobs: {stats['manual_jobs']}")
            print(f"   📈 Job types: {stats['job_types']}")
        
        print("=" * 50)
        print("✅ Database initialization completed successfully!")
        print("🚀 You can now start the Flask app with: python run.py")
        print("🌐 API will be available at: http://localhost:5000/api/jobs")
        
        return True

if __name__ == '__main__':
    main()