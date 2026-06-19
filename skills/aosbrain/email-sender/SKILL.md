# Email Sender Skill

Send emails using Miles' Hostinger account (miles@myl0nr0s.cloud).

## Credentials (Stored Securely)
- **Email:** miles@myl0nr0s.cloud
- **SMTP:** smtp.hostinger.com:587
- **Password:** [loaded from .miles_email_creds]

## Usage
```python
from skills.email-sender import send_email

send_email(
    to="recipient@example.com",
    subject="Subject Line",
    body="Plain text body",
    html_body="<h1>HTML body</h1>",
    attachments=["/path/to/file.pdf"]
)
```

## Rate Limits
- Hostinger: Max 100 emails/hour
- Internal throttle: 1 email per 5 minutes to same recipient

## Security
- Credentials loaded from ~/.miles_email_creds (600 permissions)
- Never log passwords
- TLS encryption enforced
