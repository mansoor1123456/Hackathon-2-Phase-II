# Database Schema Specification

## Overview
This document specifies the database schema for the multi-user todo application using SQLModel. The schema supports user authentication and personal todo management with proper relationships and constraints.

## Database Technology
- **Database**: Neon Serverless PostgreSQL
- **ORM**: SQLModel (SQLAlchemy + Pydantic integration)
- **Connection Pooling**: Default PostgreSQL connection pooling

## Entity Definitions

### User Table
Represents an authenticated user in the system

**Table Name**: `users`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY, NOT NULL | Unique identifier for the user |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User's email address (used for login) |
| name | VARCHAR(255) | NOT NULL | User's display name |
| password_hash | VARCHAR(255) | NOT NULL | Hashed password using secure algorithm |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Timestamp when user account was created |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Timestamp when user record was last updated |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | Whether the user account is active |

**Indexes**:
- `idx_users_email` on email (UNIQUE)
- `idx_users_created_at` on created_at

### Todo Table
Represents a todo item owned by a specific user

**Table Name**: `todos`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY, NOT NULL | Unique identifier for the todo |
| title | VARCHAR(255) | NOT NULL | Title of the todo item |
| description | TEXT | NULL | Optional description of the todo |
| completed | BOOLEAN | NOT NULL, DEFAULT FALSE | Whether the todo is completed |
| user_id | UUID | NOT NULL, FOREIGN KEY | Reference to the owning user |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Timestamp when todo was created |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Timestamp when todo was last updated |

**Indexes**:
- `idx_todos_user_id` on user_id (for efficient user todo queries)
- `idx_todos_completed` on completed (for filtering by status)
- `idx_todos_user_completed` on (user_id, completed) (composite index for common queries)

**Foreign Keys**:
- `fk_todos_user_id` → `users.id` (CASCADE DELETE: deleting user removes their todos)

## Relationships
- One User to Many Todos (one-to-many relationship)
- User owns zero or more Todos
- Todos are always associated with exactly one User

## Constraints
- All email addresses must be unique across the system
- Todo titles cannot be empty (minimum length of 1 character)
- User passwords must be properly hashed (no plain text storage)
- Todos can only be accessed by their owning user (enforced at application level)

## Indexing Strategy
- Primary keys automatically indexed
- Foreign key columns indexed for join performance
- Frequently queried columns (completed status, user_id) indexed
- Composite indexes for common query patterns

## Data Integrity
- Referential integrity enforced through foreign key constraints
- NOT NULL constraints on required fields
- UNIQUE constraints on business-critical fields (email)
- Automatic timestamp updates using database defaults

## Security Considerations
- Passwords stored as secure hashes only (never plain text)
- User isolation through proper foreign key relationships
- Access control enforced at application level based on user_id
- No sensitive data stored in plain text