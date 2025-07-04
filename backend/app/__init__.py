import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_app(config_name=None):
    app = Flask(__name__)
    
    # Database configuration - try PostgreSQL first, fallback to SQLite
    database_url = os.getenv('DATABASE_URL')
    
    # Test PostgreSQL connection
    if database_url:
        try:
            # Try to import psycopg2 to test if it's working
            import psycopg2
            app.config['SQLALCHEMY_DATABASE_URI'] = database_url
            print(f"🐘 Using PostgreSQL: {database_url.split('@')[1] if '@' in database_url else 'configured'}")
        except ImportError as e:
            print(f"⚠️ PostgreSQL driver not available: {e}")
            print("📁 Falling back to SQLite for development")
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobboard.db'
        except Exception as e:
            print(f"⚠️ PostgreSQL connection failed: {e}")
            print("📁 Falling back to SQLite for development")
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobboard.db'
    else:
        # No PostgreSQL URL configured, use SQLite
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobboard.db'
        print("📁 Using SQLite: jobboard.db")
    
    # Basic config
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    app.config['ENV'] = os.getenv('FLASK_ENV', 'development')
    
    # CORS Configuration
    cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')
    CORS(app, resources={
        r"/api/*": {
            "origins": cors_origins,
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Initialize database
    from app.models import db
    db.init_app(app)
    
    # Import and register routes AFTER app is configured
    try:
        from app.routes import api
        app.register_blueprint(api)
        print("✅ Routes registered successfully")
    except ImportError as e:
        print(f"❌ Error importing routes: {e}")
        raise e
    
    @app.route('/')
    def index():
        return jsonify({
            'message': 'Job Board API', 
            'status': 'running',
            'database': 'PostgreSQL' if database_url else 'SQLite',
            'version': '1.0.0'
        })
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Resource not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    # Create database tables
    with app.app_context():
        try:
            db.create_all()
            print("✅ Database tables created/verified")
        except Exception as e:
            print(f"❌ Database error: {e}")
    
    return app