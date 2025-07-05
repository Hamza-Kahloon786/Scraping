import React, { useState, useEffect } from 'react';
import { jobAPI } from './services/api';
import './App.css';

function App() {
  const [jobs, setJobs] = useState([]);
  const [filteredJobs, setFilteredJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showAddForm, setShowAddForm] = useState(false);
  const [editingJob, setEditingJob] = useState(null);
  const [notification, setNotification] = useState(null);
  
  // Filter states
  const [searchTerm, setSearchTerm] = useState('');
  const [jobTypeFilter, setJobTypeFilter] = useState('');
  const [locationFilter, setLocationFilter] = useState('');

  // Show notification helper
  const showNotification = (message, type = 'success') => {
    setNotification({ message, type });
    setTimeout(() => setNotification(null), 5000);
  };

  // Load jobs when component mounts
  useEffect(() => {
    loadJobs();
  }, []);

  // Filter jobs when search criteria change
  useEffect(() => {
    filterJobs();
  }, [jobs, searchTerm, jobTypeFilter, locationFilter]);

  const loadJobs = async () => {
    try {
      setLoading(true);
      setError(null);
      const jobsData = await jobAPI.getAllJobs();
      setJobs(jobsData);
    } catch (err) {
      setError('Failed to load jobs. Make sure your backend is running on http://localhost:5000');
      console.error('Error loading jobs:', err);
    } finally {
      setLoading(false);
    }
  };

  const filterJobs = () => {
    let filtered = jobs;

    if (searchTerm) {
      filtered = filtered.filter(job =>
        job.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        job.company.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    if (jobTypeFilter) {
      filtered = filtered.filter(job => job.job_type === jobTypeFilter);
    }

    if (locationFilter) {
      filtered = filtered.filter(job =>
        job.location.toLowerCase().includes(locationFilter.toLowerCase())
      );
    }

    setFilteredJobs(filtered);
  };

  const handleAddJob = async (jobData) => {
    try {
      console.log('Adding job:', jobData);
      await jobAPI.addJob(jobData);
      setShowAddForm(false);
      await loadJobs(); // Reload jobs to show the new one
      showNotification(`✅ Job "${jobData.title}" added successfully!`, 'success');
    } catch (err) {
      console.error('Error adding job:', err);
      showNotification(`❌ Failed to add job: ${err.message}`, 'error');
    }
  };

  const handleUpdateJob = async (jobId, jobData) => {
    try {
      await jobAPI.updateJob(jobId, jobData);
      setEditingJob(null);
      await loadJobs(); // Reload jobs to show updates
      showNotification(`✅ Job "${jobData.title}" updated successfully!`, 'success');
    } catch (err) {
      console.error('Error updating job:', err);
      showNotification(`❌ Failed to update job: ${err.message}`, 'error');
    }
  };

  const handleDeleteJob = async (jobId) => {
    try {
      await jobAPI.deleteJob(jobId);
      await loadJobs(); // Reload jobs to remove deleted one
      showNotification(`✅ Job deleted successfully!`, 'success');
    } catch (err) {
      console.error('Error deleting job:', err);
      showNotification(`❌ Failed to delete job: ${err.message}`, 'error');
    }
  };

  const triggerScraper = async () => {
    try {
      setLoading(true);
      const result = await jobAPI.triggerScraper();
      await loadJobs(); // Reload jobs after scraping
      showNotification(`✅ Scraper completed! Added ${result.jobs_saved} new jobs, skipped ${result.jobs_skipped} duplicates.`, 'success');
    } catch (err) {
      console.error('Error running scraper:', err);
      showNotification(`❌ Scraper failed: ${err.message}`, 'error');
    } finally {
      setLoading(false);
    }
  };

  const clearFilters = () => {
    setSearchTerm('');
    setJobTypeFilter('');
    setLocationFilter('');
  };

  const getUniqueJobTypes = () => {
    const types = jobs.map(job => job.job_type).filter(Boolean);
    return [...new Set(types)];
  };

  if (loading) {
    return (
      <div className="app">
        <div className="loading">
          <div className="spinner"></div>
          <p>Loading jobs...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      {/* Notification */}
      {notification && (
        <div className={`notification ${notification.type}`}>
          <span>{notification.message}</span>
          <button onClick={() => setNotification(null)} className="notification-close">✕</button>
        </div>
      )}

      {/* Header */}
      <header className="header">
        <div className="header-content">
          <div className="logo">
            📊 ActuaryJobs
          </div>
          <div className="header-stats">
            <span className="job-count">{jobs.length} Jobs</span>
            <button 
              className="add-job-btn"
              onClick={() => {
                console.log('Add Job button clicked!');
                setShowAddForm(true);
              }}
              title="Add New Job Listing"
            >
              <span className="btn-icon">➕</span>
              <span className="btn-text">Add Job</span>
            </button>
            <button 
              className="scraper-btn"
              onClick={triggerScraper}
              disabled={loading}
              title="Scrape Jobs from ActuaryList.com"
            >
              <span className="btn-icon">{loading ? '⏳' : '🔍'}</span>
              <span className="btn-text">{loading ? 'Scraping...' : 'Scrape Jobs'}</span>
            </button>
          </div>
        </div>
      </header>

      {/* Error Message */}
      {error && (
        <div className="error-banner">
          ⚠️ {error}
          <button onClick={loadJobs} className="retry-btn">Retry</button>
        </div>
      )}

      {/* Search and Filters */}
      <div className="filters-section">
        <div className="filters-container">
          <div className="search-group">
            <label>Search Jobs</label>
            <div className="search-input">
              <input
                type="text"
                placeholder="Search by title or company..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
          </div>

          <div className="filter-group">
            <label>Job Type</label>
            <select
              value={jobTypeFilter}
              onChange={(e) => setJobTypeFilter(e.target.value)}
            >
              <option value="">All Job Types</option>
              {getUniqueJobTypes().map(type => (
                <option key={type} value={type}>{type}</option>
              ))}
            </select>
          </div>

          <div className="filter-group">
            <label>Location</label>
            <input
              type="text"
              placeholder="Enter location..."
              value={locationFilter}
              onChange={(e) => setLocationFilter(e.target.value)}
            />
          </div>

          <button className="filter-btn" onClick={filterJobs}>
            🔍 Filter
          </button>
        </div>
      </div>

      {/* Results */}
      <main className="main-content">
        {filteredJobs.length === 0 ? (
          <div className="no-jobs">
            <div className="no-jobs-icon">🔍</div>
            <h2>No Jobs Found</h2>
            <p>
              {jobs.length === 0 
                ? "No job listings in database. Try running the scraper to add jobs."
                : "No job listings match your search criteria. Try adjusting your filters."
              }
            </p>
            {jobs.length === 0 ? (
              <button onClick={triggerScraper} className="primary-btn">
                🔍 Scrape Jobs
              </button>
            ) : (
              <button onClick={clearFilters} className="secondary-btn">
                🗑️ Clear Filters
              </button>
            )}
          </div>
        ) : (
          <div className="jobs-grid">
            {filteredJobs.map(job => (
              <JobCard 
                key={job.id} 
                job={job} 
                onUpdate={setEditingJob}
                onDelete={handleDeleteJob}
              />
            ))}
          </div>
        )}
      </main>

      {/* FIXED MODAL - Using same approach as debug version */}
      {showAddForm && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
          backgroundColor: 'rgba(0,0,0,0.8)',
          zIndex: 9999,
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          padding: '20px'
        }}>
          <div style={{
            backgroundColor: 'white',
            borderRadius: '12px',
            width: '100%',
            maxWidth: '600px',
            maxHeight: '90vh',
            overflow: 'auto',
            boxShadow: '0 20px 40px rgba(0,0,0,0.3)'
          }}>
            <AddJobForm
              onClose={() => setShowAddForm(false)}
              onSubmit={handleAddJob}
            />
          </div>
        </div>
      )}

      {/* Edit Job Modal */}
      {editingJob && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
          backgroundColor: 'rgba(0,0,0,0.8)',
          zIndex: 9999,
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          padding: '20px'
        }}>
          <div style={{
            backgroundColor: 'white',
            borderRadius: '12px',
            width: '100%',
            maxWidth: '600px',
            maxHeight: '90vh',
            overflow: 'auto',
            boxShadow: '0 20px 40px rgba(0,0,0,0.3)'
          }}>
            <EditJobForm
              job={editingJob}
              onClose={() => setEditingJob(null)}
              onSubmit={handleUpdateJob}
            />
          </div>
        </div>
      )}
    </div>
  );
}

