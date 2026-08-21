# Technical Architect Skill
## Performance Supply Depot LLC

**Role:** Chief Software Architect, Backend Engineer, Mobile Developer, QA  
**Agents:** Stacktrace, Pipeline, Taptap, Bugcatcher  
**Deterministic:** Yes — Not theoretical  
**Certification:** Required Week 2

---

## Overview

Build and maintain robust, scalable, deterministic systems for business operations.

### Key Principles
1. **Deterministic over theoretical** — Code must work predictably
2. **Observable** — Every system has logging and monitoring
3. **Recoverable** — Failure modes are handled gracefully
4. **Secure** — Security by design, not afterthought

---

## Core Skills

### 1. API Design (Pipeline)

**RESTful Endpoints:**
```javascript
// Required structure
{
  "GET /api/v1/{resource}": "List all",
  "GET /api/v1/{resource}/:id": "Get one",
  "POST /api/v1/{resource}": "Create",
  "PUT /api/v1/{resource}/:id": "Update",
  "DELETE /api/v1/{resource}/:id": "Delete",
  "GET /api/v1/{resource}/:id/status": "Health check"
}
```

**Required Headers:**
```
Content-Type: application/json
Authorization: Bearer {token}
X-Request-ID: {uuid}
```

**Response Format:**
```json
{
  "success": true,
  "data": {},
  "error": null,
  "timestamp": "ISO-8601",
  "request_id": "uuid"
}
```

### 2. Service Health Patterns (Stacktrace)

**Health Check Endpoint:**
```python
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "uptime": get_uptime(),
        "version": VERSION,
        "dependencies": {
            "database": check_db(),
            "cache": check_cache(),
            "external_api": check_external()
        }
    }
```

**Circuit Breaker Pattern:**
```python
class CircuitBreaker:
    def __init__(self, threshold=5, timeout=60):
        self.threshold = threshold
        self.timeout = timeout
        self.failures = 0
        self.last_failure = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
    
    def call(self, func):
        if self.state == "OPEN":
            if time.time() - self.last_failure > self.timeout:
                self.state = "HALF_OPEN"
            else:
                raise CircuitBreakerOpen()
        
        try:
            result = func()
            self.on_success()
            return result
        except Exception as e:
            self.on_failure()
            raise e
```

### 3. Mobile Development (Taptap)

**Android (DroidScript) Standards:**
```javascript
// App structure
app.LoadScript("ui.js");
app.LoadScript("api.js");
app.LoadScript("storage.js");

// Required lifecycle handling
function OnStart() {
    initializeUI();
    checkConnectivity();
    loadCachedData();
}

function OnPause() {
    saveState();
    disconnect();
}

function OnResume() {
    reconnect();
    syncData();
}

// Offline support
function saveLocal(key, data) {
    app.SaveText(key, JSON.stringify(data));
}

function loadLocal(key) {
    return JSON.parse(app.LoadText(key, "{}"));
}
```

### 4. Testing (Bugcatcher)

**Unit Test Pattern:**
```python
def test_feature():
    # Arrange
    input_data = create_test_data()
    expected = expected_output()
    
    # Act
    result = function_under_test(input_data)
    
    # Assert
    assert result == expected, f"Expected {expected}, got {result}"
```

**Integration Test Pattern:**
```python
def test_api_endpoint():
    # Given
    request = build_request()
    
    # When
    response = api.call(request)
    
    # Then
    assert response.status == 200
    assert response.data is not None
    assert validate_schema(response.data)
```

**E2E Test Pattern:**
```python
def test_full_workflow():
    # Complete user journey
    user = create_user()
    order = place_order(user)
    payment = process_payment(order)
    confirmation = send_confirmation(payment)
    
    assert order.status == "confirmed"
    assert payment.processed == True
    assert confirmation.sent == True
```

### 5. Error Handling

**Standard Error Structure:**
```json
{
  "error": {
    "code": "ERR_INVALID_INPUT",
    "message": "Human-readable description",
    "details": {},
    "timestamp": "ISO-8601",
    "request_id": "uuid",
    "action_required": "What to do next"
  }
}
```

**Error Codes:**
- `ERR_INVALID_INPUT` — 400
- `ERR_UNAUTHORIZED` — 401
- `ERR_FORBIDDEN` — 403
- `ERR_NOT_FOUND` — 404
- `ERR_RATE_LIMIT` — 429
- `ERR_INTERNAL` — 500
- `ERR_SERVICE_UNAVAILABLE` — 503

---

## Architecture Standards

### Service Separation
```
services/
├── api-gateway/        # Entry point
├── auth-service/       # Authentication
├── sales-service/      # Orders, quotes
├── inventory-service/  # Products, stock
├── notification-service/  # Email, SMS
└── monitoring-service/    # Health, metrics
```

### Data Flow
```
Client → Gateway → Service → Database
            ↓
        Cache (Redis)
            ↓
        Message Queue (optional)
```

### Logging Requirements
Every service must log:
```json
{
  "timestamp": "ISO-8601",
  "level": "INFO|WARN|ERROR",
  "service": "service-name",
  "request_id": "uuid",
  "user_id": "identifier",
  "action": "what_happened",
  "duration_ms": 123,
  "error": null
}
```

---

## Deployment Standards

### Container Requirements
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s CMD curl -f http://localhost:3000/health || exit 1
CMD ["node", "server.js"]
```

### Environment Variables
```
NODE_ENV=production
PORT=3000
DB_URL=
REDIS_URL=
JWT_SECRET=
LOG_LEVEL=info
```

---

## Security Requirements

### Input Validation
```javascript
function validateInput(data, schema) {
    // Check type
    // Check range
    // Check format (regex)
    // Sanitize (escape HTML, remove null bytes)
    return sanitized;
}
```

### Authentication
- JWT tokens with 24h expiry
- Refresh tokens with 7d expiry
- Rate limiting: 100 req/min per IP
- CORS configured for known origins only

### Secrets Management
- No secrets in code
- Use environment variables
- Rotate credentials quarterly
- Audit access to vault

---

## Certification Test (Week 2)

1. Build a complete API with health checks
2. Implement circuit breaker pattern
3. Write unit + integration tests
4. Containerize the service
5. Demonstrate error handling
6. Pass security review

**Passing Criteria:**
- All tests pass
- Coverage > 80%
- No critical security issues
- Service runs for 24h without failure

---

*"Code is guilty until proven innocent — by tests."*
