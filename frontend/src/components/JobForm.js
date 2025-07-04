import React, { useState, useEffect } from 'react';

function JobForm({ job, onClose, onSubmit, isEditing = false }) {
  const [formData, setFormData] = useState({
    title: '',
    company: '',
    location: '',
    job_type: 'Full-time',
    description: '',
    experience_level: 'Mid-Level',
    remote_allowed: false,
    tags: '',
    salary_range: '',
    source_url: ''
  });
  
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');

  // Load job data if editing
  useEffect(() => {
    if (isEditing && job) {
      setFormData({
        title: job.title || '',
        company: job.company || '',
        location: job.location || '',
        job_type: job.job_type || 'Full-time',
        description: job.description || '',
        experience_level: job.experience_level || 'Mid-Level',
        remote_allowed: job.remote_allowed || false,
        tags: job.tags || '',
        salary_range: job.salary_range || '',
        source_url: job.source_url || ''
      });
    }
  }, [job, isEditing]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setIsSubmitting(true);
    
    try {
      if (isEditing) {
        await onSubmit(job.id, formData);
      } else {
        await onSubmit(formData);
      }
    } catch (err) {
      setError(err.message || `Failed to ${isEditing ? 'update' : 'add'} job. Please try again.`);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  return (
    <div className="modal-overlay" onClick={(e) => e.target === e.currentTarget && onClose()}>
      <div className="modal">
        <div className="modal-header">
          <h2>
            {isEditing ? (
              <>✏️ Edit Job: {job?.title}</>
            ) : (
              <>➕ Add New Job Listing</>
            )}
          </h2>
          <button onClick={onClose} className="close-btn" type="button">✕</button>
        </div>

        {error && (
          <div className="error-message">
            ⚠️ {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="job-form">
          <div className="form-row">
            <div className="form-group">
              <label>Job Title *</label>
              <input
                type="text"
                name="title"
                value={formData.title}
                onChange={handleChange}
                placeholder="e.g., Senior Actuarial Analyst"
                required
                disabled={isSubmitting}
              />
            </div>
            <div className="form-group">
              <label>Company *</label>
              <input
                type="text"
                name="company"
                value={formData.company}
                onChange={handleChange}
                placeholder="e.g., Northwestern Mutual"
                required
                disabled={isSubmitting}
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Location *</label>
              <input
                type="text"
                name="location"
                value={formData.location}
                onChange={handleChange}
                placeholder="e.g., Milwaukee, WI"
                required
                disabled={isSubmitting}
              />
            </div>
            <div className="form-group">
              <label>Job Type</label>
              <select name="job_type" value={formData.job_type} onChange={handleChange} disabled={isSubmitting}>
                <option value="Full-time">Full-time</option>
                <option value="Part-time">Part-time</option>
                <option value="Contract">Contract</option>
                <option value="Internship">Internship</option>
              </select>
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Experience Level</label>
              <select name="experience_level" value={formData.experience_level} onChange={handleChange} disabled={isSubmitting}>
                <option value="Entry Level">Entry Level</option>
                <option value="Mid-Level">Mid-Level</option>
                <option value="Senior">Senior</option>
                <option value="Executive">Executive</option>
                <option value="Internship">Internship</option>
              </select>
            </div>
            <div className="form-group">
              <label>Salary Range</label>
              <input
                type="text"
                name="salary_range"
                value={formData.salary_range}
                onChange={handleChange}
                placeholder="e.g., $80,000 - $120,000"
                disabled={isSubmitting}
              />
            </div>
          </div>

          <div className="form-group">
            <label>Job Description *</label>
            <textarea
              name="description"
              value={formData.description}
              onChange={handleChange}
              rows="4"
              placeholder="Describe the role, responsibilities, and requirements..."
              required
              disabled={isSubmitting}
            />
          </div>

          <div className="form-group">
            <label>Skills & Tags</label>
            <input
              type="text"
              name="tags"
              value={formData.tags}
              onChange={handleChange}
              placeholder="e.g., Python, Excel, ASA, Life Insurance"
              disabled={isSubmitting}
            />
            <small>Separate multiple tags with commas</small>
          </div>

          <div className="form-group">
            <label>Source URL (Optional)</label>
            <input
              type="url"
              name="source_url"
              value={formData.source_url}
              onChange={handleChange}
              placeholder="https://company.com/careers/job-id"
              disabled={isSubmitting}
            />
          </div>

          <div className="form-group">
            <label className="checkbox-label">
              <input
                type="checkbox"
                name="remote_allowed"
                checked={formData.remote_allowed}
                onChange={handleChange}
                disabled={isSubmitting}
              />
              🏠 Remote work allowed
            </label>
          </div>

          <div className="form-actions">
            <button 
              type="button" 
              onClick={onClose} 
              className="cancel-btn"
              disabled={isSubmitting}
            >
              Cancel
            </button>
            <button 
              type="submit" 
              className="submit-btn"
              disabled={isSubmitting}
            >
              {isSubmitting ? (
                isEditing ? '⏳ Updating Job...' : '⏳ Adding Job...'
              ) : (
                isEditing ? '✅ Update Job' : '✅ Add Job'
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default JobForm;