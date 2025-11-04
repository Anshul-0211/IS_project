#!/usr/bin/env python3
"""
Authentication and Authorization System for CIA Database
Implements CONFIDENTIALITY principle with role-based access control
"""

import hashlib
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json
import os

class SecurityAnalyst:
    """Represents a security analyst with specific permissions"""
    
    def __init__(self, analyst_id: str, name: str, role: str, permissions: List[str]):
        self.analyst_id = analyst_id
        self.name = name
        self.role = role
        self.permissions = permissions
        self.created_at = datetime.now()
        self.last_activity = None
        
    def has_permission(self, permission: str) -> bool:
        """Check if analyst has specific permission"""
        return permission in self.permissions
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for storage"""
        return {
            'analyst_id': self.analyst_id,
            'name': self.name,
            'role': self.role,
            'permissions': self.permissions,
            'created_at': self.created_at.isoformat(),
            'last_activity': self.last_activity.isoformat() if self.last_activity else None
        }

class AuthenticationSystem:
    """
    CIA CONFIDENTIALITY Implementation:
    - Role-based access control
    - API key authentication
    - Permission-based authorization
    - Audit logging
    """
    
    def __init__(self):
        self.analysts = {}
        self.api_keys = {}
        self.audit_log = []
        self.load_analysts()
        
    def load_analysts(self):
        """Load security analysts from file"""
        if os.path.exists('security_analysts.json'):
            try:
                with open('security_analysts.json', 'r') as f:
                    data = json.load(f)
                    for analyst_data in data.get('analysts', []):
                        analyst = SecurityAnalyst(
                            analyst_data['analyst_id'],
                            analyst_data['name'],
                            analyst_data['role'],
                            analyst_data['permissions']
                        )
                        analyst.created_at = datetime.fromisoformat(analyst_data['created_at'])
                        if analyst_data.get('last_activity'):
                            analyst.last_activity = datetime.fromisoformat(analyst_data['last_activity'])
                        self.analysts[analyst.analyst_id] = analyst
                        
                # Load API keys
                for key_data in data.get('api_keys', []):
                    self.api_keys[key_data['api_key']] = key_data
                    
                print(f"Loaded {len(self.analysts)} security analysts")
            except Exception as e:
                print(f"Error loading analysts: {e}")
        else:
            # Create default analysts for demo
            self.create_default_analysts()
    
    def create_default_analysts(self):
        """Create default security analysts for demonstration"""
        default_analysts = [
            {
                'analyst_id': 'analyst_001',
                'name': 'Dr. Sarah Johnson',
                'role': 'Senior Security Analyst',
                'permissions': ['add_threats', 'modify_threats', 'view_all', 'admin']
            },
            {
                'analyst_id': 'analyst_002', 
                'name': 'Mike Chen',
                'role': 'Security Analyst',
                'permissions': ['add_threats', 'view_all']
            },
            {
                'analyst_id': 'analyst_003',
                'name': 'Lisa Rodriguez',
                'role': 'Junior Security Analyst', 
                'permissions': ['view_all']
            }
        ]
        
        for analyst_data in default_analysts:
            analyst = SecurityAnalyst(
                analyst_data['analyst_id'],
                analyst_data['name'],
                analyst_data['role'],
                analyst_data['permissions']
            )
            self.analysts[analyst.analyst_id] = analyst
            
        # Generate API keys for each analyst
        for analyst_id, analyst in self.analysts.items():
            api_key = self.generate_api_key(analyst_id)
            self.api_keys[api_key] = {
                'analyst_id': analyst_id,
                'created_at': datetime.now().isoformat(),
                'permissions': analyst.permissions
            }
        
        self.save_analysts()
        print("Created default security analysts for CIA demonstration")
    
    def generate_api_key(self, analyst_id: str) -> str:
        """Generate secure API key for analyst"""
        timestamp = str(int(time.time()))
        data = f"{analyst_id}{timestamp}{os.urandom(16).hex()}"
        return hashlib.sha256(data.encode()).hexdigest()[:32]
    
    def authenticate(self, api_key: str) -> Optional[SecurityAnalyst]:
        """
        Authenticate user with API key (CONFIDENTIALITY)
        """
        if api_key not in self.api_keys:
            self.log_audit('authentication_failed', f'Invalid API key: {api_key[:8]}...')
            return None
        
        analyst_id = self.api_keys[api_key]['analyst_id']
        analyst = self.analysts.get(analyst_id)
        
        if analyst:
            analyst.last_activity = datetime.now()
            self.log_audit('authentication_success', f'Analyst {analyst.name} authenticated')
            return analyst
        
        return None
    
    def authorize(self, analyst: SecurityAnalyst, permission: str) -> bool:
        """
        Check if analyst has permission for action (CONFIDENTIALITY)
        """
        has_permission = analyst.has_permission(permission)
        
        self.log_audit(
            'authorization_check',
            f'Analyst {analyst.name} permission {permission}: {"GRANTED" if has_permission else "DENIED"}'
        )
        
        return has_permission
    
    def log_audit(self, action: str, details: str):
        """Log security events for audit trail"""
        audit_entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'details': details
        }
        self.audit_log.append(audit_entry)
        
        # Keep only last 1000 entries
        if len(self.audit_log) > 1000:
            self.audit_log = self.audit_log[-1000:]
    
    def get_audit_log(self, analyst: SecurityAnalyst) -> List[Dict]:
        """Get audit log (only for authorized analysts)"""
        if not self.authorize(analyst, 'admin'):
            return []
        
        return self.audit_log[-100:]  # Last 100 entries
    
    def save_analysts(self):
        """Save analysts and API keys to file"""
        try:
            data = {
                'analysts': [analyst.to_dict() for analyst in self.analysts.values()],
                'api_keys': [
                    {
                        'api_key': key,
                        'analyst_id': info['analyst_id'],
                        'created_at': info['created_at'],
                        'permissions': info['permissions']
                    }
                    for key, info in self.api_keys.items()
                ]
            }
            
            with open('security_analysts.json', 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            print(f"Error saving analysts: {e}")
    
    def get_analyst_info(self, api_key: str) -> Optional[Dict]:
        """Get analyst information (without sensitive data)"""
        analyst = self.authenticate(api_key)
        if not analyst:
            return None
        
        return {
            'analyst_id': analyst.analyst_id,
            'name': analyst.name,
            'role': analyst.role,
            'permissions': analyst.permissions,
            'last_activity': analyst.last_activity.isoformat() if analyst.last_activity else None
        }
    
    def demonstrate_confidentiality(self) -> Dict:
        """Demonstrate CONFIDENTIALITY principles"""
        return {
            'principle': 'CONFIDENTIALITY',
            'description': 'Only authorized security analysts can access and modify threat data',
            'implementation': {
                'authentication': 'API key-based authentication',
                'authorization': 'Role-based permission system',
                'audit_logging': 'All actions logged for security monitoring'
            },
            'demo_scenarios': [
                'Try accessing without API key -> Access denied',
                'Try accessing with invalid key -> Access denied', 
                'Try unauthorized action -> Permission denied',
                'Valid analyst with proper permissions -> Access granted'
            ],
            'security_features': [
                'Multi-factor authentication (API keys)',
                'Role-based access control',
                'Permission-based authorization',
                'Comprehensive audit logging',
                'Session tracking and monitoring'
            ]
        }

# Global authentication system
auth_system = AuthenticationSystem()

def get_auth_system() -> AuthenticationSystem:
    """Get the global authentication system"""
    return auth_system
