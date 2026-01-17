# Monorepo Organization Specification

## Overview
This document specifies the monorepo structure for the full-stack todo application. The structure separates frontend and backend concerns while maintaining shared configurations and documentation in a unified repository.

## Repository Structure

```
project-root/
├── .specify/                 # Spec-Kit Plus configuration and templates
│   ├── memory/
│   ├── templates/
│   └── scripts/
├── specs/                    # All feature specifications
│   └── 1-phase2-fullstack-webapp/
│       ├── spec.md
│       ├── checklists/
│       ├── specs/            # Additional detailed specifications
│       └── CLAUDE.md
├── packages/                 # Monorepo packages
│   ├── frontend/             # Next.js web application
│   │   ├── app/              # App Router pages and layouts
│   │   ├── components/       # Reusable React components
│   │   ├── lib/              # Client-side utilities and services
│   │   ├── public/           # Static assets
│   │   ├── styles/           # Global styles and CSS modules
│   │   ├── types/            # TypeScript type definitions
│   │   ├── .env.example
│   │   ├── next.config.js
│   │   ├── package.json
│   │   └── tsconfig.json
│   ├── backend/              # FastAPI server application
│   │   ├── app/              # API routes and application logic
│   │   ├── models/           # SQLModel database models
│   │   ├── schemas/          # Pydantic request/response schemas
│   │   ├── auth/             # Authentication and authorization logic
│   │   ├── database/         # Database connection and session management
│   │   ├── utils/            # Server-side utilities
│   │   ├── tests/            # Backend test suite
│   │   ├── requirements.txt
│   │   ├── .env.example
│   │   └── main.py
│   └── shared/               # Shared types, constants, and utilities
│       ├── types/            # Shared TypeScript interfaces
│       ├── constants/        # Shared constant values
│       ├── utils/            # Shared utility functions
│       └── package.json
├── docker/                   # Docker configurations
│   ├── frontend/
│   ├── backend/
│   └── compose/
├── docs/                     # Documentation
├── scripts/                  # Build, deploy, and utility scripts
├── .github/                  # GitHub Actions workflows
│   └── workflows/
├── .gitignore
├── README.md
├── package.json              # Root package configuration
├── pnpm-workspace.yaml       # Workspace configuration
└── turbo.json                # Build system configuration
```

## Package Descriptions

### Frontend Package (`packages/frontend`)
- **Framework**: Next.js 16+ with App Router
- **Language**: TypeScript
- **UI Components**: React components with Tailwind CSS
- **State Management**: React Context API or Zustand
- **HTTP Client**: Axios or Fetch API wrapper
- **Environment**: Node.js 18+ runtime

### Backend Package (`packages/backend`)
- **Framework**: FastAPI
- **Language**: Python 3.13+
- **Database ORM**: SQLModel
- **Authentication**: Better Auth with JWT
- **Database**: PostgreSQL (Neon Serverless)
- **Dependencies**: Managed via requirements.txt

### Shared Package (`packages/shared`)
- **Language**: TypeScript
- **Purpose**: Shared types and constants between frontend and backend
- **Contents**: API response types, validation schemas, utility functions

## Build and Development Configuration

### Package Manager
- **Tool**: pnpm (recommended for monorepos)
- **Workspace**: Defined in pnpm-workspace.yaml
- **Dependency Resolution**: Hoisted dependencies where possible

### Build System
- **Tool**: Turbo (for fast builds and caching)
- **Task Pipelines**: Defined in turbo.json
- **Caching**: Local and remote caching enabled
- **Parallel Execution**: Tasks run in parallel where possible

### Environment Configuration
- **Shared Variables**: Common environment variables in root
- **Package-Specific**: Individual package environment configurations
- **Secrets**: Secure handling through environment variables
- **Development**: Separate dev, staging, and production configurations

## Testing Strategy

### Frontend Testing
- **Unit Tests**: Jest with React Testing Library
- **Integration Tests**: Testing Library with MSW for API mocking
- **End-to-End**: Playwright or Cypress for critical user flows

### Backend Testing
- **Unit Tests**: pytest for individual function testing
- **Integration Tests**: Testing FastAPI endpoints with test database
- **Database Tests**: SQLModel-specific testing with test sessions

### Shared Testing
- **Type Validation**: Shared type definitions testing
- **Utility Functions**: Common utility function testing

## CI/CD Pipeline

### GitHub Actions
- **Trigger**: Push to main and PRs
- **Linting**: ESLint and Pylint for respective packages
- **Testing**: All test suites executed
- **Building**: Production builds for both packages
- **Deployment**: Automated to staging and production environments

### Quality Gates
- **Code Coverage**: Minimum 80% coverage required
- **Security Scanning**: Dependency vulnerability checks
- **Performance**: Bundle size and performance metrics
- **Linting**: All packages must pass linting

## Deployment Strategy

### Infrastructure
- **Frontend**: Vercel or Netlify for Next.js hosting
- **Backend**: Render, Railway, or AWS for FastAPI hosting
- **Database**: Neon Serverless PostgreSQL
- **CDN**: For static asset delivery

### Environments
- **Development**: Local development with hot reloading
- **Staging**: Pre-production environment matching production
- **Production**: Live user-facing environment
- **Feature**: Isolated environments for feature development

## Documentation Standards

### Code Documentation
- **Frontend**: JSDoc-style comments in TypeScript
- **Backend**: Google-style docstrings in Python
- **API**: OpenAPI/Swagger documentation via FastAPI
- **Components**: Storybook for component documentation

### Architecture Documentation
- **Decisions**: Architecture Decision Records (ADRs)
- **Specifications**: Feature specs in specs/ directory
- **Setup**: README files in each package
- **Workflows**: Development and deployment guides

## Collaboration Guidelines

### Branch Strategy
- **Main**: Production-ready code only
- **Feature Branches**: Individual features in specs/number-name format
- **Pull Requests**: Required for all changes to main
- **Code Review**: Minimum 1 reviewer per PR

### Code Standards
- **Frontend**: ESLint with TypeScript and React rules
- **Backend**: Pylint with Python best practices
- **Formatting**: Prettier for JS/TS, Black for Python
- **Commit Messages**: Conventional Commits specification