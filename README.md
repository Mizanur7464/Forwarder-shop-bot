# Message Forwarder Bot

A Telegram bot that forwards messages from multiple source groups to a target group with automatic modifications including pricing updates, keyword replacements, and source group identification.

## Features

- **Multi-Source Group Support**: Monitor multiple source groups simultaneously
- **Source Group Identification**: Each forwarded message shows a letter prefix indicating its source group
- **Automatic Pricing Logic**: 
  - Watches: Original price + £105
  - Non-watches: Original price + 65% + £5 delivery fee
- **Keyword Replacements**: Automatic text modifications
- **Media Support**: Handles photos, videos, documents, and audio files
- **Album Support**: Properly forwards media albums
- **Group-Specific Settings**: Custom delays and settings per source group

## Source Group Letter Mapping

The bot automatically adds a letter prefix to each forwarded message to identify its source:

- **S** - Sam's group
- **R** - Raaf's group  
- **M** - Mr Sunny's group
- **A** - Amid's group
- **J** - Joyce's group

Example: `[S] Product description` indicates the message came from Sam's group.

## Setup

1. **Install dependencies**:
   ```bash
   pip install telethon python-dotenv
   ```

2. **Configure environment**:
   - Copy `env_example.txt` to `.env`
   - Fill in your Telegram API credentials
   - Add your source group IDs and target group ID

3. **Update source group letters**:
   - Edit `config.py`
   - Update `SOURCE_GROUP_LETTERS` with your actual group IDs

4. **Run the bot**:
   ```bash
   python bot.py
   ```

## Configuration

### Environment Variables

- `SOURCE_GROUP_IDS`: Comma-separated list of source group IDs
- `TARGET_GROUP_ID`: ID of the target group for forwarding
- `MESSAGE_DELAY`: Delay between forwarded messages (seconds)
- `GROUP_X_DELAY`: Individual group delays (optional)

### Source Group Settings

Each source group can have custom:
- Message delays
- Watch keywords
- Pricing logic
- Delivery messages

## Usage

1. The bot automatically monitors all configured source groups
2. When a message is received, it:
   - Adds source group letter identification
   - Applies pricing logic
   - Modifies keywords
   - Forwards to target group
3. All messages show `[LETTER]` prefix for easy identification

## Example Output

```
[S] Casio Watch - £150
Quick Free delivery 3/4 days
For orders message here
https://t.me/BFSshopuk
```

## Support

For issues or questions, please check the configuration and ensure all group IDs are correct.
