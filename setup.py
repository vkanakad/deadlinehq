#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Setup script for DeadlineHQ."""
import os
import shutil
import sys
import io

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


def create_config():
    """Create config.json from example if it doesn't exist."""
    if os.path.exists('config.json'):
        print("✓ config.json already exists")
        return
    
    if not os.path.exists('config.json.example'):
        print("✗ config.json.example not found!")
        return
    
    shutil.copy('config.json.example', 'config.json')
    print("✓ Created config.json from example")
    print("  Please edit config.json with your email settings")


def create_directories():
    """Create necessary directories."""
    directories = ['logs', 'backups']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✓ Created {directory}/ directory")
        else:
            print(f"✓ {directory}/ directory already exists")


def check_environment_variables():
    """Check if required environment variables are set."""
    print("\nChecking environment variables:")
    
    resend_key = os.getenv('DEADLINEHQ_RESEND_API_KEY')
    email_password = os.getenv('DEADLINEHQ_EMAIL_PASSWORD')
    sender_email = os.getenv('DEADLINEHQ_SENDER_EMAIL')
    
    print("\n  [Resend provider]")
    if resend_key:
        print("  ✓ DEADLINEHQ_RESEND_API_KEY is set")
    else:
        print("  - DEADLINEHQ_RESEND_API_KEY not set")
        print("    Get a free key at https://resend.com/api-keys")
    
    print("\n  [SMTP provider]")
    if email_password:
        print("  ✓ DEADLINEHQ_EMAIL_PASSWORD is set")
    else:
        print("  - DEADLINEHQ_EMAIL_PASSWORD not set")
    
    if sender_email:
        print(f"  ✓ DEADLINEHQ_SENDER_EMAIL is set to {sender_email}")
    else:
        print("  - DEADLINEHQ_SENDER_EMAIL not set")
    
    if not resend_key and not email_password:
        print("\n  ⚠ No email provider configured.")
        print("    Email notifications are optional — task management works without them.")
        print("    To enable emails, set up either Resend (easiest) or SMTP.")
        print("    See README.md for instructions.")


def check_dependencies():
    """Check if required packages are installed."""
    print("\nChecking dependencies:")
    
    try:
        import schedule
        print("✓ schedule is installed")
    except ImportError:
        print("✗ schedule is not installed")
        print("  Install with: pip install schedule")
    
    try:
        import pytest
        print("✓ pytest is installed")
    except ImportError:
        print("⚠ pytest is not installed (only needed for testing)")
        print("  Install with: pip install pytest")
    
    try:
        import resend
        print("✓ resend is installed")
    except ImportError:
        print("⚠ resend is not installed (only needed for Resend email provider)")
        print("  Install with: pip install resend")


def print_next_steps():
    """Print next steps for the user."""
    print("\n" + "="*60)
    print("Setup Complete!")
    print("="*60)
    print("\nNext steps:")
    print("1. Edit config.json with your email SMTP settings")
    print("2. Set environment variables (see above)")
    print("3. Set up email (optional — choose one):")
    print("   Resend (easiest): Get API key at https://resend.com/api-keys")
    print("   SMTP/Gmail: Generate App Password at https://myaccount.google.com/apppasswords")
    print("\n4. Test the system:")
    print("   python main.py create \"Test Task\" \"Test Description\" \"2024-12-31T23:59:59\"")
    print("   python main.py list")
    print("\n5. Run tests (optional):")
    print("   pytest tests/")
    print("\n6. Start the scheduler:")
    print("   python main.py start")
    print("\nFor more information, see README.md")
    print("="*60)


def main():
    """Run setup."""
    print("DeadlineHQ - Setup")
    print("="*60)
    
    create_config()
    create_directories()
    check_dependencies()
    check_environment_variables()
    print_next_steps()


if __name__ == '__main__':
    main()
