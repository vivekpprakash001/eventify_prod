# Eventify Plus API Documentation

**Base URL:** `https://uat.eventifyplus.com/api/`

**Version:** 1.0  
**Last Updated:** December 2025

---

## Table of Contents

1. [Authentication](#authentication)
2. [User APIs](#user-apis)
3. [Event APIs](#event-apis)
4. [Error Responses](#error-responses)

---

## Authentication

All API endpoints (except registration and login) require token-based authentication. The token must be included in the request body along with the username.

**Token Format:** The token is a string returned after successful login or registration.

---

## User APIs

### 1. User Registration

**Endpoint:** `POST /user/register/`

**Description:** Register a new user account.

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "phone_number": "+1234567890",
  "password": "securepassword123"
}
```

**Request Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| email | string | Yes | User's email address (must be unique) |
| phone_number | string | Yes | User's phone number (must be unique) |
| password | string | Yes | User's password |

**Success Response (201 Created):**
```json
{
  "message": "User registered successfully",
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

**Error Response (400 Bad Request):**
```json
{
  "errors": {
    "email": ["Email is already registered."],
    "phone_number": ["Phone number is already registered."]
  }
}
```

**Error Response (500 Internal Server Error):**
```json
{
  "error": "Error message here"
}
```

---

### 2. User Login

**Endpoint:** `POST /user/login/`

**Description:** Authenticate user and receive authentication token.

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "username": "user@example.com",
  "password": "securepassword123"
}
```

**Request Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| username | string | Yes | User's email or username |
| password | string | Yes | User's password |

**Note:** The `username` field accepts either email address or username.

**Success Response (200 OK):**
```json
{
  "message": "Login successful",
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "username": "john_doe",
  "email": "user@example.com",
  "phone_number": "+1234567890",
  "first_name": "John",
  "last_name": "Doe",
  "role": "staff",
  "pincode": "560001",
  "district": "Bangalore Urban",
  "state": "Karnataka",
  "country": "India",
  "place": "Bangalore",
  "latitude": "12.9716",
  "longitude": "77.5946"
}
```

**Error Response (401 Unauthorized):**
```json
{
  "errors": {
    "username": ["Invalid credentials."]
  }
}
```

**Error Response (500 Internal Server Error):**
```json
{
  "error": "Error message here"
}
```

---

### 3. Check User Status

**Endpoint:** `POST /user/status/`

**Description:** Verify if the authentication token is valid and get user status.

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "username": "john_doe"
}
```

**Request Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| token | string | Yes | Authentication token |
| username | string | Yes | User's username |

**Success Response (200 OK):**
```json
{
  "status": "logged_in",
  "username": "john_doe",
  "email": "user@example.com"
}
```

**Error Response (400 Bad Request):**
```json
{
  "status": "error",
  "message": "token and username required"
}
```

**Error Response (401 Unauthorized):**
```json
{
  "status": "invalid_token"
}
```

---

### 4. User Logout

**Endpoint:** `POST /user/logout/`

**Description:** Logout user and invalidate authentication token.

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "username": "john_doe"
}
```

**Request Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| token | string | Yes | Authentication token |
| username | string | Yes | User's username |

**Success Response (200 OK):**
```json
{
  "status": "logged_out",
  "message": "Logout successful"
}
```

**Error Response (400 Bad Request):**
```json
{
  "status": "error",
  "message": "token and username required"
}
```

**Error Response (401 Unauthorized):**
```json
{
  "status": "invalid_token"
}
```

---

## Event APIs

### 5. Get Event Types List

**Endpoint:** `POST events/type-list/`

**Description:** Retrieve list of all available event types with icons.

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "username": "john_doe"
}
```

**Request Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| token | string | Yes | Authentication token |
| username | string | Yes | User's username |

**Success Response (200 OK):**
```json
{
  "status": "success",
  "event_types": [
    {
      "id": 1,
      "event_type": "Concert",
      "event_type_icon": "https://uat.eventifyplus.com/media/event_type_icons/concert.png"
    },
    {
      "id": 2,
      "event_type": "Sports",
      "event_type_icon": "https://uat.eventifyplus.com/media/event_type_icons/sports.png"
    },
    {
      "id": 3,
      "event_type": "Conference",
      "event_type_icon": null
    }
  ]
}
```

**Error Response (400 Bad Request):**
```json
{
  "status": "error",
  "message": "token and username required"
}
```

**Error Response (401 Unauthorized):**
```json
{
  "status": "invalid_token"
}
```

---

### 6. Get Events by Pincode

**Endpoint:** `POST events/pincode-events/`

**Description:** Retrieve list of events filtered by pincode. If pincode is not provided or set to 'all', returns all events.

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "username": "john_doe",
  "pincode": "560001"
}
```

**Request Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| token | string | Yes | Authentication token |
| username | string | Yes | User's username |
| pincode | string | No | Pincode to filter events (optional, use 'all' or omit to get all events) |

**Success Response (200 OK):**
```json
{
  "status": "success",
  "events": [
    {
      "id": 1,
      "name": "Music Festival",
      "description": "Annual music festival",
      "start_date": "2025-06-15",
      "end_date": "2025-06-17",
      "start_time": "10:00:00",
      "end_time": "22:00:00",
      "latitude": "12.9716",
      "longitude": "77.5946",
      "pincode": "560001",
      "district": "Bangalore Urban",
      "state": "Karnataka",
      "place": "Bangalore",
      "is_bookable": true,
      "is_eventify_event": true,
      "outside_event_url": "NA",
      "event_type": 1,
      "event_status": "pending",
      "cancelled_reason": "NA",
      "title": "Summer Music Fest",
      "important_information": "Free parking available",
      "venue_name": "City Park",
      "thumb_img": "https://uat.eventifyplus.com/media/event_images/festival_thumb.jpg"
    }
  ]
}
```

**Error Response (400 Bad Request):**
```json
{
  "status": "error",
  "message": "token and username required"
}
```

**Error Response (401 Unauthorized):**
```json
{
  "status": "invalid_token"
}
```

---

### 7. Get Event Details

**Endpoint:** `POST events/event-details/`

**Description:** Retrieve detailed information about a specific event including all images.

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "username": "john_doe",
  "event_id": 1
}
```

**Request Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| token | string | Yes | Authentication token |
| username | string | Yes | User's username |
| event_id | integer | Yes | ID of the event |

**Success Response (200 OK):**
```json
{
  "id": 1,
  "name": "Music Festival",
  "description": "Annual music festival with multiple artists",
  "start_date": "2025-06-15",
  "end_date": "2025-06-17",
  "start_time": "10:00:00",
  "end_time": "22:00:00",
  "latitude": "12.9716",
  "longitude": "77.5946",
  "pincode": "560001",
  "district": "Bangalore Urban",
  "state": "Karnataka",
  "place": "Bangalore",
  "is_bookable": true,
  "is_eventify_event": true,
  "outside_event_url": "NA",
  "event_type": 1,
  "event_status": "pending",
  "cancelled_reason": "NA",
  "title": "Summer Music Fest",
  "important_information": "Free parking available",
  "venue_name": "City Park",
  "status": "success",
  "images": [
    {
      "is_primary": true,
      "image": "https://uat.eventifyplus.com/media/event_images/festival_main.jpg"
    },
    {
      "is_primary": false,
      "image": "https://uat.eventifyplus.com/media/event_images/festival_1.jpg"
    },
    {
      "is_primary": false,
      "image": "https://uat.eventifyplus.com/media/event_images/festival_2.jpg"
    }
  ]
}
```

**Error Response (400 Bad Request):**
```json
{
  "status": "error",
  "message": "token and username required"
}
```

**Error Response (401 Unauthorized):**
```json
{
  "status": "invalid_token"
}
```

---

### 8. Get Event Images

**Endpoint:** `POST events/event-images/`

**Description:** Retrieve list of all image URLs for a specific event.

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "username": "john_doe",
  "event_id": 1
}
```

**Request Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| token | string | Yes | Authentication token |
| username | string | Yes | User's username |
| event_id | integer | Yes | ID of the event |

**Success Response (200 OK):**
```json
{
  "status": "success",
  "images": [
    "https://uat.eventifyplus.com/media/event_images/festival_main.jpg",
    "https://uat.eventifyplus.com/media/event_images/festival_1.jpg",
    "https://uat.eventifyplus.com/media/event_images/festival_2.jpg"
  ]
}
```

**Error Response (400 Bad Request):**
```json
{
  "status": "error",
  "message": "token and username required"
}
```

**Error Response (401 Unauthorized):**
```json
{
  "status": "invalid_token"
}
```

---

### 9. Get Events by Category

**Endpoint:** `POST events/events-by-category/`

**Description:** Retrieve list of events filtered by event type/category ID.

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "username": "john_doe",
  "category_id": 1
}
```

