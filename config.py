import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Telethon MTProto API credentials
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
PHONE = os.getenv('PHONE')

# Group IDs
# Support multiple source groups as per buyer's requirement
SOURCE_GROUP_ID_STRS = os.getenv('SOURCE_GROUP_IDS', '').split(',')
if SOURCE_GROUP_ID_STRS == [''] or not any(
    s.strip() for s in SOURCE_GROUP_ID_STRS
):
    # Fallback to single source group for backward compatibility
    single_id_str = os.getenv('SOURCE_GROUP_ID', '0').strip()
    SOURCE_GROUP_IDS = [int(single_id_str)] if single_id_str else []
else:
    # Convert string IDs to integers
    SOURCE_GROUP_IDS = [
        int(gid.strip())
        for gid in SOURCE_GROUP_ID_STRS
        if gid.strip()
    ]

TARGET_GROUP_ID = int(os.getenv('TARGET_GROUP_ID', 0))

# Message settings
MESSAGE_DELAY = int(os.getenv('MESSAGE_DELAY', 2))

# Buyer's specific requirements
# Watch detection keywords
WATCH_KEYWORDS = [
    'watch', 'watchs', 'watches', 'timepiece', 'chronograph',
    'analog', 'digital watch', 'luxury watch', 'sports watch',
    'casio', 'rolex', 'omega', 'seiko', 'citizen',
    'tag', 'hublot', 'breitling', 'ap', 'audemars'
]

# Pricing logic as per buyer's requirements
PRICING_LOGIC = {
    'watch_multiplier': 105,  # Flat £105 for watches
    'non_watch_multiplier': 1.65,  # 65% increase for non-watches
    'non_watch_delivery_fee': 5,  # £5 delivery fee for non-watches
    'delivery_included': True,  # Delivery included in price
    'round_up_prices': True  # Round up prices to remove pence
}

# Delivery message to append
DELIVERY_MESSAGE = "Quick Free delivery 3/4 days"

# Multiple source group monitoring settings
MULTI_SOURCE_MONITORING = len(SOURCE_GROUP_IDS) > 1
_source_group_names_raw = os.getenv('SOURCE_GROUP_NAMES', '')
SOURCE_GROUP_NAMES = (
    _source_group_names_raw.split(',') if _source_group_names_raw else []
)
if not SOURCE_GROUP_NAMES:
    SOURCE_GROUP_NAMES = [
        f"Source Group {i + 1}"
        for i in range(len(SOURCE_GROUP_IDS))
    ]

# Source group letter mapping for identification
# Update these with your actual group IDs from .env file
SOURCE_GROUP_LETTERS: dict[int, str] = {
    -1001879591244: 'S',  # Sam's group
    -1001629586121: 'A',  # Amid's group  
    -1002854862865: 'M',  # Mr Sunny's group
    -1001778841365: 'R',  # Raaf's group
    -1001623053408: 'J',  # Joyce's group
}

# Source group specific settings
SOURCE_GROUP_SETTINGS = {}
for i, group_id in enumerate(SOURCE_GROUP_IDS):
    group_name = (
        SOURCE_GROUP_NAMES[i] 
        if i < len(SOURCE_GROUP_NAMES) 
        else f"Source Group {i+1}"
    )
    
    # Get group-specific delay
    group_delay_key = f'GROUP_{i+1}_DELAY'
    group_delay = int(os.getenv(group_delay_key, MESSAGE_DELAY))
    
    # Get group letter for identification (use default if not in SOURCE_GROUP_LETTERS)
    group_letter = SOURCE_GROUP_LETTERS.get(group_id, f"G{i+1}")
    
    # Custom delivery message for specific groups
    custom_delivery_message = DELIVERY_MESSAGE
    # Joyce's group gets different delivery time
    if group_id == -1001623053408:  # Joyce's group
        custom_delivery_message = "2/4 weeks delivery"
    
    SOURCE_GROUP_SETTINGS[group_id] = {
        'name': group_name,
        'enabled': True,
        'message_delay': group_delay,
        'watch_keywords': WATCH_KEYWORDS.copy(),
        'pricing_logic': PRICING_LOGIC.copy(),
        'delivery_message': custom_delivery_message,
        'letter': group_letter  # Add letter identification
    }

# Price update rules (keeping existing for backward compatibility)
PRICE_UPDATE_RULES = {
    '1000': '1200',  # 1000 → 1200
    '500': '600',    # 500 → 600
    '85': '95',      # £85 → £95
    '90': '100',     # £90 → £100
    '50': '60',      # £50 → £60
    '30': '35',      # £30 → £35
    '25': '30',      # £25 → £30
}

# Keyword replacements
KEYWORD_REPLACEMENTS = {
    'AAA': 'Premium',
    'NEW STOCK': 'FRESH STOCK',
    'old': 'new',
    'cheap': 'affordable',
}

# Contact information for orders
CONTACT_INFO = {
    'telegram_link': os.getenv('TELEGRAM_LINK', 'https://t.me/BFSshopuk'),
    'contact_text': os.getenv('CONTACT_TEXT', 'For orders message here'),
    'shop_name': os.getenv('SHOP_NAME', 'BFS'),
    'auto_add_contact': os.getenv('AUTO_ADD_CONTACT', 'true').lower() == 'true'
}

# 🚀 Quick Setup Guide:
# 1. উপরের commented lines গুলো uncomment করুন (# remove করুন)
# 2. 123456789 এর জায়গায় আপনার actual Telegram group ID দিন
# 3. Letters ('S', 'R', 'M', 'A', 'J') ঠিক রাখুন
# 4. .env ফাইলে SOURCE_GROUP_IDS আপডেট করুন
# 5. Bot restart করুন
#
# 📋 Example Configuration (আপনার actual IDs দিয়ে replace করুন):
# SOURCE_GROUP_LETTERS = {
#     555666777: 'S',  # Sam's group (আপনার actual group ID)
#     888999000: 'R',  # Raaf's group
#     111222333: 'M',  # Mr Sunny's group
#     444555666: 'A',  # Amid's group
#     777888999: 'J',  # Joyce's group
# }


