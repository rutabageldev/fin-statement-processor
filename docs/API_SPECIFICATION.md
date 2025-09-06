# 📋 Ledgerly API Specification

## Overview

This document defines the REST API specification for Ledgerly MVP. The API follows REST principles and uses JSON for data exchange.

**Self-Documenting API**: FastAPI automatically generates interactive API documentation from code annotations, type hints, and Pydantic models. All endpoints include comprehensive request/response schemas, validation rules, and example data.

**Base URL**: `http://localhost:8000/api/v1`
**Authentication**: Bearer token (Phase 4+)
**Content-Type**: `application/json`
**Interactive Documentation**:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI Schema: `http://localhost:8000/openapi.json`

---

## 🔗 Core Endpoints

### **Statements Management**

#### `POST /statements`

Upload and parse financial statement files.

**Request**:

```http
POST /api/v1/statements
Content-Type: multipart/form-data

Fields:
- account_type: string (required) - Account type (e.g., "citi_cc")
- pdf_file: file (optional) - Statement PDF file
- csv_file: file (optional) - Transaction CSV file
- institution_id: string (optional) - UUID, defaults to account type default
```

**Response**: `201 Created`

```json
{
  "statement_id": "123e4567-e89b-12d3-a456-426614174000",
  "status": "processing",
  "uploaded_at": "2025-09-06T10:30:00Z",
  "files": {
    "pdf_url": "http://localhost:9000/ledgerly-statements/abc123.pdf?X-Amz-Expires=3600&X-Amz-Signature=...",
    "csv_url": "http://localhost:9000/ledgerly-statements/abc123.csv?X-Amz-Expires=3600&X-Amz-Signature=..."
  },
  "processing_info": {
    "estimated_completion": "2025-09-06T10:35:00Z",
    "progress_url": "/api/v1/statements/123e4567-e89b-12d3-a456-426614174000/status"
  }
}
```

**Error Responses**:

- `400 Bad Request` - Invalid file format or missing required fields
- `413 Payload Too Large` - File size exceeds limit (10MB)
- `422 Unprocessable Entity` - Parsing failed

---

#### `GET /statements`

List all statements with pagination and filtering.

**Query Parameters**:

- `page`: int (default: 1) - Page number
- `limit`: int (default: 20, max: 100) - Items per page
- `account_id`: UUID (optional) - Filter by account
- `institution_id`: UUID (optional) - Filter by institution
- `period_start`: date (optional) - Filter statements from this date
- `period_end`: date (optional) - Filter statements to this date
- `status`: string (optional) - Filter by processing status

**Response**: `200 OK`

```json
{
  "statements": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "institution_id": "456e7890-e89b-12d3-a456-426614174001",
      "account_id": "789e0123-e89b-12d3-a456-426614174002",
      "period_start": "2025-08-01",
      "period_end": "2025-08-31",
      "uploaded_at": "2025-09-06T10:30:00Z",
      "status": "completed",
      "files": {
        "pdf_url": "http://localhost:9000/ledgerly-statements/abc123.pdf?X-Amz-Expires=3600&X-Amz-Signature=...",
        "csv_url": "http://localhost:9000/ledgerly-statements/abc123.csv?X-Amz-Expires=3600&X-Amz-Signature=..."
      },
      "summary": {
        "transaction_count": 42,
        "total_credits": 150.0,
        "total_debits": -1250.75,
        "net_amount": -1100.75
      }
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 15,
    "pages": 1,
    "has_next": false,
    "has_prev": false
  }
}
```

---

#### `GET /statements/{statement_id}`

Get detailed information for a specific statement.

**Path Parameters**:

- `statement_id`: UUID (required) - Statement identifier

**Response**: `200 OK`

```json
{
  "statement": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "institution_id": "456e7890-e89b-12d3-a456-426614174001",
    "account_id": "789e0123-e89b-12d3-a456-426614174002",
    "period_start": "2025-08-01",
    "period_end": "2025-08-31",
    "uploaded_at": "2025-09-06T10:30:00Z",
    "status": "completed",
    "files": {
      "pdf_url": "http://localhost:9000/ledgerly-statements/abc123.pdf?X-Amz-Expires=3600&X-Amz-Signature=...",
      "csv_url": "http://localhost:9000/ledgerly-statements/abc123.csv?X-Amz-Expires=3600&X-Amz-Signature=..."
    }
  },
  "details": {
    "id": "details-uuid",
    "statement_id": "123e4567-e89b-12d3-a456-426614174000",
    "previous_balance": 245.5,
    "new_balance": -855.25
  },
  "credit_card_details": {
    "id": "cc-details-uuid",
    "account_id": "789e0123-e89b-12d3-a456-426614174002",
    "statement_id": "123e4567-e89b-12d3-a456-426614174000",
    "credit_limit": 5000.0,
    "available_credit": 4144.75,
    "points_earned": 1250,
    "points_redeemed": 0,
    "cash_advances": 0.0,
    "fees": 0.0,
    "purchases": 1100.75,
    "credits": -150.0
  },
  "summary": {
    "transaction_count": 42,
    "total_credits": 150.0,
    "total_debits": -1250.75,
    "net_amount": -1100.75,
    "categories": {
      "groceries": -450.25,
      "restaurants": -325.5,
      "gas": -180.0,
      "refunds": 150.0
    }
  }
}
```

