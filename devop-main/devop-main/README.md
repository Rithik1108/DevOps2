# 🚀 Website Uptime Monitor

A comprehensive DevOps monitoring solution that checks website uptime, measures response times, and provides real-time alerts through multiple channels. Built with Python, Docker, GitHub Actions, and integrated with Prometheus and Grafana for advanced monitoring and visualization.

## 📋 Features

- **Website Monitoring**: Check multiple websites for uptime and response time
- **Real-time Logging**: Detailed logging with timestamps and status information
- **Multi-channel Alerts**: Email and Slack notifications for down sites
- **Prometheus Integration**: Export metrics for advanced monitoring
- **Grafana Dashboard**: Beautiful visualizations and analytics
- **Docker Support**: Containerized deployment with Docker Compose
- **CI/CD Pipeline**: Automated monitoring with GitHub Actions
- **Flexible Configuration**: Environment-based configuration

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   GitHub        │    │   Docker        │    │   Monitoring    │
│   Actions       │───▶│   Container     │───▶│   Script        │
│   (Scheduler)   │    │   (Python)      │    │   (monitor.py)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                       │
                       ┌─────────────────┐            │
                       │   Prometheus    │◀───────────┘
                       │   Exporter      │
                       └─────────────────┘
                                │
                       ┌─────────────────┐
                       │   Grafana       │
                       │   Dashboard     │
                       └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Docker and Docker Compose
- Git

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd devops
```

### 2. Set Up Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your configuration
# Add your email credentials, Slack webhook, etc.
```

### 3. Run with Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f uptime-monitor
```

### 4. Access Services

- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/admin123)
- **Metrics Endpoint**: http://localhost:8000/metrics

## 📁 Project Structure

```
devops/
├── monitor.py                 # Main monitoring script
├── prometheus_exporter.py     # Prometheus metrics exporter
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Container configuration
├── docker-compose.yml         # Multi-service deployment
├── prometheus.yml             # Prometheus configuration
├── .github/
│   └── workflows/
│       └── uptime-monitor.yml # GitHub Actions workflow
├── grafana/
│   └── provisioning/          # Grafana configuration
├── logs/                      # Log files (created at runtime)
├── results/                   # JSON results (created at runtime)
└── README.md                  # This file
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `WEBSITES_TO_MONITOR` | Comma-separated list of URLs | See monitor.py |
| `SMTP_SERVER` | SMTP server for email alerts | smtp.gmail.com |
| `SMTP_PORT` | SMTP port | 587 |
| `EMAIL_USER` | Email username | - |
| `EMAIL_PASSWORD` | Email password/app password | - |
| `EMAIL_TO` | Alert recipient email | - |
| `SLACK_WEBHOOK_URL` | Slack webhook URL | - |
| `GRAFANA_PASSWORD` | Grafana admin password | admin |

### Websites Configuration

Edit the `websites` list in `monitor.py` or set the `WEBSITES_TO_MONITOR` environment variable:

```python
websites = [
    'https://google.com',
    'https://github.com',
    'https://stackoverflow.com',
    'https://python.org',
    # Add your websites here
]
```

## 🐳 Docker Usage

### Build and Run Single Container

```bash
# Build image
docker build -t uptime-monitor .

# Run container
docker run -d \
  --name uptime-monitor \
  -e WEBSITES_TO_MONITOR="https://google.com,https://github.com" \
  -v $(pwd)/logs:/app/logs \
  uptime-monitor
```

### Full Stack with Docker Compose

```bash
# Start all services
docker-compose up -d

# Scale monitoring instances
docker-compose up -d --scale uptime-monitor=3

# Stop services
docker-compose down
```

## 🔄 GitHub Actions

The project includes a GitHub Actions workflow that:

- Runs every 30 minutes automatically
- Can be triggered manually
- Uploads logs as artifacts
- Supports custom website lists
- Builds and tests Docker images

### Setup GitHub Secrets

Add these secrets to your GitHub repository:

- `SMTP_SERVER`
- `SMTP_PORT`
- `EMAIL_USER`
- `EMAIL_PASSWORD`
- `EMAIL_TO`
- `SLACK_WEBHOOK_URL`

### Manual Trigger

Go to Actions → Website Uptime Monitor → Run workflow

## 📊 Monitoring and Alerts

### Email Alerts

Configure SMTP settings in your environment:

```bash
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
EMAIL_TO=alerts@yourcompany.com
```

### Slack Alerts

Set up a Slack webhook and configure:

```bash
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK
```

### Prometheus Metrics

Available metrics:

- `website_up`: Website status (1=up, 0=down)
- `website_response_time_ms`: Response time in milliseconds
- `website_status_code`: HTTP status code
- `website_monitor_last_update_timestamp`: Last update timestamp

### Grafana Dashboard

The included dashboard provides:

- Real-time website status table
- Response time trends
- Overall uptime percentage
- Status distribution charts

## 🛠️ Development

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run monitoring script
python monitor.py

# Run Prometheus exporter
python prometheus_exporter.py
```

### Testing

```bash
# Test with custom websites
WEBSITES_TO_MONITOR="https://httpbin.org/status/200,https://httpbin.org/status/500" python monitor.py

# Test Prometheus exporter
curl http://localhost:8000/metrics
```

## 📈 Metrics and Analytics

### Key Performance Indicators

- **Uptime Percentage**: Overall availability of monitored sites
- **Response Time**: Average and peak response times
- **Error Rate**: Percentage of failed checks
- **Alert Frequency**: Number of alerts sent

### Grafana Queries

```promql
# Average uptime percentage
avg(website_up) * 100

# Response time by website
website_response_time_ms

# Down sites count
count(website_up == 0)
```

## 🔒 Security Considerations

- Use app passwords for email authentication
- Store sensitive data in environment variables
- Run containers as non-root user
- Regularly update dependencies
- Use HTTPS for webhook URLs

## 🚨 Troubleshooting

### Common Issues

1. **Email alerts not working**
   - Check SMTP credentials
   - Use app passwords for Gmail
   - Verify firewall settings

2. **Slack alerts not working**
   - Verify webhook URL
   - Check Slack app permissions

3. **Docker build fails**
   - Check Docker daemon status
   - Verify requirements.txt syntax

4. **Grafana dashboard not loading**
   - Check Prometheus data source
   - Verify metrics endpoint

### Logs

```bash
# View container logs
docker-compose logs uptime-monitor

# View specific service logs
docker logs uptime-monitor

# Follow logs in real-time
docker-compose logs -f
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with Python and Flask
- Monitoring powered by Prometheus
- Visualizations by Grafana
- CI/CD with GitHub Actions
- Containerized with Docker

---

## 📝 Resume Bullet Point

**DevOps Monitoring System**: Developed and deployed a comprehensive website uptime monitoring solution using Python, Docker, and GitHub Actions. Implemented automated CI/CD pipeline with 30-minute intervals, integrated Prometheus metrics collection and Grafana dashboards for real-time visualization, and configured multi-channel alerting (Email/Slack) for 99.9% uptime SLA monitoring across 20+ production websites.

---

*For questions or support, please open an issue in the GitHub repository.*