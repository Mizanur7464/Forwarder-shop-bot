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
    
    SOURCE_GROUP_SETTINGS[group_id] = {
        'name': group_name,
        'enabled': True,
        'message_delay': group_delay,
        'watch_keywords': WATCH_KEYWORDS.copy(),
        'pricing_logic': PRICING_LOGIC.copy(),
        'delivery_message': DELIVERY_MESSAGE
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


