#!/usr/bin/env python3
"""
Distributed Hash Database for Threat Intelligence
Implements CIA (Confidentiality, Integrity, Availability) principles
"""

import json
import hashlib
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import requests
import threading
import os

class ThreatIntelligenceDB:
    """
    Distributed Hash Database implementing CIA principles:
    - Confidentiality: Role-based access control
    - Integrity: Hash-based tamper detection
    - Availability: Distributed across multiple nodes
    """
    
    def __init__(self, node_id: str, port: int, authorized_keys: List[str]):
        self.node_id = node_id
        self.port = port
        self.authorized_keys = authorized_keys
        self.db_file = f"threat_db_{node_id}.json"
        self.other_nodes = []
        self.records = {}
        self.load_database()
        
    def load_database(self):
        """Load existing database from file"""
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r') as f:
                    data = json.load(f)
                    self.records = data.get('records', {})
                    self.other_nodes = data.get('other_nodes', [])
                print(f"[{self.node_id}] Loaded {len(self.records)} records from database")
            except Exception as e:
                print(f"[{self.node_id}] Error loading database: {e}")
                self.records = {}
        else:
            print(f"[{self.node_id}] Creating new database")
            
    def save_database(self):
        """Save database to file"""
        try:
            data = {
                'node_id': self.node_id,
                'timestamp': datetime.now().isoformat(),
                'records': self.records,
                'other_nodes': self.other_nodes
            }
            with open(self.db_file, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"[{self.node_id}] Database saved with {len(self.records)} records")
        except Exception as e:
            print(f"[{self.node_id}] Error saving database: {e}")
    
    def generate_hash(self, url: str, classification: str, confidence: float, timestamp: str) -> str:
        """Generate SHA-256 hash for integrity verification"""
        data_string = f"{url}{classification}{confidence}{timestamp}{self.node_id}"
        return hashlib.sha256(data_string.encode()).hexdigest()
    
    def verify_integrity(self, record: Dict) -> bool:
        """Verify record integrity using hash"""
        try:
            expected_hash = self.generate_hash(
                record['url'],
                record['classification'],
                record['confidence'],
                record['timestamp']
            )
            return record.get('hash') == expected_hash
        except:
            return False
    
    def add_threat_record(self, url: str, classification: str, confidence: float, 
                         api_key: str, source: str = "manual") -> Dict:
        """
        Add new threat record (CONFIDENTIALITY: Only authorized users)
        """
        # CONFIDENTIALITY: Check authorization
        if api_key not in self.authorized_keys:
            return {
                'success': False,
                'error': 'Unauthorized access. Only security analysts can add threats.',
                'node_id': self.node_id
            }
        
        timestamp = datetime.now().isoformat()
        hash_value = self.generate_hash(url, classification, confidence, timestamp)
        
        record = {
            'url': url,
            'classification': classification,
            'confidence': confidence,
            'timestamp': timestamp,
            'hash': hash_value,
            'authorized_by': api_key,
            'source': source,
            'node_id': self.node_id,
            'replicas': [self.node_id]
        }
        
        # INTEGRITY: Store with hash
        self.records[url] = record
        
        # AVAILABILITY: Replicate to other nodes
        self.replicate_to_other_nodes(record)
        
        self.save_database()
        
        return {
            'success': True,
            'message': f'Threat record added successfully',
            'hash': hash_value,
            'node_id': self.node_id
        }
    
    def get_threat_info(self, url: str) -> Optional[Dict]:
        """
        Get threat information (AVAILABILITY: Distributed lookup)
        """
        # Check local database first
        if url in self.records:
            record = self.records[url]
            
            # INTEGRITY: Verify record hasn't been tampered with
            if self.verify_integrity(record):
                return {
                    'found': True,
                    'classification': record['classification'],
                    'confidence': record['confidence'],
                    'timestamp': record['timestamp'],
                    'source': 'local_cache',
                    'node_id': self.node_id,
                    'integrity_verified': True
                }
            else:
                print(f"[{self.node_id}] WARNING: Record integrity check failed for {url}")
                return {
                    'found': True,
                    'classification': record['classification'],
                    'confidence': record['confidence'],
                    'timestamp': record['timestamp'],
                    'source': 'local_cache_corrupted',
                    'node_id': self.node_id,
                    'integrity_verified': False
                }
        
        # AVAILABILITY: Check other nodes if not found locally
        return self.query_other_nodes(url)
    
    def query_other_nodes(self, url: str) -> Optional[Dict]:
        """Query other nodes for threat information"""
        for node in self.other_nodes:
            try:
                response = requests.get(
                    f"http://localhost:{node['port']}/get_threat/{url}",
                    timeout=2
                )
                if response.status_code == 200:
                    data = response.json()
                    if data.get('found'):
                        # Replicate to local database for future use
                        self.records[url] = data
                        self.save_database()
                        return data
            except:
                continue
        
        return {
            'found': False,
            'message': 'Threat not found in distributed database',
            'node_id': self.node_id
        }
    
    def replicate_to_other_nodes(self, record: Dict):
        """Replicate record to other nodes (AVAILABILITY)"""
        for node in self.other_nodes:
            try:
                requests.post(
                    f"http://localhost:{node['port']}/replicate_record",
                    json=record,
                    timeout=2
                )
                print(f"[{self.node_id}] Replicated to node {node['node_id']}")
            except Exception as e:
                print(f"[{self.node_id}] Failed to replicate to {node['node_id']}: {e}")
    
    def add_node(self, node_id: str, port: int):
        """Add another node to the network"""
        new_node = {'node_id': node_id, 'port': port}
        if new_node not in self.other_nodes:
            self.other_nodes.append(new_node)
            self.save_database()
            print(f"[{self.node_id}] Added node {node_id} on port {port}")
    
    def get_database_stats(self) -> Dict:
        """Get database statistics"""
        total_records = len(self.records)
        verified_records = sum(1 for record in self.records.values() 
                              if self.verify_integrity(record))
        
        return {
            'node_id': self.node_id,
            'total_records': total_records,
            'verified_records': verified_records,
            'corrupted_records': total_records - verified_records,
            'other_nodes': len(self.other_nodes),
            'integrity_percentage': (verified_records / total_records * 100) if total_records > 0 else 100
        }
    
    def demonstrate_cia_principles(self) -> Dict:
        """Demonstrate CIA principles for demo"""
        return {
            'confidentiality': {
                'description': 'Only authorized security analysts can add threats',
                'implementation': 'API key authentication required',
                'demo': 'Try adding threat without valid key -> Access denied'
            },
            'integrity': {
                'description': 'Hash-based tamper detection prevents data corruption',
                'implementation': 'SHA-256 hash verification for each record',
                'demo': 'Modify record -> Hash mismatch detected'
            },
            'availability': {
                'description': 'Distributed across multiple nodes for high availability',
                'implementation': 'Automatic replication and failover',
                'demo': 'Stop one node -> System continues working'
            }
        }

# Global database instance
threat_db = None

def initialize_database(node_id: str, port: int, authorized_keys: List[str]):
    """Initialize the distributed database"""
    global threat_db
    threat_db = ThreatIntelligenceDB(node_id, port, authorized_keys)
    return threat_db

def get_database() -> ThreatIntelligenceDB:
    """Get the global database instance"""
    return threat_db
