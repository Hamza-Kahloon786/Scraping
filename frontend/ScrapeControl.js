
// ScrapeControl.js - React component for web scraping controls
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ScrapeControl = ({ onJobsUpdated }) => {
  const [scrapeStatus, setScrapeStatus] = useState({
    is_running: false,
    progress: 0,
    current_step: '',
    jobs_found: 0,
    last_run: null,
    error: null
  });
  const [maxJobs, setMaxJobs] = useState(50);
  const [headless, setHeadless] = useState(true);

  const API_BASE = 'http://localhost:5000/api';

  // Poll scraping status when running
  useEffect(() => {
    let interval;
    if (scrapeStatus.is_running) {
      interval = setInterval(checkScrapeStatus, 2000); // Check every 2 seconds
    }
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [scrapeStatus.is_running]);

  const checkScrapeStatus = async () => {
    try {
      const response = await axios.get(`${API_BASE}/scrape/status`);
      if (response.data.success) {
        setScrapeStatus(response.data.status);
        
        // If scraping completed, refresh jobs
        if (!response.data.status.is_running && response.data.status.jobs_found > 0) {
          if (onJobsUpdated) {
            onJobsUpdated();
          }
        }
      }
    } catch (error) {
      console.error('Error checking scrape status:', error);
    }
  };

  const startScraping = async () => {
    try {
      const response = await axios.post(`${API_BASE}/scrape/start`, {
        max_jobs: maxJobs,
        headless: headless
      });

      if (response.data.success) {
        setScrapeStatus({
          is_running: true,
          progress: 0,
          current_step: 'Starting...',
          jobs_found: 0,
          error: null
        });
      } else {
        alert('Failed to start scraping: ' + response.data.error);
      }
    } catch (error) {
      alert('Error starting scraper: ' + error.message);
    }
  };

  const stopScraping = async () => {
    try {
      const response = await axios.post(`${API_BASE}/scrape/stop`);
      if (response.data.success) {
        setScrapeStatus(prev => ({
          ...prev,
          is_running: false,
          current_step: 'Stopped by user'
        }));
      }
    } catch (error) {
      console.error('Error stopping scraper:', error);
    }
  };

  const formatLastRun = (lastRun) => {
    if (!lastRun) return 'Never';
    return new Date(lastRun).toLocaleString();
  };

  return (
    <div className="scrape-control bg-white rounded-lg shadow-md p-6 mb-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-xl font-semibold text-gray-900 flex items-center">
          <span className="mr-2">🕷️</span>
          ActuaryList Scraper
        </h3>
        
        {!scrapeStatus.is_running ? (
          <button
            onClick={startScraping}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors flex items-center space-x-2"
          >
            <span>▶️</span>
            <span>Start Scraping</span>
          </button>
        ) : (
          <button
            onClick={stopScraping}
            className="bg-red-600 text-white px-6 py-2 rounded-lg hover:bg-red-700 transition-colors flex items-center space-x-2"
          >
            <span>⏹️</span>
            <span>Stop</span>
          </button>
        )}
      </div>

      {/* Configuration */}
      {!scrapeStatus.is_running && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Maximum Jobs to Scrape
            </label>
            <input
              type="number"
              min="10"
              max="200"
              value={maxJobs}
              onChange={(e) => setMaxJobs(parseInt(e.target.value))}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Browser Mode
            </label>
            <select
              value={headless ? 'headless' : 'visible'}
              onChange={(e) => setHeadless(e.target.value === 'headless')}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              <option value="headless">Headless (Background)</option>
              <option value="visible">Visible (For Debugging)</option>
            </select>
          </div>
        </div>
      )}

      {/* Status Display */}
      <div className="bg-gray-50 rounded-lg p-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Status */}
          <div>
            <div className="text-sm font-medium text-gray-500">Status</div>
            <div className={`text-lg font-semibold ${
              scrapeStatus.is_running ? 'text-blue-600' : 
              scrapeStatus.error ? 'text-red-600' : 'text-green-600'
            }`}>
              {scrapeStatus.is_running ? 'Running' : 
               scrapeStatus.error ? 'Error' : 'Ready'}
            </div>
          </div>

          {/* Progress */}
          <div>
            <div className="text-sm font-medium text-gray-500">Progress</div>
            <div className="text-lg font-semibold text-gray-900">
              {scrapeStatus.progress}%
            </div>
            {scrapeStatus.is_running && (
              <div className="w-full bg-gray-200 rounded-full h-2 mt-1">
                <div 
                  className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${scrapeStatus.progress}%` }}
                ></div>
              </div>
            )}
          </div>

          {/* Jobs Found */}
          <div>
            <div className="text-sm font-medium text-gray-500">Jobs Found</div>
            <div className="text-lg font-semibold text-green-600">
              {scrapeStatus.jobs_found}
            </div>
          </div>
        </div>

        {/* Current Step */}
        {scrapeStatus.current_step && (
          <div className="mt-4">
            <div className="text-sm font-medium text-gray-500">Current Step</div>
            <div className="text-gray-900 flex items-center">
              {scrapeStatus.is_running && (
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600 mr-2"></div>
              )}
              {scrapeStatus.current_step}
            </div>
          </div>
        )}

        {/* Error Message */}
        {scrapeStatus.error && (
          <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg">
            <div className="text-sm font-medium text-red-800">Error</div>
            <div className="text-red-700">{scrapeStatus.error}</div>
          </div>
        )}

        {/* Last Run */}
        <div className="mt-4 flex justify-between items-center text-sm text-gray-500">
          <span>Last run: {formatLastRun(scrapeStatus.last_run)}</span>
          <span>Source: actuarylist.com</span>
        </div>
      </div>

      {/* Help Text */}
      <div className="mt-4 text-sm text-gray-600">
        <p>
          <strong>How it works:</strong> This scraper visits actuarylist.com and extracts 
          actuarial job listings automatically. It finds job titles, companies, locations, 
          and other relevant details.
        </p>
        <div className="mt-2">
          <strong>Tips:</strong>
          <ul className="list-disc list-inside ml-4 space-y-1">
            <li>Start with 20-50 jobs for testing</li>
            <li>Use headless mode for production</li>
            <li>Scraping takes 2-5 minutes depending on job count</li>
            <li>New jobs are automatically added to your job board</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default ScrapeControl;