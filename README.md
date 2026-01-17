# Todo Application - Phase II

A full-stack todo application built with Next.js and FastAPI, featuring multi-user support, authentication, and persistent storage.

## Tech Stack

- **Frontend**: Next.js 16+ with App Router
- **Backend**: FastAPI with Python 3.13+
- **Database**: Neon Serverless PostgreSQL with SQLModel ORM
- **Authentication**: JWT-based authentication
- **Styling**: Tailwind CSS

## Features

- User registration and authentication
- Todo CRUD operations (Create, Read, Update, Delete)
- Multi-user support with data isolation
- Responsive web interface
- JWT-based session management

## Prerequisites

- Node.js 16+
- Python 3.13+
- pnpm
- PostgreSQL (or Neon Serverless PostgreSQL)

## Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Install dependencies

```bash
# Install pnpm if you don't have it
npm install -g pnpm

# Install all dependencies
pnpm install
```

### 3. Set up environment variables

#### Backend configuration

```bash
cd packages/backend
cp .env.example .env
```

Update the `.env` file with your database URL and secret keys.

#### Frontend configuration

```bash
cd packages/frontend
cp .env.example .env
```

Update the `.env` file with your API base URL.

### 4. Start the development servers

```bash
# Terminal 1: Start the backend
cd packages/backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Terminal 2: Start the frontend
cd packages/frontend
pnpm dev
```

## Project Structure

```
packages/
├── backend/          # FastAPI application
│   ├── app/
│   │   ├── models/   # SQLModel database models
│   │   ├── schemas/  # Pydantic request/response schemas
│   │   ├── services/ # Business logic
│   │   ├── api/      # API routes
│   │   ├── database/ # Database connection
│   │   └── auth/     # Authentication utilities
│   └── requirements.txt
├── frontend/         # Next.js application
│   ├── app/          # App Router pages
│   ├── components/   # React components
│   ├── lib/          # Utility functions
│   └── styles/       # Global styles
└── shared/           # Shared types and constants
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Authenticate user and get JWT
- `POST /api/v1/auth/logout` - Logout user

### Todos
- `GET /api/v1/todos` - Get all todos for authenticated user
- `POST /api/v1/todos` - Create a new todo
- `GET /api/v1/todos/{id}` - Get a specific todo
- `PUT /api/v1/todos/{id}` - Update a specific todo
- `DELETE /api/v1/todos/{id}` - Delete a specific todo

## Environment Variables

### Backend (.env)
- `DATABASE_URL` - PostgreSQL database URL
- `SECRET_KEY` - Secret key for JWT signing
- `ALGORITHM` - JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - JWT expiration time

### Frontend (.env)
- `NEXT_PUBLIC_API_BASE_URL` - Base URL for API requests

## Development

This is a monorepo managed with pnpm and Turbo. You can run commands across all packages:

```bash
# Run dev servers for all packages
pnpm dev

# Build all packages
pnpm build

# Run tests across all packages
pnpm test
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request