/**
 * FilterControls Component - Search and filter interface for jobs
 */
import React, { useState, useEffect } from 'react';
import { 
  Row, 
  Col, 
  Form, 
  Button, 
  InputGroup, 
  Badge,
  Card,
  Collapse
} from 'react-bootstrap';
import Select from 'react-select';
import '../styles/FilterControls.css';

const FilterControls = ({ 
  onFiltersChange, 
  onSortChange, 
  initialFilters = {},
  jobStats = {} 
}) => {
  const [filters, setFilters] = useState({
    search: '',
    job_type: 'All',
    location: '',
    tags: [],
    experience_level: 'All',
    remote_allowed: 'All',
    ...initialFilters
  });

  const [sortOptions, setSortOptions] = useState({
    sort: 'posting_date',
    order: 'desc'
  });

  const [showAdvancedFilters, setShowAdvancedFilters] = useState(false);

  // Job type options
  const jobTypeOptions = [
    { value: 'All', label: 'All Job Types' },
    { value: 'Full-time', label: 'Full-time' },
    { value: 'Part-time', label: 'Part-time' },
    { value: 'Contract', label: 'Contract' },
    { value: 'Internship', label: 'Internship' },
    { value: 'Temporary', label: 'Temporary' }
  ];

  // Experience level options
  const experienceLevelOptions = [
    { value: 'All', label: 'All Levels' },
    { value: 'Entry Level', label: 'Entry Level' },
    { value: 'Mid-Level', label: 'Mid-Level' },
    { value: 'Senior', label: 'Senior' },
    { value: 'Executive', label: 'Executive' },
    { value: 'Internship', label: 'Internship' }
  ];

  // Remote work options
  const remoteOptions = [
    { value: 'All', label: 'All Locations' },
    { value: 'true', label: 'Remote OK' },
    { value: 'false', label: 'On-site Only' }
  ];

  // Popular tags (can be dynamic based on jobStats)
  const popularTags = [
    'Life Insurance', 'Health Insurance', 'Property & Casualty',
    'Pricing', 'Reserving', 'Modeling', 'Valuation',
    'Python', 'R', 'SQL', 'Excel', 'SAS',
    'ASA', 'FSA', 'ACAS', 'FCAS',
    'Analytics', 'Risk Management', 'Consulting'
  ];

  const tagOptions = popularTags.map(tag => ({
    value: tag,
    label: tag
  }));

  // Sort options
  const sortingOptions = [
    { value: 'posting_date', label: 'Date Posted' },
    { value: 'title', label: 'Job Title' },
    { value: 'company', label: 'Company Name' },
    { value: 'created_at', label: 'Date Added' }
  ];

  // Update filters and notify parent
  const updateFilters = (newFilters) => {
    setFilters(prev => {
      const updated = { ...prev, ...newFilters };
      onFiltersChange(updated);
      return updated;
    });
  };

  // Update sorting and notify parent
  const updateSort = (newSort) => {
    setSortOptions(prev => {
      const updated = { ...prev, ...newSort };
      onSortChange(updated);
      return updated;
    });
  };

  // Handle search input change
  const handleSearchChange = (e) => {
    const search = e.target.value;
    updateFilters({ search });
  };

  // Handle job type change
  const handleJobTypeChange = (e) => {
    const job_type = e.target.value;
    updateFilters({ job_type });
  };

  // Handle location change
  const handleLocationChange = (e) => {
    const location = e.target.value;
    updateFilters({ location });
  };

  // Handle tags change
  const handleTagsChange = (selectedOptions) => {
    const tags = selectedOptions ? selectedOptions.map(option => option.value) : [];
    updateFilters({ tags });
  };

  // Handle experience level change
  const handleExperienceLevelChange = (e) => {
    const experience_level = e.target.value;
    updateFilters({ experience_level });
  };

  // Handle remote work change
  const handleRemoteChange = (e) => {
    const remote_allowed = e.target.value;
    updateFilters({ remote_allowed });
  };

  // Handle sort field change
  const handleSortChange = (e) => {
    const sort = e.target.value;
    updateSort({ sort });
  };

  // Handle sort order change
  const handleOrderChange = (e) => {
    const order = e.target.value;
    updateSort({ order });
  };

  // Clear all filters
  const clearFilters = () => {
    const clearedFilters = {
      search: '',
      job_type: 'All',
      location: '',
      tags: [],
      experience_level: 'All',
      remote_allowed: 'All'
    };
    setFilters(clearedFilters);
    onFiltersChange(clearedFilters);
  };

  // Count active filters
  const getActiveFiltersCount = () => {
    let count = 0;
    if (filters.search) count++;
    if (filters.job_type !== 'All') count++;
    if (filters.location) count++;
    if (filters.tags && filters.tags.length > 0) count++;
    if (filters.experience_level !== 'All') count++;
    if (filters.remote_allowed !== 'All') count++;
    return count;
  };

  const activeFiltersCount = getActiveFiltersCount();

  return (
    <Card className="filter-controls mb-4">
      <Card.Body>
        {/* Main search and quick filters */}
        <Row className="align-items-end">
          {/* Search bar */}
          <Col md={6} className="mb-3">
            <Form.Label htmlFor="search">Search Jobs</Form.Label>
            <InputGroup>
              <InputGroup.Text>
                <i className="bi bi-search"></i>
              </InputGroup.Text>
              <Form.Control
                id="search"
                type="text"
                placeholder="Search by title, company, or keywords..."
                value={filters.search}
                onChange={handleSearchChange}
              />
              {filters.search && (
                <Button 
                  variant="outline-secondary"
                  onClick={() => updateFilters({ search: '' })}
                >
                  <i className="bi bi-x"></i>
                </Button>
              )}
            </InputGroup>
          </Col>

          {/* Job type filter */}
          <Col md={3} className="mb-3">
            <Form.Label htmlFor="job-type">Job Type</Form.Label>
            <Form.Select
              id="job-type"
              value={filters.job_type}
              onChange={handleJobTypeChange}
            >
              {jobTypeOptions.map(option => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </Form.Select>
          </Col>

          {/* Advanced filters toggle */}
          <Col md={3} className="mb-3">
            <Button
              variant="outline-primary"
              onClick={() => setShowAdvancedFilters(!showAdvancedFilters)}
              className="w-100"
            >
              <i className="bi bi-funnel me-2"></i>
              Advanced Filters
              {activeFiltersCount > 0 && (
                <Badge bg="primary" className="ms-2">
                  {activeFiltersCount}
                </Badge>
              )}
            </Button>
          </Col>
        </Row>

        {/* Advanced filters */}
        <Collapse in={showAdvancedFilters}>
          <div>
            <hr />
            <Row>
              {/* Location filter */}
              <Col md={4} className="mb-3">
                <Form.Label htmlFor="location">Location</Form.Label>
                <Form.Control
                  id="location"
                  type="text"
                  placeholder="Enter city, state, or country..."
                  value={filters.location}
                  onChange={handleLocationChange}
                />
              </Col>

              {/* Experience level filter */}
              <Col md={4} className="mb-3">
                <Form.Label htmlFor="experience-level">Experience Level</Form.Label>
                <Form.Select
                  id="experience-level"
                  value={filters.experience_level}
                  onChange={handleExperienceLevelChange}
                >
                  {experienceLevelOptions.map(option => (
                    <option key={option.value} value={option.value}>
                      {option.label}
                    </option>
                  ))}
                </Form.Select>
              </Col>

              {/* Remote work filter */}
              <Col md={4} className="mb-3">
                <Form.Label htmlFor="remote-work">Remote Work</Form.Label>
                <Form.Select
                  id="remote-work"
                  value={filters.remote_allowed}
                  onChange={handleRemoteChange}
                >
                  {remoteOptions.map(option => (
                    <option key={option.value} value={option.value}>
                      {option.label}
                    </option>
                  ))}
                </Form.Select>
              </Col>
            </Row>

            {/* Tags filter */}
            <Row>
              <Col md={12} className="mb-3">
                <Form.Label htmlFor="tags">Skills & Keywords</Form.Label>
                <Select
                  inputId="tags"
                  isMulti
                  options={tagOptions}
                  value={tagOptions.filter(option => filters.tags.includes(option.value))}
                  onChange={handleTagsChange}
                  placeholder="Select skills, technologies, certifications..."
                  className="react-select-container"
                  classNamePrefix="react-select"
                  closeMenuOnSelect={false}
                  components={{
                    MultiValueRemove: ({ innerProps, ...props }) => (
                      <div {...innerProps} className="react-select__multi-value__remove">
                        <i className="bi bi-x"></i>
                      </div>
                    )
                  }}
                />
              </Col>
            </Row>

            {/* Sorting options */}
            <Row>
              <Col md={6} className="mb-3">
                <Form.Label htmlFor="sort-by">Sort By</Form.Label>
                <Form.Select
                  id="sort-by"
                  value={sortOptions.sort}
                  onChange={handleSortChange}
                >
                  {sortingOptions.map(option => (
                    <option key={option.value} value={option.value}>
                      {option.label}
                    </option>
                  ))}
                </Form.Select>
              </Col>

              <Col md={6} className="mb-3">
                <Form.Label htmlFor="sort-order">Sort Order</Form.Label>
                <Form.Select
                  id="sort-order"
                  value={sortOptions.order}
                  onChange={handleOrderChange}
                >
                  <option value="desc">Newest First</option>
                  <option value="asc">Oldest First</option>
                </Form.Select>
              </Col>
            </Row>

            {/* Filter actions */}
            <Row>
              <Col className="d-flex justify-content-between align-items-center">
                <div className="filter-summary">
                  {activeFiltersCount > 0 && (
                    <small className="text-muted">
                      <i className="bi bi-funnel-fill me-1"></i>
                      {activeFiltersCount} filter{activeFiltersCount !== 1 ? 's' : ''} applied
                    </small>
                  )}
                </div>
                
                <div>
                  {activeFiltersCount > 0 && (
                    <Button
                      variant="outline-secondary"
                      size="sm"
                      onClick={clearFilters}
                      className="me-2"
                    >
                      <i className="bi bi-x-circle me-1"></i>
                      Clear Filters
                    </Button>
                  )}
                  
                  <Button
                    variant="outline-primary"
                    size="sm"
                    onClick={() => setShowAdvancedFilters(false)}
                  >
                    <i className="bi bi-chevron-up me-1"></i>
                    Hide Filters
                  </Button>
                </div>
              </Col>
            </Row>
          </div>
        </Collapse>

        {/* Active filters display */}
        {activeFiltersCount > 0 && (
          <div className="active-filters mt-3">
            <div className="d-flex flex-wrap align-items-center">
              <small className="text-muted me-2">Active filters:</small>
              
              {filters.search && (
                <Badge 
                  bg="primary" 
                  className="me-2 mb-1 filter-badge"
                  onClick={() => updateFilters({ search: '' })}
                >
                  Search: "{filters.search}"
                  <i className="bi bi-x ms-1"></i>
                </Badge>
              )}
              
              {filters.job_type !== 'All' && (
                <Badge 
                  bg="primary" 
                  className="me-2 mb-1 filter-badge"
                  onClick={() => updateFilters({ job_type: 'All' })}
                >
                  Type: {filters.job_type}
                  <i className="bi bi-x ms-1"></i>
                </Badge>
              )}
              
              {filters.location && (
                <Badge 
                  bg="primary" 
                  className="me-2 mb-1 filter-badge"
                  onClick={() => updateFilters({ location: '' })}
                >
                  Location: {filters.location}
                  <i className="bi bi-x ms-1"></i>
                </Badge>
              )}
              
              {filters.experience_level !== 'All' && (
                <Badge 
                  bg="primary" 
                  className="me-2 mb-1 filter-badge"
                  onClick={() => updateFilters({ experience_level: 'All' })}
                >
                  Level: {filters.experience_level}
                  <i className="bi bi-x ms-1"></i>
                </Badge>
              )}
              
              {filters.remote_allowed !== 'All' && (
                <Badge 
                  bg="primary" 
                  className="me-2 mb-1 filter-badge"
                  onClick={() => updateFilters({ remote_allowed: 'All' })}
                >
                  {filters.remote_allowed === 'true' ? 'Remote OK' : 'On-site Only'}
                  <i className="bi bi-x ms-1"></i>
                </Badge>
              )}
              
              {filters.tags && filters.tags.length > 0 && (
                filters.tags.map(tag => (
                  <Badge 
                    key={tag}
                    bg="primary" 
                    className="me-2 mb-1 filter-badge"
                    onClick={() => updateFilters({ 
                      tags: filters.tags.filter(t => t !== tag) 
                    })}
                  >
                    {tag}
                    <i className="bi bi-x ms-1"></i>
                  </Badge>
                ))
              )}
            </div>
          </div>
        )}

        {/* Quick stats */}
        {jobStats && Object.keys(jobStats).length > 0 && (
          <div className="job-stats mt-3 pt-3 border-top">
            <Row>
              <Col>
                <small className="text-muted">
                  <i className="bi bi-bar-chart me-1"></i>
                  Quick Stats: 
                  {jobStats.total_jobs && (
                    <span className="ms-2">
                      <strong>{jobStats.total_jobs}</strong> total jobs
                    </span>
                  )}
                  {jobStats.recent_jobs !== undefined && (
                    <span className="ms-2">
                      <strong>{jobStats.recent_jobs}</strong> this week
                    </span>
                  )}
                  {jobStats.job_types && (
                    <span className="ms-2">
                      <strong>{Object.keys(jobStats.job_types).length}</strong> job types
                    </span>
                  )}
                </small>
              </Col>
            </Row>
          </div>
        )}
      </Card.Body>
    </Card>
  );
};

export default FilterControls;