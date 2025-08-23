#!/usr/bin/env python3
"""
Test script for the new contact information feature
Tests if contact details are properly added to messages
"""

import os
import sys
from message_processor import MessageProcessor

def test_contact_information():
    """Test if contact information is properly added to messages"""
    print("🧪 Testing Contact Information Feature")
    print("=" * 50)
    
    # Create processor
    processor = MessageProcessor()
    
    # Test messages
    test_messages = [
        "Gucci wallet for £35 - Boxed",
        "NEW COLOURS available",
        "Premium quality product",
        "Watch for sale - £100",
        "iPhone 15 Pro - £800"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n📝 Test {i}: {message}")
        
        # Process message
        processed = processor.process_message({
            'text': message,
            'media': None,
            'caption': None
        })
        
        # Check if contact info was added
        if "For orders message here" in processed['text']:
            print("✅ Contact info added successfully")
        else:
            print("❌ Contact info not added")
        
        # Show final message
        print(f"📤 Final message:\n{processed['text']}")
        print("-" * 30)
    
    print("\n🎯 Contact Information Feature Test Complete!")

def test_config_loading():
    """Test if contact configuration loads properly"""
    print("\n🔧 Testing Configuration Loading")
    print("=" * 50)
    
    try:
        from config import CONTACT_INFO
        print("✅ Contact info config loaded successfully")
        print(f"   Telegram Link: {CONTACT_INFO['telegram_link']}")
        print(f"   Contact Text: {CONTACT_INFO['contact_text']}")
        print(f"   Shop Name: {CONTACT_INFO['shop_name']}")
        print(f"   Auto Add: {CONTACT_INFO['auto_add_contact']}")
    except ImportError as e:
        print(f"❌ Failed to load config: {e}")
    except KeyError as e:
        print(f"❌ Missing config key: {e}")

if __name__ == "__main__":
    print("🚀 Starting Contact Information Feature Tests")
    print("=" * 60)
    
    # Test configuration
    test_config_loading()
    
    # Test contact information addition
    test_contact_information()
    
    print("\n✨ All tests completed!")
    print("\nTo use this feature:")
    print("1. Set TELEGRAM_LINK in your .env file")
    print("2. Set CONTACT_TEXT in your .env file")
    print("3. Set AUTO_ADD_CONTACT=true in your .env file")
    print("4. Restart your bot")
