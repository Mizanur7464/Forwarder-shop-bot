# Telegram Message Forwarder Bot

## 🎯 Buyer's Requirements (Implemented)

This bot was built according to specific buyer requirements:

### 📱 Core Functionality
- **Copies posts** from a source group to target group
- **Images remain exactly the same** as source
- **Auto-detects new posts** in source group

### 💰 Pricing Logic
- **Watch Products:** Original price + flat £105 (delivery included)
- **Non-Watch Products:** Original price + 65% + £5 (delivery included)

### 🔍 Watch Detection
Automatically identifies watches using keywords:
- `watch`, `watchs`, `watches`
- `timepiece`, `chronograph`
- `analog`, `digital watch`
- `luxury watch`, `sports watch`
- Brand names: `casio`, `rolex`, `omega`, `seiko`, `citizen`

### 📝 Description Enhancement
- **Keeps original description**
- **Appends:** "Quick Free delivery 3/4 days"

## 🚀 Features

### ✅ Implemented
1. **Smart Watch Detection** - Automatically identifies watch products
2. **Dynamic Pricing** - Applies different pricing rules for watches vs non-watches
3. **Delivery Message** - Automatically adds delivery information
4. **Price Conversion** - Supports multiple currency formats (£, $, ৳)
5. **Media Forwarding** - Images and files forwarded unchanged
6. **Real-time Processing** - Monitors source group for new messages

### 📊 Pricing Examples

#### Watch Product
- **Original:** £50
- **New Price:** £155 (£50 + £105)
- **Includes:** Delivery

#### Non-Watch Product
- **Original:** £100
- **New Price:** £170 (£100 × 1.65 + £5)
- **Includes:** Delivery

## 🛠️ Technical Details

### Dependencies
- `telethon` - Telegram client library
- `python-dotenv` - Environment variable management
- `asyncio` - Asynchronous programming

### Configuration
- **API Credentials:** Telegram API ID, Hash, Phone
- **Group IDs:** Source and target group identifiers
- **Pricing Rules:** Configurable multipliers and fees
- **Keywords:** Customizable watch detection terms

### File Structure
```
├── bot.py                 # Main bot logic
├── message_processor.py   # Message processing & pricing
├── config.py             # Configuration & settings
├── requirements.txt      # Python dependencies
└── test_buyer_requirements.py  # Test suite
```

## 🧪 Testing

Run the test suite to verify all features:

```bash
python test_buyer_requirements.py
```

This will test:
- Watch detection accuracy
- Pricing calculations
- Delivery message appending
- Full message processing

## 🔧 Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   ```bash
   cp env_example.txt .env
   # Edit .env with your Telegram API credentials
   ```

3. **Run the bot:**
   ```bash
   python bot.py
   ```

## 📋 Demo Requirements Met

✅ **3-5 sample posts** including:
- ✅ **Watch product** (Casio G-Shock example)
- ✅ **Non-watch product** (iPhone example)
- ✅ **Price calculations** working correctly
- ✅ **Delivery message** automatically added
- ✅ **Image forwarding** preserved

## 💡 Customization

### Adding More Watch Keywords
Edit `config.py`:
```python
WATCH_KEYWORDS = [
    'watch', 'watchs', 'watches',
    # Add your custom keywords here
    'luxury timepiece', 'premium watch'
]
```

### Modifying Pricing Logic
Edit `config.py`:
```python
PRICING_LOGIC = {
    'watch_multiplier': 105,        # Change flat fee
    'non_watch_multiplier': 1.65,   # Change percentage
    'non_watch_delivery_fee': 5,    # Change delivery fee
}
```

### Changing Delivery Message
Edit `config.py`:
```python
DELIVERY_MESSAGE = "Your custom delivery message here"
```

## 🔒 Security

- API credentials stored in environment variables
- No hardcoded sensitive information
- Secure Telegram authentication via Telethon

## 📞 Support

For technical support or customization requests, please refer to the original project specifications or contact the development team.

---

**Status:** ✅ **All Buyer Requirements Implemented and Tested**
