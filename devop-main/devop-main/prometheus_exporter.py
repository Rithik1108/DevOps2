#!/usr/bin/env python3
"""
Prometheus Metrics Exporter for Website Uptime Monitor
Exposes metrics on /metrics endpoint for Prometheus scraping
"""

from flask import Flask, Response
import json
import os
from datetime import datetime
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_latest_results():
    """Load the latest monitoring results from JSON file"""
    try:
        if os.path.exists('uptime_results.json'):
            with open('uptime_results.json', 'r') as f:
                results = json.load(f)
            return results
        return []
    except Exception as e:
        logger.error(f"Error loading results: {e}")
        return []

def generate_prometheus_metrics():
    """Generate Prometheus metrics format"""
    results = load_latest_results()
    
    if not results:
        return "# No data available\n"
    
    # Get the latest results for each website
    latest_results = {}
    for result in results:
        url = result['url']
        if url not in latest_results or result['timestamp'] > latest_results[url]['timestamp']:
            latest_results[url] = result
    
    metrics = []
    
    # Add metric descriptions
    metrics.append("# HELP website_up Whether the website is up (1) or down (0)")
    metrics.append("# TYPE website_up gauge")
    
    metrics.append("# HELP website_response_time_ms Response time in milliseconds")
    metrics.append("# TYPE website_response_time_ms gauge")
    
    metrics.append("# HELP website_status_code HTTP status code returned")
    metrics.append("# TYPE website_status_code gauge")
    
    # Generate metrics for each website
    for url, result in latest_results.items():
        # Clean URL for label (remove protocol and special characters)
        clean_url = url.replace('https://', '').replace('http://', '').replace('/', '_').replace('.', '_').replace('-', '_')
        
        # Website up/down metric
        up_value = 1 if result['status'] == 'UP' else 0
        metrics.append(f'website_up{{url="{url}",instance="{clean_url}"}} {up_value}')
        
        # Response time metric
        response_time = result.get('response_time_ms', 0)
        metrics.append(f'website_response_time_ms{{url="{url}",instance="{clean_url}"}} {response_time}')
        
        # Status code metric
        status_code = result.get('status_code', 0) or 0
        metrics.append(f'website_status_code{{url="{url}",instance="{clean_url}"}} {status_code}')
    
    # Add timestamp of last update
    if latest_results:
        latest_timestamp = max(result['timestamp'] for result in latest_results.values())
        # Convert ISO timestamp to Unix timestamp
        dt = datetime.fromisoformat(latest_timestamp.replace('Z', '+00:00'))
        unix_timestamp = int(dt.timestamp())
        metrics.append(f"# HELP website_monitor_last_update_timestamp Unix timestamp of last monitoring update")
        metrics.append(f"# TYPE website_monitor_last_update_timestamp gauge")
        metrics.append(f"website_monitor_last_update_timestamp {unix_timestamp}")
    
    return '\n'.join(metrics) + '\n'

@app.route('/metrics')
def metrics():
    """Prometheus metrics endpoint"""
    try:
        prometheus_metrics = generate_prometheus_metrics()
        return Response(prometheus_metrics, mimetype='text/plain')
    except Exception as e:
        logger.error(f"Error generating metrics: {e}")
        return Response("# Error generating metrics\n", mimetype='text/plain', status=500)

@app.route('/health')
def health():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.route('/')
def index():
    """Root endpoint with basic info"""
    return {
        "service": "Website Uptime Monitor - Prometheus Exporter",
        "endpoints": {
            "/metrics": "Prometheus metrics",
            "/health": "Health check",
            "/": "This page"
        },
        "timestamp": datetime.now().isoformat()
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    host = os.getenv('HOST', '0.0.0.0')
    
    logger.info(f"Starting Prometheus exporter on {host}:{port}")
    logger.info(f"Metrics available at http://{host}:{port}/metrics")
    
    app.run(host=host, port=port, debug=False)