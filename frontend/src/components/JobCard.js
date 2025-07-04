import React, { useState } from 'react';

function JobCard({ job, onUpdate, onDelete }) {
  const [showActions, setShowActions] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString();
  };

  const handleDelete = async () => {
    if (window.confirm(`Are you sure you want to delete "${job.title}" at ${job.company}?`)) {
      setIsDeleting(true);
      try {
        await onDelete(job.id);
      } catch (error) {
        console.error('Error deleting job:', error);
      } finally {
        setIsDeleting(false);
      }
    }
  };

  const handleEdit = () => {
    onUpdate(job);
  };

  return (
    <div className="job-card" onMouseEnter={() => setShowActions(true)} onMouseLeave={() => setShowActions(false)}>
      {/* Job Actions */}
      {showActions && (
        <div className="job-actions">
          <button 
            onClick={handleEdit}
            className="action-btn edit-btn"
            title="Edit Job"
          >
            ✏️
          </button>
          <button 
            onClick={handleDelete}
            className="action-btn delete-btn"
            title="Delete Job"
            disabled={isDeleting}
          >
            {isDeleting ? '⏳' : '🗑️'}
          </button>
        </div>
      )}

      <div className="job-header">
        <h3 className="job-title">{job.title}</h3>
        <div className="job-meta">
          <span className="company">🏢 {job.company}</span>
          <span className="location">📍 {job.location}</span>
        </div>
      </div>

      <div className="job-details">
        <div className="job-type-badge">{job.job_type}</div>
        {job.remote_allowed && <div className="remote-badge">🏠 Remote OK</div>}
        {job.salary_range && <div className="salary-badge">💰 {job.salary_range}</div>}
      </div>

      <p className="job-description">{job.description}</p>

      {job.tags && (
        <div className="job-tags">
          {job.tags.split(',').map((tag, index) => (
            <span key={index} className="tag">{tag.trim()}</span>
          ))}
        </div>
      )}

      <div className="job-footer">
        <span className="post-date">Posted: {formatDate(job.posting_date)}</span>
        <span className="experience-level">{job.experience_level}</span>
      </div>

      {job.source_url && (
        <div className="job-link">
          <a href={job.source_url} target="_blank" rel="noopener noreferrer" className="source-link">
            🔗 View Original
          </a>
        </div>
      )}
    </div>
  );
}

export default JobCard;