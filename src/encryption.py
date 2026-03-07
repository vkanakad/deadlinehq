"""Encryption utilities for DeadlineHQ.

Uses Fernet symmetric encryption (AES-128-CBC) from the cryptography library.
The encryption key is stored in the DEADLINEHQ_ENCRYPTION_KEY environment variable.

To generate a new key:
    python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
"""
import os
import base64
from cryptography.fernet import Fernet


def get_encryption_key() -> bytes:
    """Get the encryption key from environment variable.
    
    Returns:
        Fernet key as bytes
        
    Raises:
        ValueError: If the environment variable is not set
    """
    key = os.getenv('DEADLINEHQ_ENCRYPTION_KEY')
    if not key:
        raise ValueError(
            "Encryption key not found. Please set DEADLINEHQ_ENCRYPTION_KEY environment variable.\n"
            "Generate a new key with: python -c \"from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())\""
        )
    return key.encode()


def encrypt_file(input_path: str, output_path: str):
    """Encrypt a file using Fernet encryption.
    
    Args:
        input_path: Path to the plain text file
        output_path: Path to write the encrypted file
    """
    key = get_encryption_key()
    fernet = Fernet(key)
    
    with open(input_path, 'rb') as f:
        data = f.read()
    
    encrypted = fernet.encrypt(data)
    
    with open(output_path, 'wb') as f:
        f.write(encrypted)


def decrypt_file(input_path: str, output_path: str):
    """Decrypt a file using Fernet encryption.
    
    Args:
        input_path: Path to the encrypted file
        output_path: Path to write the decrypted file
    """
    key = get_encryption_key()
    fernet = Fernet(key)
    
    with open(input_path, 'rb') as f:
        encrypted = f.read()
    
    decrypted = fernet.decrypt(encrypted)
    
    with open(output_path, 'wb') as f:
        f.write(decrypted)


def encrypt_data(data: str) -> str:
    """Encrypt a string and return base64-encoded ciphertext.
    
    Args:
        data: Plain text string to encrypt
        
    Returns:
        Base64-encoded encrypted string
    """
    key = get_encryption_key()
    fernet = Fernet(key)
    return fernet.encrypt(data.encode()).decode()


def decrypt_data(encrypted: str) -> str:
    """Decrypt a base64-encoded ciphertext string.
    
    Args:
        encrypted: Base64-encoded encrypted string
        
    Returns:
        Decrypted plain text string
    """
    key = get_encryption_key()
    fernet = Fernet(key)
    return fernet.decrypt(encrypted.encode()).decode()
