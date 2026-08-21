# Dusty MVP API Reference

## Core Agent (Port 3000)

### GET /status
Returns service status.

Response:
```json
{
  "ok": true,
  "status": "idle",
  "timestamp": "2026-02-18T03:15:51.256Z"
}
```

### POST /tasks
Create a new task.

Request:
```json
{
  "type": "dust_check",
  "payload": {"user": "alice"}
}
```

Response:
```json
{
  "ok": true,
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending"
}
```

### GET /tasks/:id
Get task details.

### POST /tasks/:id/complete
Mark task as completed.

## Bridge Mock (Port 3001)

### POST /webhook
Receive Telegram webhook messages.

Request:
```json
{
  "message": {
    "from": {"username": "testuser"},
    "chat": {"id": 123},
    "text": "Hello!"
  }
}
```

### GET /health
Health check endpoint.

### GET /test
Send test message to core-agent.

## OpenClaw Mock (Port 4000)

### POST /receive_message
Receive messages from core-agent, return Dusty responses.

### GET /status
Health check.

### GET /logs
View interaction history.
