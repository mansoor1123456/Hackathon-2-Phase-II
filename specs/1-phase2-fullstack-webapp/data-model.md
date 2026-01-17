# Data Model: Phase II - Full-Stack Web Application

## Entity: User
**Fields:**
- id: UUID (Primary Key, auto-generated)
- email: String (255 chars, unique, not null)
- name: String (255 chars, not null)
- password_hash: String (255 chars, not null)
- created_at: DateTime (not null, default now())
- updated_at: DateTime (not null, default now())
- is_active: Boolean (not null, default true)

**Relationships:**
- One-to-Many: User → Todo (user has many todos)

**Validation Rules:**
- Email must be valid email format
- Name must be 1-255 characters
- Password must be properly hashed before storage
- Email must be unique across all users

## Entity: Todo
**Fields:**
- id: UUID (Primary Key, auto-generated)
- title: String (255 chars, not null)
- description: Text (optional)
- completed: Boolean (not null, default false)
- user_id: UUID (Foreign Key to User.id, not null)
- created_at: DateTime (not null, default now())
- updated_at: DateTime (not null, default now())

**Relationships:**
- Many-to-One: Todo → User (todo belongs to one user)
- User owns zero or more Todos
- Todos are always associated with exactly one User

**Validation Rules:**
- Title must be 1-255 characters
- User_id must reference an existing active user
- Completed status is boolean (true/false)
- Only the owner user can modify or delete the todo

## State Transitions

### Todo State Transitions:
- **Incomplete** → **Complete**: When user marks todo as done
- **Complete** → **Incomplete**: When user marks todo as undone

### User State Transitions:
- **Inactive** → **Active**: When account is created/activated
- **Active** → **Inactive**: When account is deactivated (soft delete)

## Indexes
- User.email: Unique index for efficient login lookup
- Todo.user_id: Index for efficient user todo queries
- Todo.completed: Index for filtering by completion status
- Todo.user_id + Todo.completed: Composite index for common queries