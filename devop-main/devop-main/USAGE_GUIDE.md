# 🚀 Website Uptime Monitor - Usage Guide

## Quick Start

### 1. Basic Monitoring
```bash
# Run the monitor with default websites
python monitor.py

# Monitor custom websites
set WEBSITES_TO_MONITOR=https://yoursite.com,https://anothersite.com
python monitor.py
```

### 2. With Docker
```bash
# Build and run
docker build -t uptime-monitor .
docker run -e WEBSITES_TO_MONITOR="https://google.com,https://github.com" uptime-monitor

# Or use Docker Compose for full stack
docker-compose up -d
```

### 3. Test the System
```bash
# Run comprehensive test
python test_system.py
```

## Configuration Options

### Environment Variables
```bash
# Websites to monitor (comma-separated)
WEBSITES_TO_MONITOR=https://site1.com,https://site2.com

# Email alerts
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
EMAIL_TO=alerts@yourcompany.com

# Slack alerts
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK
```

### Configuration File (.env)
```bash
# Copy example and customize
cp .env.example .env
# Edit .env with your settings
```

## Monitoring Features

### ✅ What Gets Monitored
- **HTTP/HTTPS websites** - Any web URL
- **Response time** - Measured in milliseconds  
- **Status codes** - 200, 404, 500, etc.
- **Connection errors** - Timeouts, DNS failures
- **Timestamps** - When each check occurred

### 📊 Data Output
- **JSON results** - `uptime_results.json`
- **Log files** - `uptime_monitor.log`
- **Prometheus metrics** - `/metrics` endpoint
- **Console output** - Real-time status

### 🚨 Alert Channels
- **Email** - SMTP notifications
- **Slack** - Webhook integration
- **Logs** - Detailed error logging

## Docker Deployment

### Single Container
```bash
# Build
docker build -t uptime-monitor .

# Run with custom sites
docker run -d \
  --name monitor \
  -e WEBSITES_TO_MONITOR="https://example.com" \
  -v $(pwd)/logs:/app/logs \
  uptime-monitor
```

### Full Stack (Recommended)
```bash
# Start everything
docker-compose up -d

# Access services
# - Grafana: http://localhost:3000 (admin/admin123)
# - Prometheus: http://localhost:9090
# - Metrics: http://localhost:8000/metrics

# View logs
docker-compose logs -f uptime-monitor
```

## GitHub Actions CI/CD

### Automatic Monitoring
- Runs **every 30 minutes** automatically
- Uploads logs as artifacts
- Supports custom website lists

### Manual Execution
1. Go to **Actions** tab in GitHub
2. Select **Website Uptime Monitor**
3. Click **Run workflow**
4. Optionally specify custom websites

### Setup Secrets
Add these to your GitHub repository secrets:
- `EMAIL_USER` - Your email
- `EMAIL_PASSWORD` - App password
- `EMAIL_TO` - Alert recipient
- `SLACK_WEBHOOK_URL` - Slack webhook

## Prometheus & Grafana

### Metrics Available
```
website_up{url="https://example.com"} 1
website_response_time_ms{url="https://example.com"} 150.5
website_status_code{url="https://example.com"} 200
```

### Grafana Dashboard
- **Real-time status** - Current up/down state
- **Response time trends** - Performance over time
- **Uptime percentage** - SLA tracking
- **Alert history** - Incident tracking

Access: http://localhost:3000 (admin/admin123)

## Common Use Cases

### 1. Production Website Monitoring
```bash
# Monitor critical production sites
WEBSITES_TO_MONITOR="https://yourapp.com,https://api.yourapp.com,https://admin.yourapp.com"
python monitor.py
```

### 2. Development Environment Checks
```bash
# Check staging and dev environments
WEBSITES_TO_MONITOR="https://staging.yourapp.com,https://dev.yourapp.com"
python monitor.py
```

### 3. Third-party Service Monitoring
```bash
# Monitor external dependencies
WEBSITES_TO_MONITOR="https://api.stripe.com,https://api.github.com,https://httpbin.org"
python monitor.py
```

