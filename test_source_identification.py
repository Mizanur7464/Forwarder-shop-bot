#!/usr/bin/env python3
"""
Test script for source group letter identification feature
This script demonstrates how the bot will add letters to messages based on source groups
"""

from config import SOURCE_GROUP_LETTERS, SOURCE_GROUP_SETTINGS
from message_processor import MessageProcessor

def test_source_identification():
    """Test the source group letter identification feature"""
    print("🔍 Testing Source Group Letter Identification Feature")
    print("=" * 60)
    
    # Show configured source groups
    print("\n📋 Configured Source Groups:")
    print("-" * 40)
    
    if not SOURCE_GROUP_LETTERS:
        print("❌ No source group letters configured!")
        print("Please update SOURCE_GROUP_LETTERS in config.py")
        return
    
    for group_id, letter in SOURCE_GROUP_LETTERS.items():
        group_name = SOURCE_GROUP_SETTINGS.get(group_id, {}).get('name', 'Unknown')
        print(f"  {letter} → Group {group_id} ({group_name})")
    
    # Test message processing
    print("\n🧪 Testing Message Processing:")
    print("-" * 40)
    
    processor = MessageProcessor()
    
    # Test messages from different source groups
    test_messages = [
        {
            'group_id': list(SOURCE_GROUP_LETTERS.keys())[0] if SOURCE_GROUP_LETTERS else 123456789,
            'text': 'Casio Watch - £150',
            'description': 'Watch product message'
        },
        {
            'group_id': list(SOURCE_GROUP_LETTERS.keys())[1] if len(SOURCE_GROUP_LETTERS) > 1 else 987654321,
            'text': 'Samsung Phone - £200',
            'description': 'Phone product message'
        }
    ]
    
    for i, test_msg in enumerate(test_messages, 1):
        print(f"\nTest {i}: {test_msg['description']}")
        print(f"Source Group: {test_msg['group_id']}")
        print(f"Original Text: {test_msg['text']}")
        
        # Process the message
        processed = processor.process_message({
            'text': test_msg['text']
        }, test_msg['group_id'])
        
        print(f"Processed Text: {processed['text']}")
        print("-" * 30)
    
    # Show configuration instructions
    print("\n📝 Configuration Instructions:")
    print("-" * 40)
    print("1. Update SOURCE_GROUP_LETTERS in config.py with your actual group IDs")
    print("2. Example:")
    print("   SOURCE_GROUP_LETTERS = {")
    print("       123456789: 'S',  # Sam's group")
    print("       987654321: 'R',  # Raaf's group")
    print("       111222333: 'M',  # Mr Sunny's group")
    print("       444555666: 'A',  # Amid's group")
    print("       777888999: 'J',  # Joyce's group")
    print("   }")
    print("\n3. Update your .env file with actual group IDs")
    print("4. Restart the bot")
    
    print("\n✅ Test completed!")

if __name__ == "__main__":
    try:
        test_source_identification()
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        print("Make sure config.py is properly configured")
