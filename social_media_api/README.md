# Social Media API

A Django REST Framework-based Social Media API with user authentication, posts, comments, follows, and notifications.

## Features

- User registration and authentication with JWT
- User profiles with bio and profile pictures
- Follow/Unfollow functionality
- Posts and comments
- Notifications for interactions
- RESTful API design

## Setup Instructions

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run migrations: `python manage.py migrate`
6. Create a superuser: `python manage.py createsuperuser`
7. Run the development server: `python manage.py runserver`

## API Endpoints

### Authentication
- `POST /api/auth/register/` - Register a new user
- `POST /api/auth/login/` - Login user and get tokens
- `GET /api/auth/profile/` - Get user profile (authenticated)
- `PUT /api/auth/profile/` - Update user profile (authenticated)

### Example Requests

#### Register a new user
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "password2": "testpass123",
    "bio": "Test user bio"
  }'

## Posts Endpoints

### List Posts
- **URL**: `/api/posts/`
- **Method**: `GET`
- **Authentication**: Required
- **Query Parameters**:
  - `search`: Search in title and content
  - `ordering`: Order by fields (created_at, updated_at, likes_count)
  - `page`: Page number for pagination

### Create Post
- **URL**: `/api/posts/`
- **Method**: `POST`
- **Authentication**: Required
- **Body**:
  ```json
  {
    "title": "Post Title",
    "content": "Post content"
  }

