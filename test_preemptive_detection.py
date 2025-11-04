#!/usr/bin/env python3
"""
Test script for preemptive URL detection
This script tests various URLs to demonstrate the preemptive detection system
"""

import requests
import json
import time

# Test URLs for demonstration
TEST_URLS = {
    "Safe URLs": [
        "https://google.com",
        "https://github.com", 
        "https://microsoft.com",
        "https://stackoverflow.com"
    ],
    "Suspicious URLs": [
        "http://phishing-test.com",
        "http://malware-testing.com",
        "http://suspicious-site.net",
        "http://fake-bank-login.org",
        "http://paypal-security-alert.com",
        "http://microsoft-account-verify.net"
    ]
}

def test_url_classification(url):
    """Test a single URL with the server"""
    try:
        response = requests.post(
            'http://localhost:5000/classify_url',
            headers={'Content-Type': 'application/json'},
            json={'url': url},
            timeout=10
        )
        
        if response.status_code == 403:
            return {
                'url': url,
                'status': 'PHISHING DETECTED',
                'source': 'Server blocked (403)',
                'safe': False
            }
        elif response.status_code == 200:
            data = response.json()
            return {
                'url': url,
                'status': 'SAFE' if not data.get('is_phishing', False) else 'PHISHING DETECTED',
                'probability': data.get('probability', 'N/A'),
                'source': data.get('source', 'Unknown'),
                'safe': not data.get('is_phishing', False)
            }
        else:
            return {
                'url': url,
                'status': 'ERROR',
                'error': f'HTTP {response.status_code}',
                'safe': True
            }
    except requests.exceptions.RequestException as e:
        return {
            'url': url,
            'status': 'ERROR',
            'error': str(e),
            'safe': True
        }

def run_preemptive_tests():
    """Run comprehensive preemptive detection tests"""
    print("PREEMPTIVE URL DETECTION TEST")
    print("=" * 50)
    print()
    
    # Test safe URLs
    print("Testing SAFE URLs:")
    print("-" * 30)
    safe_results = []
    for url in TEST_URLS["Safe URLs"]:
        result = test_url_classification(url)
        safe_results.append(result)
        
        status_icon = "[SAFE]" if result['safe'] else "[WARNING]"
        print(f"{status_icon} {url}")
        print(f"   Status: {result['status']}")
        if 'probability' in result:
            print(f"   Probability: {result['probability']}")
        print()
    
    print("\n" + "=" * 50)
    print()
    
    # Test suspicious URLs
    print("Testing SUSPICIOUS URLs:")
    print("-" * 30)
    suspicious_results = []
    for url in TEST_URLS["Suspicious URLs"]:
        result = test_url_classification(url)
        suspicious_results.append(result)
        
        status_icon = "[SAFE]" if result['safe'] else "[WARNING]"
        print(f"{status_icon} {url}")
        print(f"   Status: {result['status']}")
        if 'probability' in result:
            print(f"   Probability: {result['probability']}")
        print()
    
    print("\n" + "=" * 50)
    print()
    
    # Summary
    total_tests = len(safe_results) + len(suspicious_results)
    safe_detected = sum(1 for r in safe_results if r['safe'])
    suspicious_detected = sum(1 for r in suspicious_results if not r['safe'])
    
    print("TEST SUMMARY:")
    print(f"   Total URLs tested: {total_tests}")
    print(f"   Safe URLs correctly identified: {safe_detected}/{len(safe_results)}")
    print(f"   Suspicious URLs detected: {suspicious_detected}/{len(suspicious_results)}")
    print(f"   Overall accuracy: {((safe_detected + suspicious_detected) / total_tests * 100):.1f}%")
    
    return {
        'safe_results': safe_results,
        'suspicious_results': suspicious_results,
        'summary': {
            'total': total_tests,
            'safe_correct': safe_detected,
            'suspicious_detected': suspicious_detected,
            'accuracy': (safe_detected + suspicious_detected) / total_tests * 100
        }
    }

def demo_preemptive_flow():
    """Demonstrate the preemptive detection flow"""
    print("\nPREEMPTIVE DETECTION DEMO")
    print("=" * 50)
    print()
    print("This demonstrates how the extension works:")
    print()
    print("1. User types URL in address bar")
    print("2. User presses Enter")
    print("3. Extension checks URL BEFORE page loads")
    print("4. If phishing detected -> Shows warning, blocks navigation")
    print("5. If safe -> Allows normal page loading")
    print()
    print("To test with browser extension:")
    print("   1. Start the Flask server: python server/app.py")
    print("   2. Load the extension in Chrome")
    print("   3. Type suspicious URLs in address bar")
    print("   4. Press Enter and watch the detection!")
    print()

if __name__ == "__main__":
    print("Starting Preemptive URL Detection Tests")
    print("Make sure the Flask server is running on localhost:5000")
    print()
    
    try:
        # Test server connectivity
        response = requests.get('http://localhost:5000', timeout=5)
        print("Server is running")
    except:
        print("Server not running! Please start: python server/app.py")
        exit(1)
    
    print()
    
    # Run the tests
    results = run_preemptive_tests()
    
    # Show demo flow
    demo_preemptive_flow()
    
    print("\nKey Benefits of Preemptive Detection:")
    print("   • Prevents malicious sites from loading")
    print("   • Protects users before exposure")
    print("   • Faster detection (URL-only analysis)")
    print("   • Better user experience")
    print("   • Works with non-existent domains")
