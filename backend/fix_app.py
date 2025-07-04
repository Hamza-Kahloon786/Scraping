"""
Windows-compatible fix for Flask app CORS issue
No special characters that cause encoding problems
"""
import os

def fix_init_file():
    """Create a working __init__.py file"""
    
    init_content = '''"""
Flask application factory and initialization
"""
from flask import Flask, jsonify
from flask_cors import CORS
import os

def create_app(config_name=None):
    """Create and configure Flask application"""
    
    app = Flask(__name__)
    
    # Load configuration
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    if config_name == 'development':
        from config import DevelopmentConfig
        app.config.from_object(DevelopmentConfig)
    elif config_name == 'production':
        from config import ProductionConfig
        app.config.from_object(ProductionConfig)
    elif config_name == 'testing':
        from config import TestingConfig
        app.config.from_object(TestingConfig)
    else:
        from config import DevelopmentConfig
        app.config.from_object(DevelopmentConfig)
    
    # Initialize extensions
    from app.models import db
    db.init_app(app)
    
    # Configure CORS to allow frontend connections
    CORS(app, 
         origins=['http://localhost:3000', 'http://127.0.0.1:3000'],
         supports_credentials=True,
         allow_headers=['Content-Type', 'Authorization'],
         methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'])
    
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
            print("Database tables created successfully!")
        except Exception as e:
            print("Error creating database tables:", str(e))
    
    return app
'''
    
    try:
        # Make sure app directory exists
        if not os.path.exists('app'):
            os.makedirs('app')
        
        # Write the file with proper encoding
        with open(os.path.join('app', '__init__.py'), 'w', encoding='utf-8') as f:
            f.write(init_content)
        
        print("SUCCESS: Fixed app/__init__.py")
        return True
        
    except Exception as e:
        print("ERROR: Could not fix __init__.py -", str(e))
        return False

def create_env():
    """Create .env file"""
    env_content = '''FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=dev-secret-key-change-me
CORS_ORIGINS=http://localhost:3000
DATABASE_URL=sqlite:///jobboard.db
JOBS_PER_PAGE=20
'''
    
    try:
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("SUCCESS: Created .env file")
        return True
    except Exception as e:
        print("ERROR: Could not create .env file -", str(e))
        return False

def main():
    """Main fix function"""
    print("=" * 40)
    print("Flask CORS Fix for Windows")
    print("=" * 40)
    
    print("Step 1: Creating .env file...")
    create_env()
    
    print("Step 2: Fixing app/__init__.py...")
    fix_init_file()
    
    print("=" * 40)
    print("Fix completed!")
    print("Now run: python run.py")
    print("=" * 40)

if __name__ == "__main__":
    main()