**Request Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| token | string | Yes | Authentication token |
| username | string | Yes | User's username |
| category_id | integer | Yes | Event type/category ID |

**Success Response (200 OK):**
```json
{
  "status": "success",
  "events": [
    {
      "id": 1,
      "name": "Music Festival",
      "description": "Annual music festival",
      "start_date": "2025-06-15",
      "end_date": "2025-06-17",
      "event_type": 1,
      "event_image": "https://uat.eventifyplus.com/media/event_images/festival_main.jpg"
    }
  ]
}
```

**Error Response (400 Bad Request):**
```json
{
  "status": "error",
  "message": "token and username required"
}
```

**Error Response (400 Bad Request - Missing category_id):**
```json
{
  "status": "error",
  "message": "category_id is required"
}
```

**Error Response (401 Unauthorized):**
```json
{
  "status": "invalid_token"
}
```

---

### 10. Get Events by Month and Year

**Endpoint:** `POST events/events-by-month-year/`

**Description:** Retrieve events for a specific month and year with date-wise breakdown. Returns dates that have events, total count, and number of events per date.

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "username": "john_doe",
  "month": "August",
  "year": 2025
}
```

**Request Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| token | string | Yes | Authentication token |
| username | string | Yes | User's username |
| month | string | Yes | Month name (e.g., "August", "august", "Aug") |
| year | integer | Yes | Year (e.g., 2025) |

**Success Response (200 OK):**
```json
{
  "status": "success",
  "dates": [
    "2025-08-01",
    "2025-08-10",
    "2025-08-15"
  ],
  "total_number_of_events": 10,
  "date_events": [
    {
      "date_of_event": "2025-08-01",
      "events_of_date": 8
    },
    {
      "date_of_event": "2025-08-10",
      "events_of_date": 2
    },
    {
      "date_of_event": "2025-08-15",
      "events_of_date": 1
    }
  ]
}
```

**Error Response (400 Bad Request):**
```json
{
  "status": "error",
  "message": "month and year are required"
}
```

**Error Response (400 Bad Request - Invalid Month):**
```json
{
  "status": "error",
  "message": "Invalid month name: InvalidMonth"
}
```

**Error Response (401 Unauthorized):**
```json
{
  "status": "invalid_token"
}
```

---

### 11. Get Events by Date

**Endpoint:** `POST events/events-by-date/`

**Description:** Retrieve complete information for all events occurring on a specific date. Returns all event fields along with primary image thumbnails.

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "username": "john_doe",
  "date_of_event": "2025-08-15"
}
```

