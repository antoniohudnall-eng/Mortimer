# Collections Module - Deployment Guide

## Quick Start

```bash
# 1. Install dependencies
npm install

# 2. Configure environment
cp .env.example .env
# Edit .env with your credentials

# 3. Run database migrations
npm run migrate

# 4. Start the service
npm start
```

## Environment Configuration

Create `.env` file:

```bash
# Required Settings
NODE_ENV=production
PORT=3000
TIER=professional  # starter|professional|corporate|enterprise

# Database
DATABASE_URL=postgresql://user:pass@host:5432/collections
REDIS_URL=redis://localhost:6379

# Email (SendGrid)
SENDGRID_API_KEY=SG.xxx
FROM_EMAIL=collections@psdepot.com
FROM_NAME="Collections Department"

# SMS (Twilio)
TWILIO_SID=AC.xxx
TWILIO_AUTH_TOKEN=xxx
TWILIO_PHONE=+18007336801

# Payment Processing (Stripe)
STRIPE_SECRET_KEY=sk_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx

# Optional
LOG_LEVEL=info
MAX_ACCOUNTS=2000
SLA_HOURS=48
WEBHOOK_SECRET=your_webhook_secret
```

## Database Setup

### PostgreSQL

```sql
CREATE DATABASE collections;
CREATE USER collections_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE collections TO collections_user;
```

### Redis

```bash
# Install Redis
sudo apt-get install redis-server

# Start Redis
sudo systemctl start redis-server

# Verify
redis-cli ping
```

## Production Deployment

### Using Docker

```bash
# Build image
docker build -t psdepot-collections:latest .

# Run container
docker run -d \
  --name collections \
  -p 3000:3000 \
  --env-file .env \
  psdepot-collections:latest
```

### Using Docker Compose

```yaml
version: '3.8'
services:
  collections:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
    env_file:
      - .env
    depends_on:
      - postgres
      - redis
    restart: unless-stopped
    
  postgres:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_USER: collections
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: collections
    restart: unless-stopped
    
  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    restart: unless-stopped
    
volumes:
  postgres_data:
  redis_data:
```

### Using PM2

```bash
# Install PM2
npm install -g pm2

# Create ecosystem file
pm2 ecosystem

# Start with PM2
pm2 start ecosystem.config.js

# Save PM2 config
pm2 save
pm2 startup
```

`ecosystem.config.js`:

```javascript
module.exports = {
  apps: [{
    name: 'collections',
    script: './src/index.js',
    instances: 'max',
    exec_mode: 'cluster',
    env: {
      NODE_ENV: 'production',
      PORT: 3000
    },
    error_file: './logs/err.log',
    out_file: './logs/out.log',
    log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
    merge_logs: true,
    max_memory_restart: '1G'
  }]
};
```

## SSL/TLS Configuration

### Using Nginx Reverse Proxy

```nginx
server {
    listen 443 ssl http2;
    server_name collections.psdepot.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}

server {
    listen 80;
    server_name collections.psdepot.com;
    return 301 https://$server_name$request_uri;
}
```

## Health Checks

```bash
# API Health
curl http://localhost:3000/health

# Database Health
curl http://localhost:3000/health/db

# Full System Status
curl http://localhost:3000/health/detailed
```

## Monitoring

### Setup Prometheus Metrics

```bash
# Metrics endpoint
curl http://localhost:3000/metrics
```

### Log Rotation

```bash
# Install logrotate
sudo apt-get install logrotate

# Create config
sudo tee /etc/logrotate.d/collections << 'EOF'
/var/log/collections/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 0644 root root
    sharedscripts
    postrotate
        pm2 reload collections
    endscript
}
EOF
```

## Troubleshooting

### Common Issues

**Database Connection Failed:**
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Check connection
psql -h localhost -U collections_user -d collections

# Check logs
sudo tail -f /var/log/postgresql/postgresql.log
```

**Redis Connection Failed:**
```bash
# Check Redis is running
sudo systemctl status redis-server

# Test connection
redis-cli ping
```

**Port Already in Use:**
```bash
# Find process using port 3000
sudo lsof -i :3000

# Kill process
sudo kill -9 <PID>
```

## Backup & Recovery

### Database Backup

```bash
# Daily backup script
#!/bin/bash
BACKUP_DIR="/backups/collections"
DATE=$(date +%Y%m%d_%H%M%S)
FILENAME="collections_backup_${DATE}.sql"

pg_dump -h localhost -U collections_user collections > ${BACKUP_DIR}/${FILENAME}
gzip ${BACKUP_DIR}/${FILENAME}

# Keep only last 30 days
find ${BACKUP_DIR} -name "collections_backup_*.sql.gz" -mtime +30 -delete
```

### Restore from Backup

```bash
# Restore database
psql -h localhost -U collections_user -d collections < collections_backup_20260612.sql
```

## Security Hardening

### Firewall Rules

```bash
# Allow only necessary ports
sudo ufw default deny incoming
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

### File Permissions

```bash
# Set proper permissions
chmod 600 .env
chmod 755 src/
chmod 644 src/*.js
```

---

For support: collections@psdepot.com