**Error Responses**:

- `404 Not Found` - Statement not found
- `202 Accepted` - Statement still processing (include processing status)

---

#### `GET /statements/{statement_id}/status`

Get processing status for uploaded statement.

**Response**: `200 OK`

```json
{
  "statement_id": "123e4567-e89b-12d3-a456-426614174000",
  "status": "processing", // "processing", "completed", "failed"
  "progress": 75,
  "current_step": "parsing_transactions",
  "steps": [
    { "name": "file_validation", "status": "completed", "duration_ms": 150 },
    { "name": "pdf_parsing", "status": "completed", "duration_ms": 2300 },
    {
      "name": "parsing_transactions",
      "status": "in_progress",
      "duration_ms": null
    },
    { "name": "data_normalization", "status": "pending", "duration_ms": null },
    { "name": "database_storage", "status": "pending", "duration_ms": null }
  ],
  "estimated_completion": "2025-09-06T10:35:00Z",
  "error": null
}
```

---

### **Transactions Management**

#### `GET /transactions`

Get transactions with filtering and pagination.

**Query Parameters**:

- `page`: int (default: 1) - Page number
- `limit`: int (default: 50, max: 200) - Items per page
- `statement_id`: UUID (optional) - Filter by statement
- `account_id`: UUID (optional) - Filter by account
- `date_from`: date (optional) - Filter from date (YYYY-MM-DD)
- `date_to`: date (optional) - Filter to date (YYYY-MM-DD)
- `category`: string (optional) - Filter by category
- `type`: string (optional) - Filter by transaction type
- `min_amount`: float (optional) - Minimum transaction amount
- `max_amount`: float (optional) - Maximum transaction amount
- `search`: string (optional) - Search in description/custom_description
- `sort`: string (optional) - Sort field: "date", "amount", "description" (default: "date")
- `order`: string (optional) - Sort order: "asc", "desc" (default: "desc")

**Response**: `200 OK`

```json
{
  "transactions": [
    {
      "id": "trans-uuid-1",
      "statement_id": "123e4567-e89b-12d3-a456-426614174000",
      "account_id": "789e0123-e89b-12d3-a456-426614174002",
      "date": "2025-08-15",
      "amount": -125.5,
      "description": "WHOLE FOODS MARKET #12345",
      "custom_description": "Weekly groceries",
      "category": "groceries",
      "type": "debit"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 50,
    "total": 42,
    "pages": 1,
    "has_next": false,
    "has_prev": false
  },
  "summary": {
    "total_amount": -1100.75,
    "transaction_count": 42,
    "date_range": {
      "start": "2025-08-01",
      "end": "2025-08-31"
    }
  }
}
```

---

### **Analytics & Aggregations**

#### `GET /analytics/spending/monthly`

Get monthly spending breakdown.

**Query Parameters**:

- `account_id`: UUID (optional) - Filter by account
- `year`: int (required) - Year (e.g., 2025)
- `month`: int (optional) - Month (1-12), omit for full year
- `category`: string (optional) - Filter by specific category

**Response**: `200 OK`

```json
{
  "period": {
    "year": 2025,
    "month": 8,
    "start_date": "2025-08-01",
    "end_date": "2025-08-31"
  },
  "total_spending": -1100.75,
  "total_credits": 150.0,
  "net_amount": -950.75,
  "categories": [
    {
      "category": "groceries",
      "amount": -450.25,
      "percentage": 40.9,
      "transaction_count": 12
    },
    {
      "category": "restaurants",
      "amount": -325.5,
      "percentage": 29.6,
      "transaction_count": 8
    },
    {
      "category": "gas",
      "amount": -180.0,
      "percentage": 16.4,
      "transaction_count": 4
    },
    {
      "category": "refunds",
      "amount": 150.0,
      "percentage": -13.6,
      "transaction_count": 2
    }
  ],
  "daily_breakdown": [
    {
      "date": "2025-08-01",
      "amount": -45.2,
      "transaction_count": 2
    }
    // ... more daily entries
  ]
}
```

