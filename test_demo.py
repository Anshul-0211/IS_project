#!/usr/bin/env python3
"""
Demo Testing Script for Progress Report
Tests the phishing detection system components
"""

import requests
import json
import time
from datetime import datetime

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_header(text):
    """Print formatted header"""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}{text.center(60)}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")

def print_success(text):
    """Print success message"""
    print(f"{GREEN}✓ {text}{RESET}")

def print_error(text):
    """Print error message"""
    print(f"{RED}✗ {text}{RESET}")

def print_info(text):
    """Print info message"""
    print(f"{YELLOW}ℹ {text}{RESET}")

def test_server_connection():
    """Test if Flask server is running"""
    print_header("Testing Server Connection")
    try:
        response = requests.get("http://localhost:5000/", timeout=2)
        print_success("Flask server is running on http://localhost:5000")
        return True
    except requests.exceptions.ConnectionError:
        print_error("Flask server is NOT running!")
        print_info("Start server with: cd server && python app.py")
        return False
    except Exception as e:
        print_error(f"Error connecting to server: {e}")
        return False

def test_phishing_detection(url, expected_result):
    """Test phishing detection with a specific URL"""
    print(f"\n{YELLOW}Testing URL:{RESET} {url}")
    
    try:
        response = requests.post(
            "http://localhost:5000/classify_url",
            headers={"Content-Type": "application/json"},
            json={"url": url},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            is_phishing = data.get('is_phishing', False)
            confidence = data.get('probability', 0)
            source = data.get('source', 'Unknown')
            
            if is_phishing:
                print_error(f"⚠️  PHISHING DETECTED!")
            else:
                print_success(f"✓ SAFE WEBSITE")
            
            print(f"   Source: {source}")
            print(f"   Confidence: {confidence:.2%}" if isinstance(confidence, float) else f"   Confidence: {confidence}")
            
            return is_phishing == expected_result
            
        elif response.status_code == 403:
            print_error(f"⚠️  BLOCKED - High confidence phishing site!")
            return expected_result == True
        else:
            print_error(f"Unexpected status code: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Error testing URL: {e}")
        return False

def run_demo_tests():
    """Run comprehensive demo tests"""
    print_header("🛡️ PHISHING DETECTION SYSTEM - DEMO TESTS")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Test server connection
    if not test_server_connection():
        return
    
    time.sleep(1)
    
    # Test cases
    print_header("Testing Legitimate Websites")
    
    test_cases_safe = [
        ("https://google.com", False),
        ("https://github.com", False),
        ("https://microsoft.com", False),
    ]
    
    safe_results = []
    for url, expected in test_cases_safe:
        result = test_phishing_detection(url, expected)
        safe_results.append(result)
        time.sleep(0.5)
    
    print_header("Testing Suspicious URLs")
    
    test_cases_phishing = [
        ("http://fake-paypal-login.com", True),
        ("http://microsoft-security-alert.net", True),
        ("http://bank-account-verify.org", True),
    ]
    
    phishing_results = []
    for url, expected in test_cases_phishing:
        result = test_phishing_detection(url, expected)
        phishing_results.append(result)
        time.sleep(0.5)
    
    # Summary
    print_header("Test Summary")
    
    total_tests = len(safe_results) + len(phishing_results)
    passed_tests = sum(safe_results) + sum(phishing_results)
    
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%\n")
    
    if passed_tests == total_tests:
        print_success("🎉 All tests passed! System is working correctly.")
    else:
        print_info(f"⚠️  {total_tests - passed_tests} test(s) failed. Review configuration.")
    
    print_header("Demo Complete")

def interactive_test():
    """Interactive testing mode"""
    print_header("🛡️ INTERACTIVE PHISHING DETECTION TEST")
    
    # Test server first
    if not test_server_connection():
        return
    
    print("\nEnter URLs to test (or 'quit' to exit)")
    print("Examples:")
    print("  - https://google.com")
    print("  - http://fake-paypal-login.com")
    print("  - http://suspicious-bank-verify.org\n")
    
    while True:
        try:
            url = input(f"\n{YELLOW}Enter URL:{RESET} ").strip()
            
            if url.lower() in ['quit', 'exit', 'q']:
                print_info("Exiting interactive mode...")
                break
            
            if not url:
                continue
            
            # Add http:// if no protocol specified
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
            
            test_phishing_detection(url, None)
            
        except KeyboardInterrupt:
            print_info("\n\nExiting interactive mode...")
            break
        except Exception as e:
            print_error(f"Error: {e}")

def main():
    """Main function"""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--interactive':
        interactive_test()
    else:
        run_demo_tests()

if __name__ == "__main__":
    main()


