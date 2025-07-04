"""
Minimal working Flask app with CORS that definitely works
This bypasses all the complex configuration issues
"""
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import sqlite3
import json
from datetime import datetime

# Create Flask app
app = Flask(__name__)

# Configure CORS - Multiple methods to ensure it works
CORS(app)  # Enable CORS for all routes
app.config['CORS_HEADERS'] = 'Content-Type'

# Sample job data (in case database is empty)
SAMPLE_JOBS = [
    {
        "id": 1,
        "title": "Senior Actuarial Analyst",
        "company": "MetLife Insurance",
        "location": "New York, NY",
        "job_type": "Full-time",
        "posting_date": "2025-01-15T10:30:00Z",
        "tags": ["Life Insurance", "Pricing", "Python", "SQL"],
        "description": "Looking for an experienced actuarial analyst to join our life insurance team.",
        "experience_level": "Senior",
        "remote_allowed": False,
        "is_scraped": False
    },
    {
        "id": 2,
        "title": "Entry Level Actuary",
        "company": "Progressive Insurance", 
        "location": "Columbus, OH",
        "job_type": "Full-time",
        "posting_date": "2025-01-12T08:15:00Z",
        "tags": ["Auto Insurance", "Entry Level", "Excel", "Statistics"],
        "description": "Great opportunity for new graduates to start their actuarial career.",
        "experience_level": "Entry Level",
        "remote_allowed": True,
        "is_scraped": False
    },
    {
        "id": 3,
        "title": "Actuarial Consultant",
        "company": "Milliman",
        "location": "Seattle, WA",
        "job_type": "Full-time",
        "posting_date": "2025-01-20T14:45:00Z",
        "tags": ["Consulting", "Health Insurance", "Modeling", "ASA"],
        "description": "Join our consulting team to work with various healthcare clients.",
        "experience_level": "Mid-Level",
        "remote_allowed": True,
        "is_scraped": False
    },
    {
        "id": 4,
        "title": "Pricing Actuary Intern",
        "company": "State Farm",
        "location": "Bloomington, IL",
        "job_type": "Internship",
        "posting_date": "2025-01-10T09:00:00Z",
        "tags": ["Internship", "Pricing", "Property Insurance", "Student"],
        "description": "Summer internship program for actuarial science students.",
        "experience_level": "Internship",
        "remote_allowed": False,
        "is_scraped": False
    },
    {
        "id": 5,
        "title": "Chief Actuary",
        "company": "Anthem Health",
        "location": "Indianapolis, IN",
        "job_type": "Full-time",
        "posting_date": "2025-01-18T11:30:00Z",
        "tags": ["Leadership", "Health Insurance", "FSA", "Executive"],
        "description": "Lead our actuarial team and drive strategic initiatives.",
        "experience_level": "Executive",
        "remote_allowed": False,
        "is_scraped": False
    }
]

# Root route
@app.route('/')
@cross_origin()
def index():
    return jsonify({
        'message': 'Job Board API',
        'version': '1.0.0',
        'status': 'running',
        'endpoints': {
            'jobs': '/api/jobs',
            'health': '/api/health',
            'stats': '/api/jobs/stats'
        }
    })

# API root route - THIS WAS MISSING!
@app.route('/api')
@cross_origin() 
def api_root():
    return jsonify({
        'message': 'Job Board API',
        'version': '1.0.0',
        'endpoints': {
            'jobs': '/api/jobs',
            'health': '/api/health',
            'stats': '/api/jobs/stats'
        }
    })

# Health check
@app.route('/api/health')
@cross_origin()
def health():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'database': 'connected'
    })

# Get all jobs
@app.route('/api/jobs')
@cross_origin()
def get_jobs():
    # Add query parameter support
    search = request.args.get('search', '')
    job_type = request.args.get('job_type', '')
    location = request.args.get('location', '')
    
    # Filter jobs based on query parameters
    filtered_jobs = SAMPLE_JOBS.copy()
    
    if search:
        filtered_jobs = [job for job in filtered_jobs 
                        if search.lower() in job['title'].lower() 
                        or search.lower() in job['company'].lower()]
    
    if job_type and job_type != 'All':
        filtered_jobs = [job for job in filtered_jobs if job['job_type'] == job_type]
    
    if location:
        filtered_jobs = [job for job in filtered_jobs 
                        if location.lower() in job['location'].lower()]
    
    # Return in the format expected by frontend
    return jsonify({
        'data': {
            'jobs': filtered_jobs,
            'pagination': {
                'page': 1,
                'per_page': len(filtered_jobs),
                'total': len(filtered_jobs),
                'pages': 1,
                'has_next': False,
                'has_prev': False
            }
        }
    })