---

#### `GET /analytics/trends/categories`

Get category spending trends over time.

**Query Parameters**:

- `account_id`: UUID (optional) - Filter by account
- `period`: string (required) - "3months", "6months", "12months"
- `categories`: string (optional) - Comma-separated list of categories
- `granularity`: string (optional) - "daily", "weekly", "monthly" (default: "monthly")

**Response**: `200 OK`

```json
{
  "period": {
    "start_date": "2025-05-01",
    "end_date": "2025-08-31",
    "granularity": "monthly"
  },
  "categories": [
    {
      "category": "groceries",
      "trend": "increasing",
      "average_monthly": -425.33,
      "data_points": [
        {
          "period": "2025-05",
          "amount": -380.25,
          "transaction_count": 11
        },
        {
          "period": "2025-06",
          "amount": -445.5,
          "transaction_count": 13
        },
        {
          "period": "2025-07",
          "amount": -450.25,
          "transaction_count": 12
        },
        {
          "period": "2025-08",
          "amount": -450.25,
          "transaction_count": 12
        }
      ]
    }
  ],
  "totals": [
    {
      "period": "2025-05",
      "total_spending": -1050.75,
      "total_credits": 125.0
    }
    // ... more periods
  ]
}
```

---

## 🔧 Utility Endpoints

#### `GET /health`

Health check endpoint.

**Response**: `200 OK`

```json
{
  "status": "healthy",
  "timestamp": "2025-09-06T10:30:00Z",
  "version": "1.0.0",
  "services": {
    "database": "healthy",
    "file_storage": "healthy"
  }
}
```

---

#### `GET /account-types`

Get supported account types.

**Response**: `200 OK`

```json
{
  "account_types": [
    {
      "id": "citi_cc",
      "name": "Citi Credit Card",
      "supported_formats": ["pdf", "csv"],
      "institution": "Citibank"
    }
  ]
}
```

---

## 📁 Data Models

### **StatementData**

```typescript
interface StatementData {
  id: string; // UUID
  institution_id: string; // UUID
  account_id: string; // UUID
  period_start: string; // ISO date
  period_end: string; // ISO date
  file_url?: string; // URL to uploaded file
  uploaded_at: string; // ISO datetime
}
```

### **Transaction**

```typescript
interface Transaction {
  id: string; // UUID
  statement_id: string; // UUID
  account_id: string; // UUID
  date: string; // ISO date
  amount: number; // Positive for credits, negative for debits
  description: string; // Original transaction description
  custom_description?: string; // User-customized description
  category?: string; // Transaction category
  type: "debit" | "credit" | "payment" | "refund";
}
```

### **CreditCardDetails**

```typescript
interface CreditCardDetails {
  id: string; // UUID
  account_id: string; // UUID
  statement_id: string; // UUID
  credit_limit: number;
  available_credit: number;
  points_earned: number;
  points_redeemed: number;
  cash_advances: number;
  fees: number;
  purchases: number;
  credits: number;
}
```

---

## 🚨 Error Responses

### **Standard Error Format**

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid file format",
    "details": {
      "field": "pdf_file",
      "expected": "application/pdf",
      "received": "text/plain"
    },
    "request_id": "req_123456789"
  }
}
```

### **Common Error Codes**

- `VALIDATION_ERROR` - Request validation failed
- `FILE_TOO_LARGE` - Uploaded file exceeds size limit
- `UNSUPPORTED_FORMAT` - File format not supported
- `PARSING_FAILED` - Unable to parse uploaded file
- `STATEMENT_NOT_FOUND` - Requested statement doesn't exist
- `PROCESSING_ERROR` - Error during file processing
- `RATE_LIMIT_EXCEEDED` - Too many requests

---

## 🔒 Security Considerations

### **File Upload Security**

- Maximum file size: 10MB per file
- Allowed file types: PDF, CSV only
- Virus scanning on upload (ClamAV integration)
- Self-hosted object storage (MinIO S3-compatible)
- Pre-signed URLs with expiration (1 hour for downloads)
- Automatic file cleanup after 30 days
- Server-side encryption at rest (configurable)

### **Data Privacy**

- All financial data encrypted at rest
- Personal data anonymized in logs
- File access through signed URLs with expiration
- No sensitive data in query parameters

### **Rate Limiting**

- 100 requests per minute per IP
- 10 file uploads per hour per user
- 5 concurrent processing jobs per user

---

_Last Updated: September 6, 2025_
_API Version: v1_
