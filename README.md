# Study Partner

An AI-powered study assistant platform.

## Architecture

- **Backend**: Django with PostgreSQL and Redis
- **Frontend**: Next.js with TypeScript and Tailwind CSS
- **Async Tasks**: Celery with Redis broker

## Setup

### Prerequisites

- Python 3.11
- Node.js 20+ (for Next.js)
- Docker and Docker Compose

### Backend Setup

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Create virtual environment:
   ```bash
   python3.11 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Start development server:
   ```bash
   python manage.py runserver
   ```

### Frontend Setup

1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start development server:
   ```bash
   npm run dev
   ```

### Docker Setup

To run with Docker:

1. Start services:
   ```bash
   docker-compose up --build
   ```

This will start PostgreSQL, Redis, and the backend.

## Development Guidelines

- Use modular architecture with clear separation of concerns
- Avoid spaghetti code by organizing code into logical modules
- Follow Django and Next.js best practices
- Use environment variables for configuration