### 4. Load Balancer Health Checks
```bash
# Monitor multiple instances
WEBSITES_TO_MONITOR="https://lb1.yourapp.com,https://lb2.yourapp.com"
python monitor.py
```

## Troubleshooting

### Common Issues

**1. Email alerts not working**
```bash
# Check credentials
echo $EMAIL_USER
echo $EMAIL_PASSWORD

# Test SMTP connection
python -c "import smtplib; smtplib.SMTP('smtp.gmail.com', 587)"
```

**2. Slack alerts not working**
```bash
# Verify webhook URL
curl -X POST -H 'Content-type: application/json' \
  --data '{"text":"Test message"}' \
  $SLACK_WEBHOOK_URL
```

**3. Docker build fails**
```bash
# Check Docker daemon
docker version

# Build with verbose output
docker build -t uptime-monitor . --no-cache
```

**4. Prometheus metrics not showing**
```bash
# Check if exporter is running
curl http://localhost:8000/health

# Verify results file exists
ls -la uptime_results.json
```

### Log Analysis
```bash
# View recent logs
tail -f uptime_monitor.log

# Search for errors
grep ERROR uptime_monitor.log

# Check specific website
grep "example.com" uptime_monitor.log
```

## Performance Tips

### 1. Optimize Check Frequency
- **Production**: Every 5-10 minutes
- **Development**: Every 30 minutes
- **Testing**: Every 1 minute

### 2. Timeout Settings
- **Fast sites**: 5-10 seconds
- **Slow sites**: 15-30 seconds
- **International**: 30+ seconds

### 3. Concurrent Monitoring
```python
# For many sites, consider threading
import concurrent.futures

def check_sites_concurrently(websites):
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(check_website, site) for site in websites]
        return [future.result() for future in futures]
```

## Security Best Practices

### 1. Credentials Management
- Use **app passwords** for Gmail
- Store secrets in **environment variables**
- Never commit credentials to git

### 2. Network Security
- Use **HTTPS** for all monitored sites
- Validate **SSL certificates**
- Monitor from **trusted networks**

### 3. Container Security
- Run as **non-root user**
- Use **minimal base images**
- Keep dependencies **updated**

## Scaling Considerations

### Horizontal Scaling
```bash
# Multiple monitor instances
docker-compose up --scale uptime-monitor=3
```

### Vertical Scaling
```bash
# More resources per container
docker run -m 512m --cpus="1.0" uptime-monitor
```

### Distributed Monitoring
- Deploy in **multiple regions**
- Use **load balancers**
- Aggregate metrics centrally

## Integration Examples

### 1. PagerDuty Integration
```python
# Add to monitor.py
def send_pagerduty_alert(down_sites):
    payload = {
        "routing_key": os.getenv('PAGERDUTY_KEY'),
        "event_action": "trigger",
        "payload": {
            "summary": f"{len(down_sites)} websites down",
            "severity": "critical"
        }
    }
    requests.post('https://events.pagerduty.com/v2/enqueue', json=payload)
```

### 2. Discord Webhook
```python
def send_discord_alert(down_sites):
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    message = {
        "content": f"🚨 {len(down_sites)} websites are down!",
        "embeds": [
            {
                "title": site['url'],
                "description": site['error'],
                "color": 15158332  # Red color
            }
            for site in down_sites
        ]
    }
    requests.post(webhook_url, json=message)
```

### 3. Database Storage
```python
import sqlite3

def save_to_database(results):
    conn = sqlite3.connect('monitoring.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS checks (
            id INTEGER PRIMARY KEY,
            url TEXT,
            status TEXT,
            response_time REAL,
            timestamp TEXT
        )
    ''')
    
    for result in results:
        cursor.execute('''
            INSERT INTO checks (url, status, response_time, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (result['url'], result['status'], 
              result['response_time_ms'], result['timestamp']))
    
    conn.commit()
    conn.close()
```

## Support & Resources

- **Documentation**: README.md
- **Examples**: test_system.py
- **Configuration**: .env.example
- **Docker**: docker-compose.yml
- **CI/CD**: .github/workflows/

---

**Happy Monitoring! 🚀**