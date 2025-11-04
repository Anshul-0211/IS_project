"""
Test script for crypto_utils module
Run from server directory: python test_crypto.py
"""

import sys
import os

# Add server directory to path
sys.path.insert(0, os.path.dirname(__file__))

from crypto_utils import test_encryption, test_signatures

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🔐 CRYPTOGRAPHY MODULE - PHISHING DETECTION SYSTEM")
    print("="*60)
    
    # Run tests
    test_encryption()
    test_signatures()
    
    print("\n" + "="*60)
    print("✅ ALL TESTS COMPLETE")
    print("="*60 + "\n")
