"""
Cryptography Utilities for Phishing Detection System
Implements RSA encryption, digital signatures, and key management
"""

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import json
import os
from datetime import datetime
import hashlib


class CryptoManager:
    """Manages encryption, decryption, and digital signatures"""
    
    def __init__(self, keys_dir='keys'):
        self.keys_dir = keys_dir
        os.makedirs(keys_dir, exist_ok=True)
        
        # RSA key size
        self.key_size = 2048
        
        # Paths for key files
        self.db_public_key_path = os.path.join(keys_dir, 'database_public.pem')
        self.db_private_key_path = os.path.join(keys_dir, 'database_private.pem')
        self.extension_private_key_path = os.path.join(keys_dir, 'extension_private.pem')
        self.extension_public_key_path = os.path.join(keys_dir, 'extension_public.pem')
        
        print(f"[CryptoManager] Initialized with keys directory: {keys_dir}")
    
    
    # ==================== KEY GENERATION ====================
    
    def generate_rsa_key_pair(self, key_name='database'):
        """Generate RSA public/private key pair"""
        print(f"[CryptoManager] Generating RSA key pair for: {key_name}")
        
        # Generate private key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=self.key_size,
            backend=default_backend()
        )
        
        # Generate public key
        public_key = private_key.public_key()
        
        # Serialize private key
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        # Serialize public key
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        print(f"[CryptoManager] ✅ RSA key pair generated successfully")
        return private_pem, public_pem
    
    
    def save_key_pair(self, private_pem, public_pem, key_name='database'):
        """Save key pair to files"""
        private_path = os.path.join(self.keys_dir, f'{key_name}_private.pem')
        public_path = os.path.join(self.keys_dir, f'{key_name}_public.pem')
        
        # Save private key
        with open(private_path, 'wb') as f:
            f.write(private_pem)
        print(f"[CryptoManager] Private key saved: {private_path}")
        
        # Save public key
        with open(public_path, 'wb') as f:
            f.write(public_pem)
        print(f"[CryptoManager] Public key saved: {public_path}")
        
        return private_path, public_path
    
    
    def load_private_key(self, key_path):
        """Load private key from file"""
        try:
            with open(key_path, 'rb') as f:
                private_key = serialization.load_pem_private_key(
                    f.read(),
                    password=None,
                    backend=default_backend()
                )
            print(f"[CryptoManager] ✅ Private key loaded: {key_path}")
            return private_key
        except Exception as e:
            print(f"[CryptoManager] ❌ Error loading private key: {e}")
            return None
    
    
    def load_public_key(self, key_path):
        """Load public key from file"""
        try:
            with open(key_path, 'rb') as f:
                public_key = serialization.load_pem_public_key(
                    f.read(),
                    backend=default_backend()
                )
            print(f"[CryptoManager] ✅ Public key loaded: {key_path}")
            return public_key
        except Exception as e:
            print(f"[CryptoManager] ❌ Error loading public key: {e}")
            return None
    
    
    # ==================== ENCRYPTION/DECRYPTION ====================
    
    def encrypt_data(self, data, public_key_path=None):
        """
        Encrypt data using hybrid encryption (AES + RSA)
        - Data encrypted with AES-256 (fast)
        - AES key encrypted with RSA (secure)
        """
        print(f"[CryptoManager] Encrypting data...")
        
        # Use database public key by default
        if public_key_path is None:
            public_key_path = self.db_public_key_path
        
        # Load public key
        public_key = self.load_public_key(public_key_path)
        if not public_key:
            raise Exception("Failed to load public key")
        
        # Convert data to JSON string if it's a dict
        if isinstance(data, dict):
            data = json.dumps(data)
        
        # Convert to bytes
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        # Generate random AES key (256-bit)
        aes_key = os.urandom(32)  # 32 bytes = 256 bits
        
        # Generate random IV for AES
        iv = os.urandom(16)  # 16 bytes for AES
        
        # Encrypt data with AES
        cipher = Cipher(
            algorithms.AES(aes_key),
            modes.CFB(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(data) + encryptor.finalize()
        
        # Encrypt AES key with RSA public key
        encrypted_aes_key = public_key.encrypt(
            aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        # Combine everything and encode to base64
        result = {
            'encrypted_data': base64.b64encode(encrypted_data).decode('utf-8'),
            'encrypted_key': base64.b64encode(encrypted_aes_key).decode('utf-8'),
            'iv': base64.b64encode(iv).decode('utf-8')
        }
        
        print(f"[CryptoManager] ✅ Data encrypted successfully")
        return json.dumps(result)
    
    
    def decrypt_data(self, encrypted_package, private_key_path=None):
        """
        Decrypt data using hybrid encryption
        """
        print(f"[CryptoManager] Decrypting data...")
        
        # Use database private key by default
        if private_key_path is None:
            private_key_path = self.db_private_key_path
        
        # Load private key
        private_key = self.load_private_key(private_key_path)
        if not private_key:
            raise Exception("Failed to load private key")
        
        # Parse encrypted package
        if isinstance(encrypted_package, str):
            encrypted_package = json.loads(encrypted_package)
        
        # Decode from base64
        encrypted_data = base64.b64decode(encrypted_package['encrypted_data'])
        encrypted_aes_key = base64.b64decode(encrypted_package['encrypted_key'])
        iv = base64.b64decode(encrypted_package['iv'])
        
        # Decrypt AES key with RSA private key
        aes_key = private_key.decrypt(
            encrypted_aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        # Decrypt data with AES
        cipher = Cipher(
            algorithms.AES(aes_key),
            modes.CFB(iv),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
        
        # Convert back to string
        decrypted_string = decrypted_data.decode('utf-8')
        
        # Try to parse as JSON
        try:
            result = json.loads(decrypted_string)
        except:
            result = decrypted_string
        
        print(f"[CryptoManager] ✅ Data decrypted successfully")
        return result
    
    
    # ==================== DIGITAL SIGNATURES ====================
    
    def sign_data(self, data, private_key_path=None):
        """Create digital signature for data"""
        print(f"[CryptoManager] Creating digital signature...")
        
        # Use extension private key by default for signing
        if private_key_path is None:
            private_key_path = self.extension_private_key_path
        
        # Load private key
        private_key = self.load_private_key(private_key_path)
        if not private_key:
            raise Exception("Failed to load private key for signing")
        
        # Convert data to bytes
        if isinstance(data, dict):
            data = json.dumps(data, sort_keys=True)
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        # Create signature
        signature = private_key.sign(
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        
        # Encode to base64
        signature_b64 = base64.b64encode(signature).decode('utf-8')
        
        print(f"[CryptoManager] ✅ Digital signature created")
        return signature_b64
    
    
    def verify_signature(self, data, signature, public_key_path=None):
        """Verify digital signature"""
        print(f"[CryptoManager] Verifying digital signature...")
        
        # Use extension public key by default for verification
        if public_key_path is None:
            public_key_path = self.extension_public_key_path
        
        # Load public key
        public_key = self.load_public_key(public_key_path)
        if not public_key:
            raise Exception("Failed to load public key for verification")
        
        # Convert data to bytes
        if isinstance(data, dict):
            data = json.dumps(data, sort_keys=True)
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        # Decode signature from base64
        signature_bytes = base64.b64decode(signature)
        
        # Verify signature
        try:
            public_key.verify(
                signature_bytes,
                data,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            print(f"[CryptoManager] ✅ Signature verified - Data is authentic")
            return True
        except Exception as e:
            print(f"[CryptoManager] ❌ Signature verification failed: {e}")
            return False
    
    
    # ==================== HASHING (for blockchain) ====================
    
    def hash_data(self, data):
        """Create SHA-256 hash of data"""
        if isinstance(data, dict):
            data = json.dumps(data, sort_keys=True)
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        hash_object = hashlib.sha256(data)
        return hash_object.hexdigest()
    
    
    def create_block_hash(self, previous_hash, encrypted_data, timestamp):
        """Create blockchain-style hash linking to previous block"""
        block_data = {
            'previous_hash': previous_hash,
            'encrypted_data': encrypted_data,
            'timestamp': timestamp
        }
        return self.hash_data(block_data)
    
    
    # ==================== SETUP UTILITIES ====================
    
    def setup_keys(self):
        """Generate all required keys if they don't exist"""
        print("\n" + "="*60)
        print("🔐 CRYPTO SETUP - Generating Keys")
        print("="*60 + "\n")
        
        keys_generated = False
        
        # Generate database keys
        if not os.path.exists(self.db_private_key_path):
            print("📝 Generating Database key pair...")
            private_pem, public_pem = self.generate_rsa_key_pair('database')
            self.save_key_pair(private_pem, public_pem, 'database')
            keys_generated = True
        else:
            print("✅ Database keys already exist")
        
        # Generate extension keys
        if not os.path.exists(self.extension_private_key_path):
            print("\n📝 Generating Extension key pair...")
            private_pem, public_pem = self.generate_rsa_key_pair('extension')
            self.save_key_pair(private_pem, public_pem, 'extension')
            keys_generated = True
        else:
            print("✅ Extension keys already exist")
        
        if keys_generated:
            print("\n" + "="*60)
            print("✅ Key generation complete!")
            print("="*60)
        else:
            print("\n" + "="*60)
            print("ℹ️  All keys already exist - No generation needed")
            print("="*60)
        
        return True


# ==================== TESTING FUNCTIONS ====================

def test_encryption():
    """Test encryption and decryption"""
    print("\n" + "="*60)
    print("🧪 TESTING ENCRYPTION/DECRYPTION")
    print("="*60 + "\n")
    
    crypto = CryptoManager()
    
    # Setup keys
    crypto.setup_keys()
    
    # Test data
    test_data = {
        'url': 'http://phishing-site.com',
        'probability': 0.95,
        'source': 'ML Model',
        'timestamp': datetime.now().isoformat(),
        'virustotal_reports': 5
    }
    
    print("\n📦 Original Data:")
    print(json.dumps(test_data, indent=2))
    
    # Encrypt
    print("\n🔒 Encrypting data...")
    encrypted = crypto.encrypt_data(test_data)
    print(f"Encrypted (first 100 chars): {encrypted[:100]}...")
    
    # Decrypt
    print("\n🔓 Decrypting data...")
    decrypted = crypto.decrypt_data(encrypted)
    print("Decrypted Data:")
    print(json.dumps(decrypted, indent=2))
    
    # Verify
    if decrypted == test_data:
        print("\n✅ SUCCESS: Encrypted and decrypted data match!")
    else:
        print("\n❌ ERROR: Data mismatch!")
    
    return encrypted, decrypted


def test_signatures():
    """Test digital signatures"""
    print("\n" + "="*60)
    print("🧪 TESTING DIGITAL SIGNATURES")
    print("="*60 + "\n")
    
    crypto = CryptoManager()
    
    # Test data
    test_data = {
        'url': 'http://phishing-site.com',
        'timestamp': datetime.now().isoformat()
    }
    
    print("📦 Data to sign:")
    print(json.dumps(test_data, indent=2))
    
    # Sign
    print("\n✍️ Creating signature...")
    signature = crypto.sign_data(test_data)
    print(f"Signature (first 50 chars): {signature[:50]}...")
    
    # Verify
    print("\n🔍 Verifying signature...")
    is_valid = crypto.verify_signature(test_data, signature)
    
    if is_valid:
        print("✅ SUCCESS: Signature is valid!")
    else:
        print("❌ ERROR: Signature verification failed!")
    
    # Test with tampered data
    print("\n🔍 Testing with tampered data...")
    tampered_data = test_data.copy()
    tampered_data['url'] = 'http://different-site.com'
    is_valid_tampered = crypto.verify_signature(tampered_data, signature)
    
    if not is_valid_tampered:
        print("✅ SUCCESS: Tampered data correctly rejected!")
    else:
        print("❌ ERROR: Tampered data was accepted!")


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
