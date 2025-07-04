"""
Database models for the Job Board application
"""
from datetime import datetime, UTC
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, post_load

db = SQLAlchemy()

class Job(db.Model):
    """Job model representing a job posting"""
    
    __tablename__ = 'jobs'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Required fields
    title = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    
    # Date fields - FIXED: Using timezone-aware datetime
    posting_date = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(UTC))
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(UTC))
    updated_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))
    
    # Job details
    job_type = db.Column(db.String(50), nullable=False, default='Full-time')
    tags = db.Column(db.Text)  # Stored as comma-separated string
    
    # Optional fields
    description = db.Column(db.Text)
    salary_range = db.Column(db.String(100))
    experience_level = db.Column(db.String(50))
    remote_allowed = db.Column(db.Boolean, default=False)
    
    # Source tracking (for scraped jobs)
    source_url = db.Column(db.String(500))
    is_scraped = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<Job {self.id}: {self.title} at {self.company}>'
    
    def get_tags_list(self):
        """Convert comma-separated tags string to list"""
        if not self.tags:
            return []
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
    
    def set_tags_from_list(self, tags_list):
        """Convert list of tags to comma-separated string"""
        if tags_list:
            self.tags = ', '.join([tag.strip() for tag in tags_list if tag.strip()])
        else:
            self.tags = None
    
    def to_dict(self):
        """Convert job instance to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'company': self.company,
            'location': self.location,
            'posting_date': self.posting_date.isoformat() if self.posting_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'job_type': self.job_type,
            'tags': self.tags,  # Keep as string for API consistency
            'tags_list': self.get_tags_list(),  # Provide list version too
            'description': self.description,
            'salary_range': self.salary_range,
            'experience_level': self.experience_level,
            'remote_allowed': self.remote_allowed,
            'source_url': self.source_url,
            'is_scraped': self.is_scraped
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create Job instance from dictionary"""
        # Create a copy to avoid modifying original data
        job_data = data.copy()
        
        # Handle tags conversion
        if 'tags' in job_data and isinstance(job_data['tags'], list):
            tags_list = job_data.pop('tags')
            job = cls(**job_data)
            job.set_tags_from_list(tags_list)
            return job
        
        # Handle posting_date conversion
        if 'posting_date' in job_data and isinstance(job_data['posting_date'], str):
            try:
                job_data['posting_date'] = datetime.fromisoformat(job_data['posting_date'].replace('Z', '+00:00'))
            except (ValueError, AttributeError):
                # If parsing fails, use current time
                job_data['posting_date'] = datetime.now(UTC)
        
        return cls(**job_data)
    
    def update_from_dict(self, data):
        """Update job instance from dictionary"""
        # Fields that can be updated
        updatable_fields = [
            'title', 'company', 'location', 'job_type', 'description',
            'salary_range', 'experience_level', 'remote_allowed', 'source_url'
        ]
        
        for field in updatable_fields:
            if field in data:
                setattr(self, field, data[field])
        
        # Handle tags specially
        if 'tags' in data:
            if isinstance(data['tags'], list):
                self.set_tags_from_list(data['tags'])
            else:
                self.tags = data['tags']
        
        # Update timestamp
        self.updated_at = datetime.now(UTC)
    
    @staticmethod
    def search_jobs(search_term=None, job_type=None, location=None, 
                   experience_level=None, remote_allowed=None, tags=None):
        """Search jobs with multiple filters"""
        query = Job.query
        
        if search_term:
            search_pattern = f"%{search_term}%"
            query = query.filter(
                db.or_(
                    Job.title.ilike(search_pattern),
                    Job.company.ilike(search_pattern),
                    Job.description.ilike(search_pattern)
                )
            )
        
        if job_type and job_type.lower() != 'all':
            query = query.filter(Job.job_type == job_type)
        
        if location:
            location_pattern = f"%{location}%"
            query = query.filter(Job.location.ilike(location_pattern))
        
        if experience_level and experience_level.lower() != 'all':
            query = query.filter(Job.experience_level == experience_level)
        
        if remote_allowed is not None and str(remote_allowed).lower() != 'all':
            if isinstance(remote_allowed, str):
                remote_allowed = remote_allowed.lower() == 'true'
            query = query.filter(Job.remote_allowed == remote_allowed)
        
        if tags:
            if isinstance(tags, str):
                tags = [tag.strip() for tag in tags.split(',')]
            for tag in tags:
                if tag.strip():
                    tag_pattern = f"%{tag.strip()}%"
                    query = query.filter(Job.tags.ilike(tag_pattern))
        
        return query.order_by(Job.posting_date.desc())

class JobSchema(Schema):
    """Schema for serializing/deserializing Job objects"""
    
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    company = fields.Str(required=True)
    location = fields.Str(required=True)
    posting_date = fields.DateTime()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    job_type = fields.Str()
    tags = fields.Raw()  # Can be string or list
    tags_list = fields.List(fields.Str(), dump_only=True)
    description = fields.Str()
    salary_range = fields.Str()
    experience_level = fields.Str()
    remote_allowed = fields.Bool()
    source_url = fields.Str()
    is_scraped = fields.Bool(dump_only=True)
    
    @post_load
    def make_job(self, data, **kwargs):
        """Create Job instance from deserialized data"""
        return Job.from_dict(data)

# Schema instances for reuse
job_schema = JobSchema()
jobs_schema = JobSchema(many=True)

# Utility functions for database operations
class JobService:
    """Service class for job-related database operations"""
    
    @staticmethod
    def get_all_jobs(filters=None):
        """Get all jobs with optional filters"""
        if not filters:
            return Job.query.order_by(Job.posting_date.desc()).all()
        
        return Job.search_jobs(
            search_term=filters.get('search'),
            job_type=filters.get('job_type'),
            location=filters.get('location'),
            experience_level=filters.get('experience_level'),
            remote_allowed=filters.get('remote_allowed'),
            tags=filters.get('tags')
        ).all()
    
    @staticmethod
    def get_job_by_id(job_id):
        """Get job by ID"""
        return Job.query.get(job_id)
    
    @staticmethod
    def create_job(job_data):
        """Create new job"""
        job = Job.from_dict(job_data)
        db.session.add(job)
        db.session.commit()
        return job
    
    @staticmethod
    def update_job(job_id, job_data):
        """Update existing job"""
        job = Job.query.get(job_id)
        if not job:
            return None
        
        job.update_from_dict(job_data)
        db.session.commit()
        return job
    
    @staticmethod
    def delete_job(job_id):
        """Delete job by ID"""
        job = Job.query.get(job_id)
        if not job:
            return False
        
        db.session.delete(job)
        db.session.commit()
        return True
    
    @staticmethod
    def get_job_stats():
        """Get job statistics"""
        total_jobs = Job.query.count()
        recent_jobs = Job.query.filter(
            Job.posting_date >= datetime.now(UTC).replace(hour=0, minute=0, second=0, microsecond=0)
        ).count()
        companies = db.session.query(Job.company).distinct().count()
        
        return {
            'total': total_jobs,
            'recent': recent_jobs,
            'companies': companies
        }
    
    @staticmethod
    def get_unique_job_types():
        """Get list of unique job types"""
        result = db.session.query(Job.job_type).distinct().all()
        return [row[0] for row in result if row[0]]
    
    @staticmethod
    def get_unique_experience_levels():
        """Get list of unique experience levels"""
        result = db.session.query(Job.experience_level).distinct().all()
        return [row[0] for row in result if row[0]]