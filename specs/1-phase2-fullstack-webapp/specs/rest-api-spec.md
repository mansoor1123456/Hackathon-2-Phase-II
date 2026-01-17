# REST API Specification

## Overview
This document specifies the RESTful API endpoints for the multi-user todo application. The API follows standard REST conventions and supports all necessary operations for user management and todo CRUD operations.

## Base URL
`https://api.example.com/v1`

## Authentication
All endpoints (except authentication) require a valid JWT token in the Authorization header:
```
Authorization: Bearer <jwt_token>
```

## API Endpoints

### User Authentication

#### POST /auth/register
Register a new user account
- **Description**: Creates a new user account with provided credentials
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "secure_password",
    "name": "User Name"
  }
  ```
- **Response Codes**:
  - 201: Account created successfully
  - 400: Invalid input data
  - 409: Email already exists
- **Response Body** (201):
  ```json
  {
    "id": "user_id",
    "email": "user@example.com",
    "name": "User Name",
    "created_at": "2026-01-08T10:00:00Z"
  }
  ```

#### POST /auth/login
Authenticate user and return JWT token
- **Description**: Validates user credentials and returns authentication token
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "secure_password"
  }
  ```
- **Response Codes**:
  - 200: Login successful
  - 400: Invalid input data
  - 401: Invalid credentials
- **Response Body** (200):
  ```json
  {
    "token": "jwt_token",
    "user": {
      "id": "user_id",
      "email": "user@example.com",
      "name": "User Name"
    }
  }
  ```

#### POST /auth/logout
Terminate user session
- **Description**: Invalidates the current user session
- **Response Codes**:
  - 200: Logout successful
  - 401: Invalid or expired token

### Todo Operations

#### GET /todos
Retrieve all todos for the authenticated user
- **Description**: Returns a list of all todos belonging to the authenticated user
- **Query Parameters**:
  - `limit`: Number of items to return (default: 20, max: 100)
  - `offset`: Number of items to skip (default: 0)
  - `status`: Filter by completion status ('all', 'completed', 'incomplete') (default: 'all')
- **Response Codes**:
  - 200: Todos retrieved successfully
  - 401: Unauthorized access
- **Response Body** (200):
  ```json
  {
    "todos": [
      {
        "id": "todo_id",
        "title": "Todo Title",
        "description": "Todo Description",
        "completed": false,
        "created_at": "2026-01-08T10:00:00Z",
        "updated_at": "2026-01-08T10:00:00Z"
      }
    ],
    "total_count": 1,
    "limit": 20,
    "offset": 0
  }
  ```

#### POST /todos
Create a new todo for the authenticated user
- **Description**: Creates a new todo associated with the authenticated user
- **Request Body**:
  ```json
  {
    "title": "Todo Title",
    "description": "Todo Description"
  }
  ```
- **Response Codes**:
  - 201: Todo created successfully
  - 400: Invalid input data
  - 401: Unauthorized access
- **Response Body** (201):
  ```json
  {
    "id": "todo_id",
    "title": "Todo Title",
    "description": "Todo Description",
    "completed": false,
    "created_at": "2026-01-08T10:00:00Z",
    "updated_at": "2026-01-08T10:00:00Z",
    "user_id": "user_id"
  }
  ```

#### GET /todos/{id}
Retrieve a specific todo
- **Description**: Returns details of a specific todo if it belongs to the authenticated user
- **Path Parameter**:
  - `id`: The ID of the todo to retrieve
- **Response Codes**:
  - 200: Todo retrieved successfully
  - 401: Unauthorized access
  - 404: Todo not found
- **Response Body** (200):
  ```json
  {
    "id": "todo_id",
    "title": "Todo Title",
    "description": "Todo Description",
    "completed": false,
    "created_at": "2026-01-08T10:00:00Z",
    "updated_at": "2026-01-08T10:00:00Z",
    "user_id": "user_id"
  }
  ```

#### PUT /todos/{id}
Update a specific todo
- **Description**: Updates the details of a specific todo if it belongs to the authenticated user
- **Path Parameter**:
  - `id`: The ID of the todo to update
- **Request Body**:
  ```json
  {
    "title": "Updated Todo Title",
    "description": "Updated Todo Description",
    "completed": true
  }
  ```
- **Response Codes**:
  - 200: Todo updated successfully
  - 400: Invalid input data
  - 401: Unauthorized access
  - 404: Todo not found
- **Response Body** (200):
  ```json
  {
    "id": "todo_id",
    "title": "Updated Todo Title",
    "description": "Updated Todo Description",
    "completed": true,
    "created_at": "2026-01-08T10:00:00Z",
    "updated_at": "2026-01-08T11:00:00Z",
    "user_id": "user_id"
  }
  ```

#### DELETE /todos/{id}
Delete a specific todo
- **Description**: Permanently deletes a specific todo if it belongs to the authenticated user
- **Path Parameter**:
  - `id`: The ID of the todo to delete
- **Response Codes**:
  - 204: Todo deleted successfully
  - 401: Unauthorized access
  - 404: Todo not found

## Error Responses
All error responses follow this structure:
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": "Additional error details if applicable"
  }
}
```

## Rate Limiting
- Authenticated endpoints: 100 requests per minute per user
- Unauthenticated endpoints: 10 requests per minute per IP

## CORS Policy
- Allowed origins: Specific frontend domains only
- Allowed methods: GET, POST, PUT, DELETE
- Credentials: Allowed