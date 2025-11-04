#!/usr/bin/env python3
"""
Start Node 2 of the Distributed Threat Intelligence Database
Port: 5002
"""

import os
import sys

# Set environment variables for this node
os.environ['NODE_ID'] = 'node_2'
os.environ['PORT'] = '5002'

# Add the distributed-db directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'distributed-db'))

# Import and run the API server
from api_server import app

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 STARTING DISTRIBUTED THREAT INTELLIGENCE NODE 2")
    print("=" * 60)
    print("Node ID: node_2")
    print("Port: 5002")
    print("Role: Secondary Security Node")
    print("CIA Features: Confidentiality, Integrity, Availability")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5002, debug=False)
