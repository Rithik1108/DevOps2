#!/usr/bin/env python3
"""
Simple test script to demonstrate the uptime monitoring system
Tests both successful and failed website checks
"""

import os
import time
from monitor import UptimeMonitor

def test_monitoring_system():
    """Test the monitoring system with various scenarios"""
    
    print("🧪 Testing Website Uptime Monitor System")
    print("=" * 50)
    
    # Test websites - mix of working and non-working
    test_websites = [
        'https://httpbin.org/status/200',  # Should work
        'https://httpbin.org/status/404',  # Should return 404
        'https://httpbin.org/status/500',  # Should return 500
        'https://httpbin.org/delay/2',     # Should work but be slow
        'https://nonexistent-website-12345.com',  # Should fail
    ]
    
    print(f"Testing {len(test_websites)} websites:")
    for i, site in enumerate(test_websites, 1):
        print(f"  {i}. {site}")
    
    print("\n" + "=" * 50)
    print("Starting monitoring test...")
    print("=" * 50)
    
    # Create monitor instance
    monitor = UptimeMonitor(test_websites, timeout=10)
    
    # Run the monitoring
    results = monitor.check_all_websites()
    
    # Save results
    monitor.save_results_to_json('test_results.json')
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print("=" * 50)
    
    up_count = 0
    down_count = 0
    
    for result in results:
        status_emoji = "✅" if result['status'] == 'UP' else "❌"
        print(f"{status_emoji} {result['url']}")
        print(f"   Status: {result['status']}")
        print(f"   Response Time: {result['response_time_ms']}ms")
        print(f"   Status Code: {result['status_code']}")
        if result['error']:
            print(f"   Error: {result['error']}")
        print()
        
        if result['status'] == 'UP':
            up_count += 1
        else:
            down_count += 1
    
    print("=" * 50)
    print(f"📈 Final Summary: {up_count} UP, {down_count} DOWN")
    print("=" * 50)
    
    # Test alert functionality (without actually sending)
    down_sites = [r for r in results if r['status'] == 'DOWN']
    if down_sites:
        print(f"🚨 Found {len(down_sites)} down sites - Alert system would trigger")
        print("   (Email and Slack alerts disabled for testing)")
    else:
        print("🎉 All sites are up - No alerts needed")
    
    print("\n✅ Test completed successfully!")
    print(f"📄 Results saved to: test_results.json")
    
    return results

if __name__ == "__main__":
    test_monitoring_system()