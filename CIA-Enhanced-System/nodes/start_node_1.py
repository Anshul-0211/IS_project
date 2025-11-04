#!/usr/bin/env python3
"""
Start Node 1 of the Distributed Threat Intelligence Database
Port: 5001
"""

import os
import sys

# Set environment variables for this node
os.environ['NODE_ID'] = 'node_1'
os.environ['PORT'] = '5001'

# Add the distributed-db directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'distributed-db'))

# Import and run the API server
from api_server import app

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 STARTING DISTRIBUTED THREAT INTELLIGENCE NODE 1")
    print("=" * 60)
    print("Node ID: node_1")
    print("Port: 5001")
    print("Role: Primary Security Node")
    print("CIA Features: Confidentiality, Integrity, Availability")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5001, debug=False)
