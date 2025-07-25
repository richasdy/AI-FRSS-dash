# AI-FRSS Mobile API Documentation

## Overview

AI-FRSS Mobile API v1 provides authentication and face recognition services for mobile applications.

## Base URL

```
http://localhost:8000/api/mobile/v1
```

## Authentication Endpoints

### POST /auth/signup

Register a new admin user.

**Request Body:**

```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response:**

```json
{
  "type": "insert_admin",
  "success": true,
  "message": "Admin registered successfully"
}
```

### POST /auth/login

Login admin user and get JWT token.

**Request Body:**

```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response:**

```json
{
  "type": "login",
  "success": true,
  "message": "Login successful",
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "admin": {
    "id": 1,
    "username": "admin"
  }
}
```

## Face Recognition Endpoints

### POST /faces/verify

Verify face against registered faces in database.

**Request Body:**

```json
{
  "embedding": [0.1, 0.2, 0.3, ..., 0.512]
}
```

**Response (Match Found):**

```json
{
  "type": "recognize_face",
  "match": true,
  "name": "John Doe",
  "distance": 0.75,
  "face_id": 1
}
```

**Response (No Match):**

```json
{
  "type": "recognize_face",
  "match": false,
  "name": null,
  "distance": null,
  "face_id": null
}
```

### POST /faces/insert

Register a new face in the database.

**Request Body:**

```json
{
  "name": "John Doe",
  "embedding": [0.1, 0.2, 0.3, ..., 0.512]
}
```

**Response:**

```json
{
  "type": "insert_face",
  "success": true,
  "message": "Face registered successfully for John Doe",
  "face_id": 1
}
```

## Error Responses

### 400 Bad Request

```json
{
  "detail": "Validation error message"
}
```

### 401 Unauthorized

```json
{
  "detail": "Invalid credentials"
}
```

### 500 Internal Server Error

```json
{
  "detail": "Server error description"
}
```

## Notes

1. **Face Embeddings**: Must be arrays of float numbers with minimum 128 features
2. **Distance Threshold**: Default threshold for face matching is 0.9 (lower = more similar)
3. **JWT Tokens**: Valid for 7 days from issue date
4. **Username Requirements**: 3-50 characters
5. **Password Requirements**: Minimum 6 characters

## Testing

You can test the API using the interactive documentation at:

```
http://localhost:8000/docs
```

Or using curl:

```bash
# Test login
curl -X POST "http://localhost:8000/api/mobile/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# Test face verification
curl -X POST "http://localhost:8000/api/mobile/v1/faces/verify" \
  -H "Content-Type: application/json" \
  -d '{"embedding": [0.1, 0.2, ...]}'
```
