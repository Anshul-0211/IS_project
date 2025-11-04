#!/usr/bin/env python3
"""
Email Phishing Detection Test Script
Tests the email phishing detection model with sample emails
"""

import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
import joblib
import numpy as np

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

def print_result(is_phishing, probability):
    """Print detection result with color"""
    if is_phishing:
        print(f"{RED}⚠️  PHISHING DETECTED!{RESET}")
        print(f"{RED}   Confidence: {probability*100:.1f}%{RESET}")
    else:
        print(f"{GREEN}✓ LEGITIMATE EMAIL{RESET}")
        print(f"{GREEN}   Confidence: {(1-probability)*100:.1f}%{RESET}")

def detect_phishing(text, model, tokenizer, max_len=200):
    """Detect if email content is phishing"""
    # Preprocess input text
    sequence = tokenizer.texts_to_sequences([text])
    padded_sequence = pad_sequences(sequence, maxlen=max_len, padding='post')
    
    # Get model prediction
    prob = model.predict(padded_sequence, verbose=0)[0][0]
    is_phishing = prob >= 0.5
    
    return is_phishing, prob

def test_sample_emails():
    """Test the model with sample emails"""
    print_header("📧 EMAIL PHISHING DETECTION TEST")
    
    # Load model and tokenizer
    print(f"{YELLOW}Loading model and tokenizer...{RESET}")
    try:
        model = tf.keras.models.load_model('phishing_detection_model.h5')
        tokenizer = joblib.load('tokenizer.pkl')
        print(f"{GREEN}✓ Model and tokenizer loaded successfully{RESET}\n")
    except Exception as e:
        print(f"{RED}✗ Error loading model: {e}{RESET}")
        return
    
    # Test cases
    test_cases = [
        {
            "label": "Legitimate Email 1: Meeting Reminder",
            "subject": "Team Meeting Tomorrow",
            "content": "Hi team, just a reminder about our weekly meeting tomorrow at 3 PM in conference room B. Please bring your project updates.",
            "expected": False
        },
        {
            "label": "Legitimate Email 2: Project Update",
            "subject": "Project Status Update",
            "content": "Hello everyone, the project is progressing well. We've completed the design phase and are moving to implementation. Next review is scheduled for Friday.",
            "expected": False
        },
        {
            "label": "Phishing Email 1: Urgent Account Alert",
            "subject": "URGENT: Your account has been compromised!",
            "content": "Your account has been compromised! Click here immediately to verify your identity and secure your account. Failure to do so within 24 hours will result in permanent account suspension.",
            "expected": True
        },
        {
            "label": "Phishing Email 2: Prize Winner",
            "subject": "Congratulations! You've won $1,000,000!",
            "content": "You have been selected as the winner of our lottery! Click this link to claim your prize. Enter your bank details to receive the money immediately. Act now, this offer expires soon!",
            "expected": True
        },
        {
            "label": "Phishing Email 3: Bank Alert",
            "subject": "Your bank account needs verification",
            "content": "Dear customer, we have detected suspicious activity on your account. Please click the link below to verify your account information and prevent it from being locked.",
            "expected": True
        },
        {
            "label": "Legitimate Email 3: Newsletter",
            "subject": "Monthly Newsletter - December 2024",
            "content": "Welcome to our monthly newsletter! This month we're featuring tips on cybersecurity, new product launches, and upcoming events. Thank you for being a valued subscriber.",
            "expected": False
        }
    ]
    
    # Test each email
    results = []
    for i, test in enumerate(test_cases, 1):
        print_header(f"Test {i}: {test['label']}")
        
        print(f"{YELLOW}Subject:{RESET} {test['subject']}")
        print(f"{YELLOW}Content:{RESET} {test['content'][:100]}...")
        
        # Combine subject and content
        email_text = f"{test['subject']} {test['content']}"
        
        # Detect phishing
        is_phishing, prob = detect_phishing(email_text, model, tokenizer)
        
        print()
        print_result(is_phishing, prob)
        
        # Check if result matches expected
        correct = (is_phishing == test['expected'])
        results.append(correct)
        
        if correct:
            print(f"{GREEN}✓ Correct detection{RESET}")
        else:
            print(f"{RED}✗ Incorrect detection (expected: {'Phishing' if test['expected'] else 'Legitimate'}){RESET}")
    
    # Summary
    print_header("Test Summary")
    total = len(results)
    passed = sum(results)
    accuracy = (passed / total) * 100
    
    print(f"Total Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Accuracy: {accuracy:.1f}%\n")
    
    if passed == total:
        print(f"{GREEN}🎉 All tests passed!{RESET}")
    else:
        print(f"{YELLOW}⚠️  {total - passed} test(s) failed{RESET}")

def interactive_test():
    """Interactive testing mode"""
    print_header("📧 INTERACTIVE EMAIL PHISHING TEST")
    
    # Load model and tokenizer
    print(f"{YELLOW}Loading model and tokenizer...{RESET}")
    try:
        model = tf.keras.models.load_model('phishing_detection_model.h5')
        tokenizer = joblib.load('tokenizer.pkl')
        print(f"{GREEN}✓ Model and tokenizer loaded successfully{RESET}\n")
    except Exception as e:
        print(f"{RED}✗ Error loading model: {e}{RESET}")
        return
    
    print("Enter email details to test (or 'quit' to exit)\n")
    
    while True:
        try:
            print(f"\n{BLUE}{'─'*60}{RESET}")
            subject = input(f"{YELLOW}Subject:{RESET} ").strip()
            
            if subject.lower() in ['quit', 'exit', 'q']:
                print(f"{YELLOW}Exiting...{RESET}")
                break
            
            content = input(f"{YELLOW}Content:{RESET} ").strip()
            
            if not subject and not content:
                continue
            
            # Combine and test
            email_text = f"{subject} {content}"
            is_phishing, prob = detect_phishing(email_text, model, tokenizer)
            
            print()
            print_result(is_phishing, prob)
            
        except KeyboardInterrupt:
            print(f"\n{YELLOW}Exiting...{RESET}")
            break
        except Exception as e:
            print(f"{RED}Error: {e}{RESET}")

def main():
    """Main function"""
    import sys
    
    print(f"{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}Email Phishing Detection Test System{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")
    
    if len(sys.argv) > 1 and sys.argv[1] == '--interactive':
        interactive_test()
    else:
        test_sample_emails()
        print(f"\n{YELLOW}Tip: Run with --interactive flag for interactive testing{RESET}")
        print(f"{YELLOW}     python test_email_phishing.py --interactive{RESET}\n")

if __name__ == "__main__":
    main()


