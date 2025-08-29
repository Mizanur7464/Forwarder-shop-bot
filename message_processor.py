import re
import logging
from typing import Dict, Any
from config import (
    PRICE_UPDATE_RULES, 
    KEYWORD_REPLACEMENTS,
    WATCH_KEYWORDS,
    PRICING_LOGIC,
    DELIVERY_MESSAGE
)


logger = logging.getLogger(__name__)


class MessageProcessor:
    """Handles message content extraction and modification for Telethon"""
    
    def __init__(self):
        self.price_patterns = [
            r'(\d+)\s*(?:taka|tk|৳)',
            r'৳\s*(\d+)',
            r'price[:\s]*(\d+)',
            r'cost[:\s]*(\d+)',
            r'(\d+)\s*(?:rs|rupees?)',
            r'£(\d+)',  # British pound
            r'\$(\d+)',  # US dollar
        ]
    
    def process_message(self, message_data: Dict[str, Any], source_group_id: int = None) -> Dict[str, Any]:
        """Process message and return modified content"""
        try:
            # Extract content
            content = self.extract_content(message_data)
            
            # Add source group letter identification
            if source_group_id:
                content = self._add_source_identification(
                    content, source_group_id)
            
            # Modify text with group-specific settings
            if content['text']:
                content['text'] = self.modify_text(content['text'], source_group_id)
            if content['caption']:
                content['caption'] = self.modify_text(content['caption'], source_group_id)
            
            return content
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return message_data
    
    def extract_content(self, message_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract text and media content from message"""
        content = {
            'text': '',
            'media': [],
            'media_type': None,
            'caption': ''
        }
        
        # Extract text
        if message_data.get('text'):
            content['text'] = message_data['text']
        elif message_data.get('caption'):
            content['text'] = message_data['caption']
            content['caption'] = message_data['caption']
        
        # Extract media - prioritize message.media for albums
        if message_data.get('media'):
            # message.media contains all media in album
            media_list = []
            # Check if it's a list (multiple media) or single media
            if isinstance(message_data['media'], list):
                for media in message_data['media']:
                    if hasattr(media, 'photo'):
                        media_list.append(media.photo)
                    elif hasattr(media, 'video'):
                        media_list.append(media.video)
                    elif hasattr(media, 'document'):
                        media_list.append(media.document)
                    elif hasattr(media, 'audio'):
                        media_list.append(media.audio)
            else:
                # Single media object
                media = message_data['media']
                if hasattr(media, 'photo'):
                    media_list.append(media.photo)
                    content['media_type'] = 'photo'
                elif hasattr(media, 'video'):
                    media_list.append(media.video)
                    content['media_type'] = 'video'
                elif hasattr(media, 'document'):
                    media_list.append(media.document)
                    content['media_type'] = 'document'
                elif hasattr(media, 'audio'):
                    media_list.append(media.audio)
                    content['media_type'] = 'audio'
            
            if media_list:
                content['media'] = media_list
                # Determine media type from first media if not set
                if not content['media_type']:
                    if hasattr(message_data['media'][0], 'photo'):
                        content['media_type'] = 'photo'
                    elif hasattr(message_data['media'][0], 'video'):
                        content['media_type'] = 'video'
                    elif hasattr(message_data['media'][0], 'document'):
                        content['media_type'] = 'document'
                    elif hasattr(message_data['media'][0], 'audio'):
                        content['media_type'] = 'audio'
        
        # Fallback to individual media fields
        elif message_data.get('photo'):
            # Handle multiple photos
            if isinstance(message_data['photo'], list):
                content['media'] = message_data['photo']
            else:
                content['media'] = [message_data['photo']]
            content['media_type'] = 'photo'
        elif message_data.get('video'):
            if isinstance(message_data['video'], list):
                content['media'] = message_data['video']
            else:
                content['media'] = [message_data['video']]
            content['media_type'] = 'video'
        elif message_data.get('document'):
            if isinstance(message_data['document'], list):
                content['media'] = message_data['document']
            else:
                content['media'] = [message_data['document']]
            content['media_type'] = 'document'
        elif message_data.get('audio'):
            if isinstance(message_data['audio'], list):
                content['media'] = message_data['audio']
            else:
                content['media'] = [message_data['audio']]
            content['media_type'] = 'audio'
        
        return content
    
    def _add_source_identification(self, content: Dict[str, Any], 
                                 source_group_id: int) -> Dict[str, Any]:
        """Add source group letter identification to message content"""
        try:
            from config import SOURCE_GROUP_SETTINGS
            group_settings = SOURCE_GROUP_SETTINGS.get(source_group_id, {})
            group_letter = group_settings.get('letter', f'G{source_group_id}')
            
            # Add letter prefix to text and caption
            if content['text']:
                content['text'] = f"[{group_letter}] {content['text']}"
            if content['caption']:
                content['caption'] = f"[{group_letter}] {content['caption']}"
                
            return content
        except Exception as e:
            logger.error(f"Error adding source identification: {e}")
            return content
        """Add source group letter identification to message content"""
        try:
            from config import SOURCE_GROUP_SETTINGS
            group_settings = SOURCE_GROUP_SETTINGS.get(source_group_id, {})
            group_letter = group_settings.get('letter', f'G{source_group_id}')
            
            # Add letter prefix to text and caption
            if content['text']:
                content['text'] = f"[{group_letter}] {content['text']}"
            if content['caption']:
                content['caption'] = f"[{group_letter}] {content['caption']}"
                
            return content
        except Exception as e:
            logger.error(f"Error adding source identification: {e}")
            return content
    
    def _add_source_identification(self, content: Dict[str, Any], 
                                 source_group_id: int) -> Dict[str, Any]:
        """Add source group letter identification to message content"""
        try:
            from config import SOURCE_GROUP_SETTINGS
            group_settings = SOURCE_GROUP_SETTINGS.get(source_group_id, {})
            group_letter = group_settings.get('letter', f'G{source_group_id}')
            
            # Add letter prefix to text and caption
            if content['text']:
                content['text'] = f"[{group_letter}] {content['text']}"
            if content['caption']:
                content['caption'] = f"[{group_letter}] {content['caption']}"
                
            return content
        except Exception as e:
            logger.error(f"Error adding source identification: {e}")
            return content
    
    def modify_text(self, text: str, source_group_id: int = None) -> str:
        """Apply all text modifications with group-specific settings"""
        if not text:
            return text
        
        # Get group-specific settings
        group_settings = self._get_group_settings(source_group_id)
        
        modified_text = text
        
        # Apply buyer's specific pricing logic
        modified_text = self._apply_buyer_pricing_logic(modified_text, group_settings)
        
        # Apply price updates (keeping existing for backward compatibility)
        modified_text = self._update_prices(modified_text)
        
        # Apply keyword replacements
        modified_text = self._replace_keywords(modified_text)
        
        # Append delivery message as per buyer's requirement
        modified_text = self._append_delivery_message(modified_text, group_settings)
        
        return modified_text

    def _get_group_settings(self, source_group_id: int = None) -> dict:
        """Get group-specific settings from config if available"""
        try:
            if source_group_id is None:
                return {}
            # Lazy import to avoid circular import at module import time
            from config import SOURCE_GROUP_SETTINGS  # noqa: WPS433
            return SOURCE_GROUP_SETTINGS.get(source_group_id, {})
        except Exception:  # pragma: no cover - fallback if config missing
            return {}
    
    def _update_prices(self, text: str) -> str:
        """Update prices in text based on rules"""
        for old_price, new_price in PRICE_UPDATE_RULES.items():
            # Replace exact price matches
            text = re.sub(rf'\b{old_price}\b', new_price, text)
            
            # Replace prices with currency symbols
            text = re.sub(rf'৳\s*{old_price}', f'৳ {new_price}', text)
            text = re.sub(rf'{old_price}\s*taka', f'{new_price} taka', text)
            text = re.sub(rf'{old_price}\s*tk', f'{new_price} tk', text)
            text = re.sub(rf'£{old_price}', f'£{new_price}', text)
            text = re.sub(rf'\${old_price}', f'${new_price}', text)
        
        return text
    
    def _replace_keywords(self, text: str) -> str:
        """Replace keywords based on rules"""
        for old_keyword, new_keyword in KEYWORD_REPLACEMENTS.items():
            # Case-insensitive replacement
            pattern = re.compile(re.escape(old_keyword), re.IGNORECASE)
            text = pattern.sub(new_keyword, text)
        
        return text
    



    def _apply_buyer_pricing_logic(self, text: str, group_settings: dict = None) -> str:
        """Apply buyer's specific pricing logic for watches vs non-watches"""
        if not text:
            return text
        
        # Use group-specific settings or defaults
        watch_keywords = group_settings.get('watch_keywords', WATCH_KEYWORDS)
        pricing_logic = group_settings.get('pricing_logic', PRICING_LOGIC)
        
        # Check if this is a watch product
        is_watch = self._is_watch_product(text, watch_keywords)
        
        # Find all price patterns in the text
        price_patterns = [
            r'£(\d+(?:\.\d{2})?)',  # £50, £99.99
            r'\$(\d+(?:\.\d{2})?)',  # $50, $99.99
            r'(\d+(?:\.\d{2})?)\s*(?:taka|tk|৳)',  # 1000 taka
            r'৳\s*(\d+(?:\.\d{2})?)',  # ৳1000
            r'(\d+(?:\.\d{2})?)\s*rs',  # 1000 rs
            r'(\d+(?:\.\d{2})?)\s*rupees?',  # 1000 rupees
            r'price[:\s]*(\d+(?:\.\d{2})?)',  # price: 1000.50
            r'cost[:\s]*(\d+(?:\.\d{2})?)',  # cost: 1000.50
        ]
        
        for pattern in price_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                original_price = float(match.group(1))
                new_price = self._calculate_new_price(original_price, is_watch, pricing_logic)
                
                # Replace the price in the text
                if '£' in match.group(0):
                    text = text.replace(match.group(0), f"£{int(new_price)}")
                elif '$' in match.group(0):
                    text = text.replace(match.group(0), f"£{int(new_price)}")
                elif '৳' in match.group(0):
                    text = text.replace(match.group(0), f"৳{int(new_price)}")
                else:
                    text = text.replace(match.group(0), f"৳{int(new_price)}")
        
        return text

    def _is_watch_product(self, text: str, watch_keywords: list = None) -> bool:
        """Check if the product is a watch based on keywords"""
        if watch_keywords is None:
            watch_keywords = WATCH_KEYWORDS
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in watch_keywords)

    def _calculate_new_price(self, original_price: float, is_watch: bool, pricing_logic: dict = None) -> float:
        """Calculate new price based on buyer's requirements"""
        if pricing_logic is None:
            pricing_logic = PRICING_LOGIC
            
        if is_watch:
            # Watch: original price + flat £105
            new_price = original_price + pricing_logic['watch_multiplier']
        else:
            # Non-watch: original price + 65% + £5
            increased_price = original_price * pricing_logic['non_watch_multiplier']
            new_price = increased_price + pricing_logic['non_watch_delivery_fee']
        
        # Round up to remove pence (e.g., £64.80 becomes £65) if enabled
        if pricing_logic.get('round_up_prices', True):
            import math
            return math.ceil(new_price)  # This properly rounds up
        else:
            return new_price

    def _append_delivery_message(self, text: str, group_settings: dict = None) -> str:
        """Append delivery message as per buyer's requirement"""
        if not text:
            return text
        
        # Use group-specific delivery message or default
        delivery_message = group_settings.get('delivery_message', DELIVERY_MESSAGE) if group_settings else DELIVERY_MESSAGE
        
        # Check if delivery message is already present
        if delivery_message.lower() not in text.lower():
            text += f"\n\n{delivery_message}"
        
        # Add contact information for orders
        text = self._append_contact_info(text)
        
        return text

    def _append_contact_info(self, text: str) -> str:
        """Append contact information for orders"""
        try:
            from config import CONTACT_INFO
            contact_info = CONTACT_INFO
        except ImportError:
            # Fallback if config not available
            contact_info = {
                'telegram_link': 'https://t.me/BFSshopuk',
                'contact_text': 'For orders message here',
                'shop_name': 'BFS',
                'auto_add_contact': True
            }
        
        if not contact_info.get('auto_add_contact', True):
            return text
        
        # Check if contact info is already present
        if contact_info['contact_text'].lower() not in text.lower():
            text += f"\n\n{contact_info['contact_text']}\n{contact_info['telegram_link']}"
        
        return text