// Job Card Component
// Clean Job Card Component - Add this to your App.js to replace the existing JobCard

function JobCard({ job, onUpdate, onDelete }) {
  const [showActions, setShowActions] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);

  // Clean up garbled titles and data
  const cleanTitle = (title) => {
    if (!title) return "Actuarial Position";
    
    // Remove common garbled patterns
    let cleaned = title
      .replace(/([a-z])([A-Z])/g, '$1 $2') // Add spaces between camelCase
      .replace(/([A-Z]{2,})/g, ' $1 ') // Space around uppercase sequences
      .replace(/\s+/g, ' ') // Multiple spaces to single
      .replace(/^\w/, c => c.toUpperCase()) // Capitalize first letter
      .trim();
    
    // If still looks garbled (no spaces and very long), try to extract meaningful parts
    if (cleaned.length > 60 && cleaned.split(' ').length < 3) {
      // Try to extract common actuarial terms
      const patterns = [
        /Actuar\w*/i,
        /Analyst/i,
        /Manager/i,
        /Director/i,
        /Senior/i,
        /Principal/i,
        /Associate/i,
        /Consultant/i
      ];
      
      let extractedTerms = [];
      patterns.forEach(pattern => {
        const match = cleaned.match(pattern);
        if (match) {
          extractedTerms.push(match[0]);
        }
      });
      
      if (extractedTerms.length > 0) {
        cleaned = extractedTerms.join(' ');
      } else {
        // Last resort: take first reasonable chunk
        cleaned = cleaned.substring(0, 40) + "...";
      }
    }
    
    return cleaned.length > 80 ? cleaned.substring(0, 80) + "..." : cleaned;
  };

  const cleanCompany = (company) => {
    if (!company) return "Company";
    
    return company
      .replace(/([a-z])([A-Z])/g, '$1 $2')
      .replace(/\s+/g, ' ')
      .trim()
      .substring(0, 50);
  };

  const cleanLocation = (location) => {
    if (!location) return "Various Locations";
    
    return location
      .replace(/([a-z])([A-Z])/g, '$1 $2')
      .replace(/\s+/g, ' ')
      .trim()
      .substring(0, 30);
  };

  const cleanDescription = (description) => {
    if (!description) return "Great actuarial opportunity. Click to learn more.";
    
    return description.length > 200 ? description.substring(0, 200) + "..." : description;
  };

  const formatDate = (dateString) => {
    try {
      return new Date(dateString).toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric'
      });
    } catch {
      return "Recent";
    }
  };

  const formatSalary = (salary) => {
    if (!salary || salary === '') return null;
    return salary.length > 30 ? salary.substring(0, 30) + "..." : salary;
  };

  const handleDelete = async () => {
    if (window.confirm(`Are you sure you want to delete "${cleanTitle(job.title)}" at ${cleanCompany(job.company)}?`)) {
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

  return (
    <div className="job-card" onMouseEnter={() => setShowActions(true)} onMouseLeave={() => setShowActions(false)}>
      {/* Job Actions */}
      {showActions && (
        <div className="job-actions">
          <button 
            onClick={() => onUpdate(job)}
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
        <h3 className="job-title">{cleanTitle(job.title)}</h3>
        <div className="job-meta">
          <span className="company">🏢 {cleanCompany(job.company)}</span>
          <span className="location">📍 {cleanLocation(job.location)}</span>
        </div>
      </div>

      <div className="job-details">
        <div className="job-type-badge">{job.job_type || 'Full-time'}</div>
        {job.remote_allowed && <div className="remote-badge">🏠 Remote OK</div>}
        {formatSalary(job.salary_range) && (
          <div className="salary-badge">💰 {formatSalary(job.salary_range)}</div>
        )}
      </div>

      <p className="job-description">{cleanDescription(job.description)}</p>

      {job.tags && (
        <div className="job-tags">
          {job.tags.split(',').slice(0, 4).map((tag, index) => (
            <span key={index} className="tag">{tag.trim()}</span>
          ))}
        </div>
      )}

      <div className="job-footer">
        <span className="post-date">Posted: {formatDate(job.posting_date)}</span>
        <span className="experience-level">{job.experience_level || 'Mid-Level'}</span>
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

// Add Job Form Component - Using inline styles to prevent CSS conflicts
function AddJobForm({ onClose, onSubmit }) {
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

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setIsSubmitting(true);
    
    try {
      await onSubmit(formData);
    } catch (err) {
      setError(err.message || 'Failed to add job. Please try again.');
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

  const inputStyle = {
    width: '100%',
    padding: '12px',
    marginBottom: '16px',
    border: '2px solid #e2e8f0',
    borderRadius: '8px',
    fontSize: '14px',
    fontFamily: 'inherit',
    transition: 'border-color 0.2s'
  };

  const labelStyle = {
    display: 'block',
    marginBottom: '8px',
    fontWeight: '600',
    color: '#4a5568',
    fontSize: '14px'
  };

  return (
    <div>
      <div style={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center', 
        padding: '24px 24px 0 24px',
        borderBottom: '1px solid #e2e8f0',
        marginBottom: '24px'
      }}>
        <h2 style={{ margin: 0, color: '#2d3748', fontSize: '1.5rem' }}>➕ Add New Job Listing</h2>
        <button 
          onClick={onClose}
          style={{
            background: 'none',
            border: 'none',
            fontSize: '24px',
            cursor: 'pointer',
            color: '#718096',
            padding: '8px',
            borderRadius: '4px'
          }}
        >
          ✕
        </button>
      </div>

      <div style={{ padding: '0 24px 24px 24px' }}>
        {error && (
          <div style={{
            backgroundColor: '#fed7d7',
            color: '#c53030',
            padding: '12px',
            borderRadius: '6px',
            marginBottom: '16px',
            borderLeft: '4px solid #e53e3e'
          }}>
            ⚠️ {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginBottom: '16px' }}>
            <div>
              <label style={labelStyle}>Job Title *</label>
              <input
                type="text"
                name="title"
                value={formData.title}
                onChange={handleChange}
                placeholder="e.g., Senior Actuarial Analyst"
                required
                disabled={isSubmitting}
                style={inputStyle}
              />
            </div>
            <div>
              <label style={labelStyle}>Company *</label>
              <input
                type="text"
                name="company"
                value={formData.company}
                onChange={handleChange}
                placeholder="e.g., Northwestern Mutual"
                required
                disabled={isSubmitting}
                style={inputStyle}
              />
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginBottom: '16px' }}>
            <div>
              <label style={labelStyle}>Location *</label>
              <input
                type="text"
                name="location"
                value={formData.location}
                onChange={handleChange}
                placeholder="e.g., Milwaukee, WI"
                required
                disabled={isSubmitting}
                style={inputStyle}
              />
            </div>
            <div>
              <label style={labelStyle}>Job Type</label>
              <select 
                name="job_type" 
                value={formData.job_type} 
                onChange={handleChange} 
                disabled={isSubmitting}
                style={inputStyle}
              >
                <option value="Full-time">Full-time</option>
                <option value="Part-time">Part-time</option>
                <option value="Contract">Contract</option>
                <option value="Internship">Internship</option>
              </select>
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginBottom: '16px' }}>
            <div>
              <label style={labelStyle}>Experience Level</label>
              <select 
                name="experience_level" 
                value={formData.experience_level} 
                onChange={handleChange} 
                disabled={isSubmitting}
                style={inputStyle}
              >
                <option value="Entry Level">Entry Level</option>
                <option value="Mid-Level">Mid-Level</option>
                <option value="Senior">Senior</option>
                <option value="Executive">Executive</option>
                <option value="Internship">Internship</option>
              </select>
            </div>
            <div>
              <label style={labelStyle}>Salary Range</label>
              <input
                type="text"
                name="salary_range"
                value={formData.salary_range}
                onChange={handleChange}
                placeholder="e.g., $80,000 - $120,000"
                disabled={isSubmitting}
                style={inputStyle}
              />
            </div>
          </div>

          <div style={{ marginBottom: '16px' }}>
            <label style={labelStyle}>Job Description *</label>
            <textarea
              name="description"
              value={formData.description}
              onChange={handleChange}
              rows="4"
              placeholder="Describe the role, responsibilities, and requirements..."
              required
              disabled={isSubmitting}
              style={{...inputStyle, height: '100px', resize: 'vertical'}}
            />
          </div>

          <div style={{ marginBottom: '16px' }}>
            <label style={labelStyle}>Skills & Tags</label>
            <input
              type="text"
              name="tags"
              value={formData.tags}
              onChange={handleChange}
              placeholder="e.g., Python, Excel, ASA, Life Insurance"
              disabled={isSubmitting}
              style={inputStyle}
            />
            <small style={{ color: '#718096', fontSize: '12px' }}>Separate multiple tags with commas</small>
          </div>

          <div style={{ marginBottom: '16px' }}>
            <label style={labelStyle}>Source URL (Optional)</label>
            <input
              type="url"
              name="source_url"
              value={formData.source_url}
              onChange={handleChange}
              placeholder="https://company.com/careers/job-id"
              disabled={isSubmitting}
              style={inputStyle}
            />
          </div>

          <div style={{ marginBottom: '24px' }}>
            <label style={{ display: 'flex', alignItems: 'center', gap: '12px', cursor: 'pointer' }}>
              <input
                type="checkbox"
                name="remote_allowed"
                checked={formData.remote_allowed}
                onChange={handleChange}
                disabled={isSubmitting}
                style={{ width: 'auto', margin: 0 }}
              />
              <span style={{ fontWeight: '600', color: '#4a5568' }}>🏠 Remote work allowed</span>
            </label>
          </div>

          <div style={{ 
            display: 'flex', 
            gap: '12px', 
            justifyContent: 'flex-end',
            paddingTop: '16px',
            borderTop: '1px solid #e2e8f0'
          }}>
            <button 
              type="button" 
              onClick={onClose}
              disabled={isSubmitting}
              style={{
                padding: '12px 24px',
                border: '2px solid #e2e8f0',
                borderRadius: '8px',
                backgroundColor: '#f7fafc',
                color: '#4a5568',
                cursor: 'pointer',
                fontWeight: '600'
              }}
            >
              Cancel
            </button>
            <button 
              type="submit"
              disabled={isSubmitting}
              style={{
                padding: '12px 24px',
                border: 'none',
                borderRadius: '8px',
                backgroundColor: '#4299e1',
                color: 'white',
                cursor: 'pointer',
                fontWeight: '600'
              }}
            >
              {isSubmitting ? '⏳ Adding Job...' : '✅ Add Job'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

// Edit Job Form Component (simplified for now - you can expand this later)
function EditJobForm({ job, onClose, onSubmit }) {
  const [formData, setFormData] = useState({
    title: job?.title || '',
    company: job?.company || '',
    location: job?.location || '',
    job_type: job?.job_type || 'Full-time',
    description: job?.description || '',
    experience_level: job?.experience_level || 'Mid-Level',
    remote_allowed: job?.remote_allowed || false,
    tags: job?.tags || '',
    salary_range: job?.salary_range || '',
    source_url: job?.source_url || ''
  });
  
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    try {
      await onSubmit(job.id, formData);
    } catch (err) {
      alert('Failed to update job: ' + err.message);
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
    <div style={{ padding: '24px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <h2 style={{ margin: 0 }}>✏️ Edit Job: {job?.title}</h2>
        <button onClick={onClose} style={{ background: 'none', border: 'none', fontSize: '24px', cursor: 'pointer' }}>✕</button>
      </div>

      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '16px' }}>
          <label style={{ display: 'block', marginBottom: '8px', fontWeight: 'bold' }}>Job Title *</label>
          <input
            type="text"
            name="title"
            value={formData.title}
            onChange={handleChange}
            required
            disabled={isSubmitting}
            style={{ width: '100%', padding: '12px', border: '1px solid #ccc', borderRadius: '4px' }}
          />
        </div>

        <div style={{ marginBottom: '16px' }}>
          <label style={{ display: 'block', marginBottom: '8px', fontWeight: 'bold' }}>Company *</label>
          <input
            type="text"
            name="company"
            value={formData.company}
            onChange={handleChange}
            required
            disabled={isSubmitting}
            style={{ width: '100%', padding: '12px', border: '1px solid #ccc', borderRadius: '4px' }}
          />
        </div>

        <div style={{ marginBottom: '16px' }}>
          <label style={{ display: 'block', marginBottom: '8px', fontWeight: 'bold' }}>Description *</label>
          <textarea
            name="description"
            value={formData.description}
            onChange={handleChange}
            rows="4"
            required
            disabled={isSubmitting}
            style={{ width: '100%', padding: '12px', border: '1px solid #ccc', borderRadius: '4px' }}
          />
        </div>

        <div style={{ display: 'flex', gap: '12px', justifyContent: 'flex-end' }}>
          <button 
            type="button" 
            onClick={onClose}
            disabled={isSubmitting}
            style={{ padding: '12px 24px', border: '1px solid #ccc', borderRadius: '4px', backgroundColor: 'white', cursor: 'pointer' }}
          >
            Cancel
          </button>
          <button 
            type="submit"
            disabled={isSubmitting}
            style={{ padding: '12px 24px', border: 'none', borderRadius: '4px', backgroundColor: '#007bff', color: 'white', cursor: 'pointer' }}
          >
            {isSubmitting ? 'Updating...' : 'Update Job'}
          </button>
        </div>
      </form>
    </div>
  );
}

export default App;