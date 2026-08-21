# Alert Configuration

## Webhook Alerts

Send alerts to Slack/Discord webhook on failure:

```bash
export ALERT_WEBHOOK="https://hooks.slack.com/services/..."
export ALERT_CHANNEL="#alerts"
```

## Email Alerts

Configure SMTP for email notifications:

```bash
export SMTP_HOST="smtp.gmail.com"
export SMTP_PORT="587"
export SMTP_USER="alerts@example.com"
export SMTP_PASS="app-password"
export ALERT_EMAIL="ops@example.com"
```

## Alert Thresholds

- **Warning**: Service responds but slow (> 2s)
- **Critical**: Service not responding or HTTP 5xx
- **Recovery**: Service back to healthy

## Rate Limiting

Send max 1 alert per 5 minutes per service to prevent spam.
