import React from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import App from './App';

// Wait for DOM to be ready
const initializeApp = () => {
  const container = document.getElementById('root');
  
  if (!container) {
    console.error('❌ Could not find root element. Make sure public/index.html has <div id="root"></div>');
    return;
  }

  console.log('✅ Root element found, initializing React app...');
  
  try {
    const root = createRoot(container);
    root.render(
      <React.StrictMode>
        <App />
      </React.StrictMode>
    );
    console.log('✅ React app initialized successfully');
  } catch (error) {
    console.error('❌ Failed to initialize React app:', error);
  }
};

// Initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initializeApp);
} else {
  initializeApp();
}