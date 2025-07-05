# Job Board Application

A full-stack job listing web application built for Bitbash's hiring assessment. This application allows users to view, add, edit, and delete actuarial job postings with data scraped from Actuary List website.

## 🚀 Project Overview

This project demonstrates full-stack development skills including:
- **Backend**: Flask REST API with SQLAlchemy and PostgreSQL/MySQL
- **Frontend**: React.js with responsive UI
- **Web Scraping**: Selenium automation for data collection
- **Database**: CRUD operations with filtering and sorting

## 🏗️ Architecture

```
job-board-application/
├── frontend/                 # React.js application
│   ├── src/
│   │   ├── components/      # Reusable React components
│   │   ├── pages/          # Main application pages
│   │   └── App.js          # Main App component
│   ├── public/
│   └── package.json
├── backend/                 # Flask API server
│   ├── app/
│   │   ├── models/             # SQLAlchemy database models
│   │   ├── routes/             # API route definitions
│   │   ├── scraping/           # Selenium web scraper
│   │-run.py              # Application entry point
│   │-requirements.txt
│   
└── README.md
```

## 🛠️ Technology Stack

### Backend
- **Flask** - Python web framework
- **SQLAlchemy** - ORM for database operations
- **PostgreSQL/MySQL** - Relational database
- **Flask-CORS** - Cross-origin resource sharing
- **Selenium** - Web scraping automation

### Frontend
- **React.js** - Frontend JavaScript library
- **CSS3** - Styling and responsive design
- **Axios** - HTTP client for API calls
- **React Hooks** - State management

## 📋 Features

### Core Functionality
- ✅ **CRUD Operations**: Create, Read, Update, Delete job listings
- ✅ **Filtering**: Filter jobs by type, location, and tags
- ✅ **Sorting**: Sort by posting date, company, or title
- ✅ **Search**: Keyword search across job titles and companies
- ✅ **Responsive Design**: Mobile and desktop optimized
- ✅ **Web Scraping**: Automated data collection from Actuary List

### API Endpoints
```
GET    /api/jobs              # Get all jobs with optional filters
GET    /api/jobs/      # Get specific job by ID
POST   /api/jobs              # Create new job
PUT    /api/jobs/        # Update existing job
DELETE /api/jobs/         # Delete job
```

### Database Schema
```sql
Job Model:
- id (Primary Key)
- title (String, required)
- company (String, required)
- location (String, required)
- posting_date (DateTime)
- job_type (String)
- tags (String, comma-separated)
```

## 🚀 Setup Instructions

### Prerequisites
- **Python 3.8+**
- **Node.js 14+**
- **PostgreSQL** or **MySQL**
- **Chrome Browser** (for Selenium)

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database Configuration**
   - Create a new database in PostgreSQL/MySQL
   - Update database connection string in `config.py` or environment variables
   
   ```python
   # Example database URL format
   DATABASE_URL = "postgresql://username:password@localhost/job_board"
   # or
   DATABASE_URL = "mysql://username:password@localhost/job_board"
   ```

5. **Initialize database**
   ```bash
   python -c "from app import db; db.create_all()"
   ```

6. **Run the Flask server**
   ```bash
   python run.py
   ```
   
   The API will be available at `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm start
   ```
   
   The React app will be available at `http://localhost:3000`

### Web Scraper Setup

1. **Install ChromeDriver**
   - Download ChromeDriver from https://chromedriver.chromium.org/
   - Add to your system PATH or place in backend directory

2. **Run the scraper**
   ```bash
   cd backend
   python app/run_scraper.py
         OR 
   Scrape jobs Icon from Frontend 

   ```

## 🎯 Usage Guide

### Adding New Jobs
1. Click "Add New Job" button
2. Fill in required fields (Title, Company, Location)
3. Select job type and add relevant tags
4. Submit form to create new job listing

### Filtering Jobs
- **By Job Type**: Use dropdown to filter Full-time, Part-time, etc.
- **By Location**: Select from available locations
- **By Tags**: Use checkboxes to filter by skill/industry tags
- **Search**: Enter keywords to search titles and companies

### Editing Jobs
1. Click "Edit" button on any job card
2. Modify fields in the form
3. Save changes to update the listing

### Deleting Jobs
1. Click "Delete" button on job card
2. Confirm deletion in the prompt
3. Job will be removed from the database

## 🕷️ Web Scraping Details

The Selenium scraper automatically collects job data from https://www.actuarylist.com including:

- **Job Title**: Position name
- **Company**: Employer name
- **Location**: City and country
- **Posting Date**: When the job was posted
- **Job Type**: Full-time, Part-time, etc. (inferred if not explicit)
- **Tags**: Skills, industries, and categories

### Scraping Features
- **Dynamic Content Handling**: Manages infinite scroll and "Load More" buttons
- **Duplicate Prevention**: Checks existing jobs before inserting
- **Error Handling**: Gracefully handles missing data or page changes
- **Batch Processing**: Processes multiple pages efficiently
```

## 🧪 API Testing

### Using curl
```bash
# Get all jobs
curl http://localhost:5000/api/jobs

# Get jobs with filters
curl "http://localhost:5000/api/jobs?job_type=Full-time&location=London"

# Create new job
curl -X POST http://localhost:5000/api/jobs \
  -H "Content-Type: application/json" \
  -d '{"title":"Senior Actuary","company":"ABC Insurance","location":"New York"}'

# Update job
curl -X PUT http://localhost:5000/api/jobs/1 \
  -H "Content-Type: application/json" \
  -d '{"title":"Lead Actuary","company":"ABC Insurance","location":"New York"}'

# Delete job
curl -X DELETE http://localhost:5000/api/jobs/1
```

### Using Postman
Import the API endpoints and test all CRUD operations with the Postman collection.

## 🎨 Frontend Components

### Key Components
- **JobList**: Displays all job listings with pagination
- **JobCard**: Individual job display component
- **JobForm**: Add/Edit job form with validation
- **FilterBar**: Filtering and sorting controls
- **SearchBox**: Keyword search functionality

### State Management
- Uses React hooks (useState, useEffect) for state management
- Implements real-time UI updates after API operations
- Handles loading states and error messages

## 🛡️ Error Handling

### Backend
- **Input Validation**: Validates required fields and data types
- **HTTP Status Codes**: Proper status codes (200, 201, 400, 404, 500)
- **Error Messages**: Clear, descriptive error responses
- **Exception Handling**: Prevents server crashes

### Frontend
- **Form Validation**: Client-side validation before submission
- **API Error Handling**: Displays user-friendly error messages
- **Loading States**: Shows feedback during API calls
- **Fallback UI**: Handles network errors gracefully

## 📱 Responsive Design

- **Mobile-First**: Designed for mobile devices first
- **Breakpoints**: Responsive layouts for different screen sizes
- **Touch-Friendly**: Optimized for touch interactions
- **Accessibility**: Semantic HTML and keyboard navigation

## 🔧 Configuration

### Environment Variables
Create `.env` file in backend directory:
```
DATABASE_URL=postgresql://username:password@localhost/job_board
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
CORS_ORIGINS=http://localhost:3000
```

### Development vs Production
- **Development**: Debug mode enabled, CORS allowed for localhost
- **Production**: Debug disabled, secure CORS settings, environment-based config

## 🚀 Deployment

### Backend Deployment
1. Set production environment variables
2. Install production dependencies
3. Run database migrations
4. Configure web server (Gunicorn, uWSGI)

### Frontend Deployment
1. Build production bundle: `npm run build`
2. Serve static files from build directory
3. Configure API base URL for production

## 🧩 Project Decisions & Trade-offs

### Architecture Choices
- **Monolithic Structure**: Simpler deployment and development
- **SQLAlchemy ORM**: Faster development over raw SQL
- **Comma-separated Tags**: Simple implementation vs. normalized table
- **Client-side Filtering**: Better UX for small datasets

### Time Management
- **Prioritized Core Features**: CRUD operations and basic UI first
- **Simplified Authentication**: Focused on core functionality
- **Basic Styling**: Clean, professional look without complex design

### Assumptions Made
- **Job Types**: Default to "Full-time" when not specified
- **Date Handling**: Store posting dates as strings for flexibility
- **Tag Format**: Simple comma-separated values
- **User Base**: Single-user application (no authentication required)

## 🎥 Video Demonstration

A comprehensive video walkthrough is available showing:
- **Project Overview**: Architecture and technology choices
- **API Demonstration**: All CRUD operations using Postman
- **Frontend Walkthrough**: Complete UI functionality
- **Scraper Demo**: Live data collection from Actuary List
- **Challenges & Solutions**: Technical decisions and problem-solving

## 📞 Support & Contact

For questions about this project or implementation details, please contact the development team.

## 📄 License

This project is created for Bitbash's technical assessment and is not intended for commercial use.

---