**Request Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| token | string | Yes | Authentication token |
| username | string | Yes | User's username |
| date_of_event | string | Yes | Date in YYYY-MM-DD format (e.g., "2025-08-15") |

**Success Response (200 OK):**
```json
{
  "status": "success",
  "events": [
    {
      "id": 1,
      "created_date": "2025-07-01",
      "name": "Music Festival",
      "description": "Annual music festival with multiple artists",
      "start_date": "2025-08-10",
      "end_date": "2025-08-20",
      "start_time": "10:00:00",
      "end_time": "22:00:00",
      "latitude": "12.9716",
      "longitude": "77.5946",
      "pincode": "560001",
      "district": "Bangalore Urban",
      "state": "Karnataka",
      "place": "Bangalore",
      "is_bookable": true,
      "is_eventify_event": true,
      "outside_event_url": "NA",
      "event_type": 1,
      "event_status": "pending",
      "cancelled_reason": "NA",
      "title": "Summer Music Fest",
      "important_information": "Free parking available",
      "venue_name": "City Park",
      "thumb_img": "https://uat.eventifyplus.com/media/event_images/festival_thumb.jpg"
    },
    {
      "id": 2,
      "created_date": "2025-07-05",
      "name": "Sports Championship",
      "description": "Regional sports championship",
      "start_date": "2025-08-15",
      "end_date": "2025-08-15",
      "start_time": "09:00:00",
      "end_time": "18:00:00",
      "latitude": "12.9352",
      "longitude": "77.6245",
      "pincode": "560001",
      "district": "Bangalore Urban",
      "state": "Karnataka",
      "place": "Bangalore",
      "is_bookable": false,
      "is_eventify_event": true,
      "outside_event_url": "NA",
      "event_type": 2,
      "event_status": "pending",
      "cancelled_reason": "NA",
      "title": "Regional Sports Championship",
      "important_information": "Entry fee required",
      "venue_name": "Sports Complex",
      "thumb_img": "https://uat.eventifyplus.com/media/event_images/sports_thumb.jpg"
    }
  ]
}
```

