# Telegram Message Forwarder Bot

A powerful Telegram bot that forwards messages from source groups to target groups with automatic modifications including pricing updates, keyword replacements, and contact information.

## Features

- **Multi-group monitoring**: Monitor multiple source groups simultaneously
- **Automatic pricing logic**: 
  - Watches: Original price + £105
  - Non-watches: Original price + 65% + £5 delivery fee
- **Keyword replacements**: Automatically replace keywords (e.g., "AAA" → "Premium")
- **Media support**: Handles photos, videos, documents, and audio files
- **Album support**: Properly forwards media albums
- **Delivery message**: Automatically adds delivery information
- **Contact information**: Automatically adds order contact details
- **Group-specific settings**: Customize settings for each source group

## New Feature: Contact Information

The bot now automatically adds contact information to every forwarded message, making it easy for users to place orders:

- **Contact text**: "For orders message here"
- **Telegram link**: Direct link to your shop (e.g., https://t.me/BFSshopuk)
- **Configurable**: Can be enabled/disabled via environment variables

## Configuration

Create a `.env` file with the following variables:

```env
# Telegram API credentials
API_ID=your_telegram_api_id
API_HASH=your_telegram_api_hash
PHONE=your_phone_number

# Group IDs
SOURCE_GROUP_IDS=group_id1,group_id2,group_id3
SOURCE_GROUP_NAMES="Group Name 1,Group Name 2,Group Name 3"
TARGET_GROUP_ID=target_group_id

# Message settings
MESSAGE_DELAY=2

# Group-specific delays (optional)
GROUP_1_DELAY=2
GROUP_2_DELAY=3
GROUP_3_DELAY=2

# Contact information for orders
TELEGRAM_LINK=https://t.me/BFSshopuk
CONTACT_TEXT=For orders message here
SHOP_NAME=BFS
AUTO_ADD_CONTACT=true
```

## Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Configure your `.env` file
4. Run the bot: `python bot.py`

## Usage

The bot will:
1. Monitor specified source groups
2. Process incoming messages with pricing logic
3. Add delivery information
4. Add contact information for orders
5. Forward modified messages to target group

## Hosting on AWS EC2

See the detailed hosting guide in the project documentation for AWS EC2 deployment instructions.

## License

This project is licensed under the MIT License.
