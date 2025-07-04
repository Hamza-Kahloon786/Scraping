"""
Quick CORS fix for the Flask backend
This will update your Flask app to allow frontend connections
"""
import os

def create_env_file():
    """Create .env file with proper CORS settings"""
    env_content = """# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=dev-secret-key-change-me

# CORS Configuration - Allow frontend to connect
CORS_ORIGINS=http://localhost:3000

# Database Configuration
DATABASE_URL=sqlite:///jobboard.db

# App Settings
JOBS_PER_PAGE=20
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ Created .env file with CORS configuration")
        return True
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False

def update_app_init():
    """Update the Flask app initialization to fix CORS"""
    app_init_file = os.path.join('app', '__init__.py')
    
    if not os.path.exists(app_init_file):
        print(f"❌ {app_init_file} not found")
        return False
    
    try:
        with open(app_init_file, 'r') as f:
            content = f.read()
        
        # Check if CORS is already properly configured
        if "CORS(app, origins=" in content:
            print("✅ CORS already configured in __init__.py")
            return True
        
        # Update CORS configuration
        if "CORS(app, origins=app.config['CORS_ORIGINS'])" not in content:
            # Replace the basic CORS line
            content = content.replace(
                "CORS(app, origins=app.config['CORS_ORIGINS'])",
                "CORS(app, origins=['http://localhost:3000'], supports_credentials=True)"
            )
            
            # If that didn't work, try a different approach
            if "CORS(app)" in content:
                content = content.replace(
                    "CORS(app)",
                    "CORS(app, origins=['http://localhost:3000'], supports_credentials=True)"
                )
        
        with open(app_init_file, 'w') as f:
            f.write(content)
        
        print("✅ Updated CORS configuration in __init__.py")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {app_init_file}: {e}")
        return False

def create_simple_flask_app():
    """Create a simple Flask app with proper CORS"""
    app_content = '''"""
Flask application factory and initialization with CORS fix
"""
from flask import Flask, jsonify
from flask_cors import CORS
import os

def create_app(config_name=None):
    """Create and configure Flask application"""
    
    app = Flask(__name__)
    
    # Basic configuration
    app.config['SECRET_KEY'] = 'dev-secret-key-change-me'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobboard.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = True
    
    # Initialize extensions
    from app.models import db
    db.init_app(app)
    
    # Configure CORS - THIS IS THE KEY FIX
    CORS(app, 
         origins=['http://localhost:3000'],  # Allow frontend
         supports_credentials=True,
         allow_headers=['Content-Type', 'Authorization'],
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
    
    # Register blueprints
    from app.routes import api
    app.register_blueprint(api)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found'}), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({'error': 'Method not allowed'}), 405
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    # Root route
    @app.route('/')
    def index():
        return jsonify({
            'message': 'Job Board API',
            'version': '1.0.0',
            'endpoints': {
                'jobs': '/api/jobs',
                'health': '/api/health',
                'stats': '/api/jobs/stats'
            }
        })
    
    # Create database tables
    with app.app_context():
        try:
            db.create_all()
            print("✅ Database tables created successfully!")
        except Exception as e:
            print(f"❌ Error creating database tables: {e}")
    
    return app
'''
    
    try:
        os.makedirs('app', exist_ok=True)
        with open(os.path.join('app', '__init__.py'), 'w') as f:
            f.write(app_content)
        print("✅ Created CORS-fixed __init__.py")
        return True
    except Exception as e:
        print(f"❌ Error creating __init__.py: {e}")
        return False

def main():
    """Main fix function"""
    print("🔧 CORS Fix for Job Board Backend")
    print("=" * 40)
    
    # Step 1: Create .env file
    print("1. Creating .env file...")
    create_env_file()
    
    # Step 2: Update Flask app
    print("2. Fixing Flask CORS configuration...")
    if not update_app_init():
        print("🔄 Creating new Flask app with CORS fix...")
        create_simple_flask_app()
    
    print("\n✅ CORS fix completed!")
    print("🚀 Now restart your backend:")
    print("   1. Stop the current backend (Ctrl+C)")
    print("   2. Run: python run.py")
    print("   3. Restart your frontend if needed")
    print("\nThe frontend should now connect successfully! 🎉")

if __name__ == "__main__":
    main()