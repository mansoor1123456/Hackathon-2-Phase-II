# Quickstart Guide: Phase II - Full-Stack Web Application

## Prerequisites
- Node.js 18+ and pnpm
- Python 3.13+
- PostgreSQL client tools
- Git

## Setup Instructions

### 1. Clone and Initialize Repository
```bash
# Clone the repository
git clone <repository-url>
cd <repository-name>

# Install pnpm if not already installed
npm install -g pnpm

# Install dependencies
pnpm install
```

### 2. Set Up Environment Variables
```bash
# Copy environment files
cp packages/backend/.env.example packages/backend/.env
cp packages/frontend/.env.example packages/frontend/.env
```

### 3. Configure Database
```bash
# Set up Neon PostgreSQL database
# 1. Create account at neon.tech
# 2. Create a new project
# 3. Copy the connection string to packages/backend/.env as DATABASE_URL
```

### 4. Install Backend Dependencies
```bash
cd packages/backend
pip install -r requirements.txt
```

### 5. Run Database Migrations
```bash
cd packages/backend
# Run initial migrations to set up tables
python -m alembic upgrade head
```

### 6. Start Development Servers
```bash
# Terminal 1: Start backend
cd packages/backend
python main.py

# Terminal 2: Start frontend
cd packages/frontend
pnpm dev
```

## Available Scripts

### Frontend Commands
```bash
pnpm dev          # Start development server
pnpm build        # Build for production
pnpm start        # Start production server
pnpm test         # Run tests
```

### Backend Commands
```bash
python main.py    # Start development server
python -m pytest  # Run tests
python -m alembic # Database migrations
```

## Project Structure
- `packages/frontend/` - Next.js application
- `packages/backend/` - FastAPI application
- `packages/shared/` - Shared types and utilities

## API Endpoints
- Backend: http://localhost:8000
- Frontend: http://localhost:3000
- API routes follow REST conventions under `/api/`

## Authentication
- Register at `/auth/register`
- Login at `/auth/login`
- Protected routes require JWT in Authorization header