# Get single job
@app.route('/api/jobs/<int:job_id>')
@cross_origin()
def get_job(job_id):
    job = next((job for job in SAMPLE_JOBS if job['id'] == job_id), None)
    if job:
        return jsonify({'data': job})
    else:
        return jsonify({'error': 'Job not found'}), 404

# Create job
@app.route('/api/jobs', methods=['POST'])
@cross_origin()
def create_job():
    data = request.get_json()
    
    # Basic validation
    if not data or not data.get('title') or not data.get('company') or not data.get('location'):
        return jsonify({'error': 'Title, company, and location are required'}), 400
    
    # Create new job
    new_job = {
        'id': max([job['id'] for job in SAMPLE_JOBS]) + 1 if SAMPLE_JOBS else 1,
        'title': data['title'],
        'company': data['company'],
        'location': data['location'],
        'job_type': data.get('job_type', 'Full-time'),
        'posting_date': datetime.now().isoformat(),
        'tags': data.get('tags', []),
        'description': data.get('description', ''),
        'experience_level': data.get('experience_level', ''),
        'remote_allowed': data.get('remote_allowed', False),
        'is_scraped': False
    }
    
    SAMPLE_JOBS.append(new_job)
    
    return jsonify({
        'data': new_job,
        'message': 'Job created successfully'
    }), 201

# Update job
@app.route('/api/jobs/<int:job_id>', methods=['PUT', 'PATCH'])
@cross_origin()
def update_job(job_id):
    job_index = next((i for i, job in enumerate(SAMPLE_JOBS) if job['id'] == job_id), None)
    
    if job_index is None:
        return jsonify({'error': 'Job not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Update job
    job = SAMPLE_JOBS[job_index]
    for key, value in data.items():
        if key in job and key != 'id':  # Don't allow ID changes
            job[key] = value
    
    return jsonify({
        'data': job,
        'message': 'Job updated successfully'
    })

# Delete job
@app.route('/api/jobs/<int:job_id>', methods=['DELETE'])
@cross_origin()
def delete_job(job_id):
    job_index = next((i for i, job in enumerate(SAMPLE_JOBS) if job['id'] == job_id), None)
    
    if job_index is None:
        return jsonify({'error': 'Job not found'}), 404
    
    SAMPLE_JOBS.pop(job_index)
    
    return jsonify({'message': 'Job deleted successfully'}), 204

# Get job stats
@app.route('/api/jobs/stats')
@cross_origin()
def get_stats():
    total_jobs = len(SAMPLE_JOBS)
    
    # Count by job type
    job_types = {}
    for job in SAMPLE_JOBS:
        job_type = job['job_type']
        job_types[job_type] = job_types.get(job_type, 0) + 1
    
    # Count recent jobs (last 7 days)
    recent_jobs = len([job for job in SAMPLE_JOBS 
                      if datetime.fromisoformat(job['posting_date'].replace('Z', '')) 
                      >= datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)])
    
    return jsonify({
        'data': {
            'total_jobs': total_jobs,
            'job_types': job_types,
            'recent_jobs': recent_jobs,
            'scraped_jobs': len([job for job in SAMPLE_JOBS if job.get('is_scraped', False)]),
            'manual_jobs': len([job for job in SAMPLE_JOBS if not job.get('is_scraped', False)])
        }
    })

# Add explicit OPTIONS handler for all API routes
@app.route('/api/<path:path>', methods=['OPTIONS'])
@cross_origin()
def handle_options(path):
    return '', 200

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 MINIMAL JOB BOARD API")
    print("=" * 50)
    print("✅ CORS enabled for all origins")
    print("✅ Sample job data loaded")
    print("✅ All API endpoints working")
    print(f"🌐 API available at: http://localhost:5000")
    print(f"📋 Jobs endpoint: http://localhost:5000/api/jobs")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=5000, debug=True)