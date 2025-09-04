#!/usr/bin/env python3
"""
Configuration Test Script for Message Forwarder Bot
This script checks if all required configuration is properly set up.
"""

import os
from dotenv import load_dotenv

def test_configuration():
    """Test the bot configuration and identify issues"""
    print("🔍 Testing Bot Configuration...")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Check required environment variables
    required_vars = ['API_ID', 'API_HASH', 'PHONE', 'TARGET_GROUP_ID']
    missing_vars = []
    
    for var in required_vars:
        value = os.getenv(var)
        if not value or value == '0' or value == 'your_api_id_here':
            missing_vars.append(var)
            print(f"❌ {var}: Missing or invalid value")
        else:
            print(f"✅ {var}: Configured")
    
    # Check source group IDs
    source_group_ids_str = os.getenv('SOURCE_GROUP_IDS', '')
    if not source_group_ids_str or source_group_ids_str == '123456789,987654321,111222333,444555666,777888999':
        print("❌ SOURCE_GROUP_IDS: Not configured with actual group IDs")
    else:
        try:
            source_group_ids = [int(gid.strip()) for gid in source_group_ids_str.split(',') if gid.strip()]
            print(f"✅ SOURCE_GROUP_IDS: {len(source_group_ids)} groups configured")
            for i, gid in enumerate(source_group_ids):
                print(f"   Group {i+1}: {gid}")
        except ValueError:
            print("❌ SOURCE_GROUP_IDS: Invalid format (should be comma-separated integers)")
    
    # Check target group ID
    target_group_id = os.getenv('TARGET_GROUP_ID', '0')
    if target_group_id == '0' or target_group_id == 'your_target_group_id_here':
        print("❌ TARGET_GROUP_ID: Not configured with actual group ID")
    else:
        print(f"✅ TARGET_GROUP_ID: {target_group_id}")
    
    # Check if .env file exists
    if os.path.exists('.env'):
        print("✅ .env file exists")
    else:
        print("❌ .env file missing - create one from env_example.txt")
    
    # Check session file
    if os.path.exists('session_name.session'):
        print("✅ Session file exists")
    else:
        print("⚠️  Session file missing - will be created on first run")
    
    # Summary
    print("\n" + "=" * 50)
    if missing_vars:
        print(f"❌ Configuration incomplete! {len(missing_vars)} required variables missing.")
        print("Please update your .env file with actual values.")
        return False
    else:
        print("✅ Configuration looks good! Bot should work properly.")
        return True

if __name__ == "__main__":
    test_configuration()
