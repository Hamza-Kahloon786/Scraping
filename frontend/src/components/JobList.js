/**
 * JobList Component - Displays grid of job cards with pagination
 */
import React from 'react';
import { 
  Row, 
  Col, 
  Card, 
  Button, 
  Pagination, 
  Alert,
  Spinner,
  Badge
} from 'react-bootstrap';
import JobCard from './JobCard';

const JobList = ({ 
  jobs = [], 
  loading = false, 
  error = null,
  pagination = null,
  onPageChange,
  onEditJob,
  onDeleteJob,
  onViewJob
}) => {
  
  // Handle pagination
  const handlePageClick = (page) => {
    if (onPageChange && page !== pagination?.page) {
      onPageChange(page);
    }
  };

  // Render pagination component
  const renderPagination = () => {
    if (!pagination || pagination.pages <= 1) return null;

    const { page: currentPage, pages: totalPages, has_prev, has_next } = pagination;
    const items = [];

    // Previous button
    items.push(
      <Pagination.Prev
        key="prev"
        disabled={!has_prev}
        onClick={() => handlePageClick(currentPage - 1)}
      />
    );

    // Page numbers
    const startPage = Math.max(1, currentPage - 2);
    const endPage = Math.min(totalPages, currentPage + 2);

    // First page and ellipsis
    if (startPage > 1) {
      items.push(
        <Pagination.Item
          key={1}
          active={currentPage === 1}
          onClick={() => handlePageClick(1)}
        >
          1
        </Pagination.Item>
      );
      
      if (startPage > 2) {
        items.push(<Pagination.Ellipsis key="ellipsis1" />);
      }
    }

    // Current page range
    for (let page = startPage; page <= endPage; page++) {
      items.push(
        <Pagination.Item
          key={page}
          active={page === currentPage}
          onClick={() => handlePageClick(page)}
        >
          {page}
        </Pagination.Item>
      );
    }

    // Last page and ellipsis
    if (endPage < totalPages) {
      if (endPage < totalPages - 1) {
        items.push(<Pagination.Ellipsis key="ellipsis2" />);
      }
      
      items.push(
        <Pagination.Item
          key={totalPages}
          active={currentPage === totalPages}
          onClick={() => handlePageClick(totalPages)}
        >
          {totalPages}
        </Pagination.Item>
      );
    }

    // Next button
    items.push(
      <Pagination.Next
        key="next"
        disabled={!has_next}
        onClick={() => handlePageClick(currentPage + 1)}
      />
    );

    return (
      <div className="d-flex justify-content-center mt-4">
        <Pagination>{items}</Pagination>
      </div>
    );
  };

  // Render pagination info
  const renderPaginationInfo = () => {
    if (!pagination || pagination.total === 0) return null;

    const { page, per_page, total } = pagination;
    const start = (page - 1) * per_page + 1;
    const end = Math.min(page * per_page, total);

    return (
      <div className="d-flex justify-content-between align-items-center mb-3">
        <small className="text-muted">
          Showing {start}-{end} of {total} jobs
        </small>
        
        <div className="d-flex align-items-center">
          {pagination.pages > 1 && (
            <small className="text-muted me-3">
              Page {page} of {pagination.pages}
            </small>
          )}
          
          <Button
            variant="outline-secondary"
            size="sm"
            onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
          >
            <i className="bi bi-arrow-up"></i>
            Top
          </Button>
        </div>
      </div>
    );
  };

  // Loading state
  if (loading) {
    return (
      <Card className="text-center py-5">
        <Card.Body>
          <Spinner animation="border" variant="primary" className="mb-3" />
          <h5>Loading jobs...</h5>
          <p className="text-muted">Please wait while we fetch the latest job listings.</p>
        </Card.Body>
      </Card>
    );
  }

  // Error state
  if (error) {
    return (
      <Alert variant="danger" className="text-center">
        <Alert.Heading>
          <i className="bi bi-exclamation-triangle me-2"></i>
          Oops! Something went wrong
        </Alert.Heading>
        <p className="mb-3">{error}</p>
        <Button 
          variant="outline-danger"
          onClick={() => window.location.reload()}
        >
          <i className="bi bi-arrow-clockwise me-2"></i>
          Try Again
        </Button>
      </Alert>
    );
  }

  // Empty state
  if (!jobs || jobs.length === 0) {
    return (
      <Card className="text-center py-5">
        <Card.Body>
          <div className="mb-3">
            <i className="bi bi-search display-1 text-muted"></i>
          </div>
          <h5>No jobs found</h5>
          <p className="text-muted mb-4">
            We couldn't find any jobs matching your criteria. 
            Try adjusting your filters or search terms.
          </p>
          <div className="d-flex gap-2 justify-content-center">
            <Button variant="outline-primary">
              <i className="bi bi-funnel me-2"></i>
              Clear Filters
            </Button>
            <Button variant="primary">
              <i className="bi bi-plus-circle me-2"></i>
              Add New Job
            </Button>
          </div>
        </Card.Body>
      </Card>
    );
  }

  // Job results summary
  const renderResultsSummary = () => {
    const totalJobs = pagination?.total || jobs.length;
    const hasFilters = window.location.search.includes('?'); // Simple check for filters
    
    return (
      <div className="mb-4">
        <div className="d-flex justify-content-between align-items-center">
          <div>
            <h5 className="mb-1">
              {totalJobs} Job{totalJobs !== 1 ? 's' : ''} Found
            </h5>
            {hasFilters && (
              <small className="text-muted">
                <i className="bi bi-funnel me-1"></i>
                Filtered results
              </small>
            )}
          </div>
          
          <div className="d-flex gap-2">
            {/* Quick stats badges */}
            <Badge bg="light" text="dark" className="d-none d-md-inline">
              <i className="bi bi-briefcase me-1"></i>
              {jobs.filter(job => job.job_type === 'Full-time').length} Full-time
            </Badge>
            
            <Badge bg="light" text="dark" className="d-none d-md-inline">
              <i className="bi bi-geo-alt me-1"></i>
              {jobs.filter(job => job.remote_allowed).length} Remote OK
            </Badge>
            
            <Badge bg="light" text="dark" className="d-none d-lg-inline">
              <i className="bi bi-robot me-1"></i>
              {jobs.filter(job => job.is_scraped).length} Auto-imported
            </Badge>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="job-list">
      {/* Results summary */}
      {renderResultsSummary()}
      
      {/* Pagination info */}
      {renderPaginationInfo()}

      {/* Job cards grid */}
      <Row>
        {jobs.map((job) => (
          <Col 
            key={job.id} 
            xs={12} 
            md={6} 
            lg={4} 
            xl={3} 
            className="mb-4"
          >
            <JobCard
              job={job}
              onEdit={onEditJob}
              onDelete={onDeleteJob}
              onView={onViewJob}
            />
          </Col>
        ))}
      </Row>

      {/* Bottom pagination */}
      {renderPagination()}

      {/* Back to top button for long lists */}
      {jobs.length > 12 && (
        <div className="text-center mt-4">
          <Button
            variant="outline-secondary"
            onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
          >
            <i className="bi bi-arrow-up me-2"></i>
            Back to Top
          </Button>
        </div>
      )}

      {/* Performance tip for large datasets */}
      {pagination && pagination.total > 500 && (
        <Alert variant="info" className="mt-4">
          <Alert.Heading>
            <i className="bi bi-lightbulb me-2"></i>
            Tip
          </Alert.Heading>
          <p className="mb-0">
            With {pagination.total} total jobs, try using filters to narrow down results 
            for better performance and easier browsing.
          </p>
        </Alert>
      )}
    </div>
  );
};

export default JobList;