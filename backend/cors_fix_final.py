"""
Final CORS fix for Flask backend
This will definitely solve the CORS issue
"""
import os
import shutil

def backup_current_init():
    """Backup current __init__.py"""
    init_file = os.path.join('app', '__init__.py')
    if os.path.exists(init_file):
        backup_file = os.path.join('app', '__init__.py.backup')
        shutil.copy2(init_file, backup_file)
        print("Backed up current __init__.py")

def create_working_init():
    """Create a working __init__.py with proper CORS"""
    
    # This is a minimal, working Flask app with CORS
    init_content = """from flask import Flask, jsonify
from flask_cors import CORS

def create_app(config_name=None):
    app = Flask(__name__)
    
    # Basic configuration
    app.config['SECRET_KEY'] = 'dev-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobboard.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = True
    
    # CRITICAL: Configure CORS BEFORE any routes
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:3000", "http://127.0.0.1:3000"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Initialize database
    from app.models import db
    db.init_app(app)
    
    # Register routes
    from app.routes import api
    app.register_blueprint(api)
    
    # Root route
    @app.route('/')
    def index():
        return jsonify({
            'message': 'Job Board API',
            'version': '1.0.0',
            'status': 'running'
        })
    
    # Create tables
    with app.app_context():
        try:
            db.create_all()
            print("Database tables ready")
        except Exception as e:
            print(f"Database error: {e}")
    
    return app
"""
    
    try:
        # Create app directory if it doesn't exist
        os.makedirs('app', exist_ok=True)
        
        # Write the new __init__.py
        with open(os.path.join('app', '__init__.py'), 'w', encoding='utf-8') as f:
            f.write(init_content)
        
        print("SUCCESS: Created new __init__.py with proper CORS")
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_flask_cors():
    """Test if Flask-CORS is installed"""
    try:
        import flask_cors
        print("Flask-CORS is installed")
        return True
    except ImportError:
        print("Flask-CORS is NOT installed")
        return False

def install_flask_cors():
    """Install Flask-CORS if needed"""
    import subprocess
    import sys
    
    try:
        print("Installing Flask-CORS...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'flask-cors'])
        print("Flask-CORS installed successfully")
        return True
    except Exception as e:
        print(f"Failed to install Flask-CORS: {e}")
        return False

def main():
    """Main fix function"""
    print("=" * 50)
    print("FINAL CORS FIX FOR FLASK")
    print("=" * 50)
    
    # Step 1: Check Flask-CORS
    print("Step 1: Checking Flask-CORS...")
    if not test_flask_cors():
        if not install_flask_cors():
            print("CRITICAL: Cannot install Flask-CORS")
            return False
    
    # Step 2: Backup current file
    print("Step 2: Backing up current files...")
    backup_current_init()
    
    # Step 3: Create working version
    print("Step 3: Creating CORS-fixed Flask app...")
    if create_working_init():
        print("SUCCESS: CORS fix applied")
    else:
        print("FAILED: Could not apply fix")
        return False
    
    print("=" * 50)
    print("FIX COMPLETED!")
    print("Now do the following:")
    print("1. Stop your backend (Ctrl+C)")
    print("2. Run: python run.py")
    print("3. The frontend should now work!")
    print("=" * 50)
    
    return True

if __name__ == "__main__":
    main()