#!/usr/bin/env python3
"""
Start Node 3 of the Distributed Threat Intelligence Database
Port: 5003
"""

import os
import sys

# Set environment variables for this node
os.environ['NODE_ID'] = 'node_3'
os.environ['PORT'] = '5003'

# Add the distributed-db directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'distributed-db'))

# Import and run the API server
from api_server import app

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 STARTING DISTRIBUTED THREAT INTELLIGENCE NODE 3")
    print("=" * 60)
    print("Node ID: node_3")
    print("Port: 5003")
    print("Role: Tertiary Security Node")
    print("CIA Features: Confidentiality, Integrity, Availability")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5003, debug=False)
