#!/usr/bin/env python3
"""
Comprehensive Configuration Validation for Message Forwarder Bot
This script validates all configuration aspects and provides detailed feedback.
"""

import os
import sys
from dotenv import load_dotenv

def validate_configuration():
    """Validate the complete bot configuration"""
    print("🔍 Comprehensive Bot Configuration Validation")
    print("=" * 60)
    
    # Load environment variables
    load_dotenv()
    
    # Track validation results
    validation_results = {
        'env_file': False,
        'api_credentials': False,
        'group_ids': False,
        'source_groups': False,
        'target_group': False,
        'session_file': False
    }
    
    # 1. Check .env file
    print("\n📁 1. Environment File Check:")
    if os.path.exists('.env'):
        print("   ✅ .env file exists")
        validation_results['env_file'] = True
    else:
        print("   ❌ .env file missing!")
        print("   💡 Create .env file from env_example.txt")
        return False
    
    # 2. Check API credentials
    print("\n🔑 2. API Credentials Check:")
    api_id = os.getenv('API_ID')
    api_hash = os.getenv('API_HASH')
    phone = os.getenv('PHONE')
    
    if api_id and api_id != 'your_api_id_here':
        print(f"   ✅ API_ID: {api_id[:8]}...")
    else:
        print("   ❌ API_ID: Missing or invalid")
        validation_results['api_credentials'] = False
    
    if api_hash and api_hash != 'your_api_hash_here':
        print(f"   ✅ API_HASH: {api_hash[:8]}...")
    else:
        print("   ❌ API_HASH: Missing or invalid")
        validation_results['api_credentials'] = False
    
    if phone and phone != 'your_phone_number_here':
        print(f"   ✅ PHONE: {phone}")
    else:
        print("   ❌ PHONE: Missing or invalid")
        validation_results['api_credentials'] = False
    
    if all([api_id, api_hash, phone]) and \
       api_id != 'your_api_id_here' and \
       api_hash != 'your_api_hash_here' and \
       phone != 'your_phone_number_here':
        validation_results['api_credentials'] = True
    
    # 3. Check source group IDs
    print("\n📤 3. Source Group IDs Check:")
    source_group_ids_str = os.getenv('SOURCE_GROUP_IDS', '')
    
    if not source_group_ids_str:
        print("   ❌ SOURCE_GROUP_IDS: Not configured")
        validation_results['source_groups'] = False
    elif source_group_ids_str == '123456789,987654321,111222333,444555666,777888999':
        print("   ❌ SOURCE_GROUP_IDS: Still using example values")
        validation_results['source_groups'] = False
    else:
        try:
            source_group_ids = [
                int(gid.strip()) 
                for gid in source_group_ids_str.split(',') 
                if gid.strip()
            ]
            if source_group_ids:
                print(f"   ✅ SOURCE_GROUP_IDS: {len(source_group_ids)} groups")
                for i, gid in enumerate(source_group_ids):
                    print(f"      Group {i+1}: {gid}")
                validation_results['source_groups'] = True
            else:
                print("   ❌ SOURCE_GROUP_IDS: Empty after parsing")
                validation_results['source_groups'] = False
        except ValueError:
            print("   ❌ SOURCE_GROUP_IDS: Invalid format")
            validation_results['source_groups'] = False
    
    # 4. Check target group ID
    print("\n📥 4. Target Group ID Check:")
    target_group_id = os.getenv('TARGET_GROUP_ID', '0')
    
    if target_group_id == '0' or target_group_id == 'your_target_group_id_here':
        print("   ❌ TARGET_GROUP_ID: Not configured")
        validation_results['target_group'] = False
    else:
        try:
            target_id = int(target_group_id)
            print(f"   ✅ TARGET_GROUP_ID: {target_id}")
            validation_results['target_group'] = True
        except ValueError:
            print("   ❌ TARGET_GROUP_ID: Invalid format")
            validation_results['target_group'] = False
    
    # 5. Check session file
    print("\n💾 5. Session File Check:")
    if os.path.exists('session_name.session'):
        file_size = os.path.getsize('session_name.session')
        print(f"   ✅ Session file exists ({file_size} bytes)")
        validation_results['session_file'] = True
    else:
        print("   ⚠️  Session file missing (will be created on first run)")
        validation_results['session_file'] = True  # Not critical
    
    # 6. Check config.py source group letters
    print("\n🔤 6. Source Group Letters Check:")
    try:
        # Import config to check SOURCE_GROUP_LETTERS
        sys.path.append('.')
        from config import SOURCE_GROUP_LETTERS, SOURCE_GROUP_IDS
        
        if SOURCE_GROUP_LETTERS:
            print(f"   ✅ SOURCE_GROUP_LETTERS: {len(SOURCE_GROUP_LETTERS)} mappings")
            for group_id, letter in SOURCE_GROUP_LETTERS.items():
                print(f"      Group {group_id}: {letter}")
        else:
            print("   ❌ SOURCE_GROUP_LETTERS: Empty dictionary")
            print("   💡 Update config.py with actual group IDs")
        
        if SOURCE_GROUP_IDS:
            print(f"   ✅ SOURCE_GROUP_IDS loaded: {len(SOURCE_GROUP_IDS)} groups")
        else:
            print("   ❌ SOURCE_GROUP_IDS: No groups loaded")
            
    except ImportError as e:
        print(f"   ❌ Error importing config: {e}")
    except Exception as e:
        print(f"   ❌ Error checking config: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 VALIDATION SUMMARY:")
    
    critical_checks = ['env_file', 'api_credentials', 'source_groups', 'target_group']
    passed_critical = sum(validation_results[check] for check in critical_checks)
    total_critical = len(critical_checks)
    
    if passed_critical == total_critical:
        print("🎉 CONGRATULATIONS! All critical checks passed!")
        print("✅ Your bot should work properly now!")
        return True
    else:
        print(f"❌ Configuration incomplete! {passed_critical}/{total_critical} critical checks passed.")
        print("\n🔧 REQUIRED ACTIONS:")
        
        if not validation_results['env_file']:
            print("   • Create .env file from env_example.txt")
        
        if not validation_results['api_credentials']:
            print("   • Get API_ID and API_HASH from my.telegram.org")
            print("   • Add your phone number to .env")
        
        if not validation_results['source_groups']:
            print("   • Add actual source group IDs to .env")
            print("   • Update SOURCE_GROUP_LETTERS in config.py")
        
        if not validation_results['target_group']:
            print("   • Add actual target group ID to .env")
        
        return False

if __name__ == "__main__":
    try:
        success = validate_configuration()
        if success:
            print("\n🚀 Ready to run: python bot.py")
        else:
            print("\n⚠️  Fix the issues above before running the bot")
    except Exception as e:
        print(f"\n💥 Validation error: {e}")
        print("Please check your configuration files")