**Error Response (400 Bad Request - Missing date_of_event):**
```json
{
  "status": "error",
  "message": "date_of_event is required"
}
```

**Error Response (400 Bad Request - Invalid Date Format):**
```json
{
  "status": "error",
  "message": "Invalid date format. Expected YYYY-MM-DD"
}
```

**Error Response (400 Bad Request - Missing Credentials):**
```json
{
  "status": "error",
  "message": "token and username required"
}
```

**Error Response (401 Unauthorized):**
```json
{
  "status": "invalid_token"
}
```

---

## Error Responses

### Common Error Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 201 | Created (Registration successful) |
| 400 | Bad Request (Missing or invalid parameters) |
| 401 | Unauthorized (Invalid token or credentials) |
| 500 | Internal Server Error |

### Standard Error Response Format

```json
{
  "status": "error",
  "message": "Error description here"
}
```

### Authentication Errors

**Invalid Token:**
```json
{
  "status": "invalid_token"
}
```

**Token Mismatch:**
```json
{
  "status": "error",
  "message": "token does not match user"
}
```

**Missing Credentials:**
```json
{
  "status": "error",
  "message": "token and username required"
}
```

---

## Notes

1. **Authentication:** All endpoints except registration and login require a valid token in the request body.

2. **Content-Type:** All requests must include `Content-Type: application/json` header.

3. **Date Format:** Dates are returned in `YYYY-MM-DD` format. The `date_of_event` parameter in `events-by-date` endpoint must also be provided in `YYYY-MM-DD` format.

4. **Time Format:** Times are returned in `HH:MM:SS` format (24-hour).

5. **Image URLs:** All image URLs are returned as absolute URLs starting with the base URL.

6. **Pincode Filter:** The pincode parameter in `pincode-events` endpoint is optional. Omit it or set to `'all'` to retrieve all events.

7. **Month Names:** The month parameter accepts full month names (e.g., "August") or abbreviations (e.g., "Aug"), case-insensitive.

8. **Multi-day Events:** Events that span multiple days will be counted for each day they occur in the specified month. The `events-by-date` endpoint returns all events where the specified date falls between the event's `start_date` and `end_date` (inclusive).

---

## Support

For API support or questions, please contact the development team.

**API Base URL:** `https://uat.eventifyplus.com/api/`

---

*Document Version: 1.0*  
*Last Updated: December 2025*

