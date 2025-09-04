import asyncio
import logging
from telethon import TelegramClient, events
from telethon.tl.types import Message, InputMediaPhoto
from config import (
    API_ID, 
    API_HASH, 
    PHONE, 
    SOURCE_GROUP_IDS, 
    TARGET_GROUP_ID, 
    MESSAGE_DELAY,
    SOURCE_GROUP_SETTINGS,
    MULTI_SOURCE_MONITORING
)
from message_processor import MessageProcessor


# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class MessageForwarderBot:
    """Telethon-based bot that forwards messages with modifications"""
    
    def __init__(self):
        self.processor = MessageProcessor()
        self.client = None
    
    async def start(self):
        """Start the bot"""
        try:
            # Create Telethon client
            self.client = TelegramClient('session_name', API_ID, API_HASH)
            
            # Start the client
            await self.client.start(phone=PHONE)
            logger.info("Bot started successfully!")
            
            # Add event handlers for multiple source groups
            if MULTI_SOURCE_MONITORING:
                logger.info(f"Multi-source monitoring enabled for {len(SOURCE_GROUP_IDS)} groups")
                for group_id in SOURCE_GROUP_IDS:
                    group_name = SOURCE_GROUP_SETTINGS[group_id]['name']
                    logger.info(f"Setting up listener for: {group_name} ({group_id})")
                    
                    # Create a closure to capture the current group_id
                    async def create_handler(current_group_id):
                        @self.client.on(events.NewMessage(chats=current_group_id))
                        async def handle_new_message(event):
                            await self.handle_source_message(event.message, current_group_id)
                    
                    await create_handler(group_id)
            else:
                # Single source group (backward compatibility)
                group_id = SOURCE_GROUP_IDS[0]
                logger.info(f"Single source monitoring for group: {group_id}")
                
                @self.client.on(events.NewMessage(chats=group_id))
                async def handle_new_message(event):
                    await self.handle_source_message(event.message, group_id)
            
            logger.info("Bot is now running and listening for messages...")
            logger.info(f"Monitoring {len(SOURCE_GROUP_IDS)} source group(s)")
            logger.info(f"Forwarding to target group: {TARGET_GROUP_ID}")
            logger.info("=" * 50)
            logger.info("IMPORTANT: Bot will ONLY forward to this target group!")
            logger.info("=" * 50)
            
            # FINAL VERIFICATION: Ensure only one target group
            if TARGET_GROUP_ID == 0:
                logger.error("CRITICAL ERROR: TARGET_GROUP_ID is 0!")
                logger.error("Please check your .env file and restart the bot")
                return
            else:
                logger.info(f"✅ VERIFIED: Bot will forward ONLY to {TARGET_GROUP_ID}")
            
            # Keep the bot running
            await self.client.run_until_disconnected()
            
        except Exception as e:
            logger.error(f"Failed to start bot: {e}")
            raise
    
    async def handle_source_message(self, message: Message, source_group_id: int):
        """Handle incoming messages from source group"""
        try:
            # Skip bot messages and service messages
            if message.from_id and hasattr(message.from_id, 'user_id'):
                if message.from_id.user_id == (await self.client.get_me()).id:
                    return  # Skip own messages
            
            group_name = SOURCE_GROUP_SETTINGS[source_group_id]['name']
            logger.info(
                f"New message from {message.sender_id} "
                f"in {group_name} ({source_group_id}): {message.id}"
            )
            
            # Process the message with group-specific settings
            # Use message.media for proper album detection
            processed_content = self.processor.process_message({
                'text': message.text,
                'media': message.media,  # This handles albums properly
                'photo': message.photo,
                'video': message.video,
                'document': message.document,
                'audio': message.audio,
                'caption': message.message
            }, source_group_id)
            
            # Forward to target group with modifications
            await self.forward_to_target(processed_content, source_group_id)
            
        except Exception as e:
            logger.error(f"Error handling source message: {e}")
    
    async def forward_to_target(self, content: dict, source_group_id: int):
        """Forward processed content to target group"""
        try:
            # STRICT CHECK: Only forward to the configured target group
            if TARGET_GROUP_ID == 0:
                logger.error("TARGET_GROUP_ID is 0! Check your .env file")
                return
            
            logger.info(f"STRICT: Forwarding ONLY to target group {TARGET_GROUP_ID}")
            
            # Add delay to avoid spam (prefer group-specific delay)
            try:
                from config import SOURCE_GROUP_SETTINGS  # lazy import
                group_delay = SOURCE_GROUP_SETTINGS.get(
                    source_group_id, {}
                ).get('message_delay', MESSAGE_DELAY)
            except Exception:
                group_delay = MESSAGE_DELAY
            await asyncio.sleep(group_delay)
            
            if content['media'] and content['media_type']:
                # Send media with caption
                caption = content['caption'] or content['text']
                
                # Log the target group ID for debugging
                logger.info(f"Sending media to target group: {TARGET_GROUP_ID}")
                
                if content['media_type'] == 'photo':
                    # Handle multiple photos - send as album if multiple
                    if len(content['media']) > 1:
                        # Send multiple photos as album with caption
                        try:
                            # Create media group with InputMediaPhoto for proper album
                            media_group = []
                            for photo in content['media']:
                                # ALL photos get the same caption
                                media_group.append(InputMediaPhoto(photo, caption=caption))
                            
                            await self.client.send_media_group(
                                TARGET_GROUP_ID,
                                media_group
                            )
                            logger.info(f"Sent {len(content['media'])} photos as ALBUM to target group {TARGET_GROUP_ID}")
                        except Exception as e:
                            logger.error(f"Failed to send album: {e}")
                            # Fallback: send first photo with caption, then others without
                            await self.client.send_file(
                                TARGET_GROUP_ID,
                                content['media'][0],
                                caption=caption
                            )
                            # Send remaining photos without caption
                            for photo in content['media'][1:]:
                                await self.client.send_file(
                                    TARGET_GROUP_ID,
                                    photo
                                )
                            logger.info(f"Sent {len(content['media'])} photos with fallback method")
                    else:
                        await self.client.send_file(
                            TARGET_GROUP_ID,
                            content['media'][0],
                            caption=caption
                        )
                        logger.info(f"Sent 1 photo to target group {TARGET_GROUP_ID}")
                elif content['media_type'] == 'video':
                    if len(content['media']) > 1:
                        # Send multiple videos as album
                        try:
                            # Create media group with InputMediaPhoto for proper album
                            media_group = []
                            for video in content['media']:
                                # ALL videos get the same caption
                                media_group.append(InputMediaPhoto(video, caption=caption))
                            
                            await self.client.send_media_group(
                                TARGET_GROUP_ID,
                                media_group
                            )
                            logger.info(f"Sent {len(content['media'])} videos as ALBUM to target group {TARGET_GROUP_ID}")
                        except Exception as e:
                            logger.error(f"Failed to send video album: {e}")
                            # Fallback: send first video with caption, then others without
                            await self.client.send_file(
                                TARGET_GROUP_ID,
                                content['media'][0],
                                caption=caption
                            )
                            # Send remaining videos without caption
                            for video in content['media'][1:]:
                                await self.client.send_file(TARGET_GROUP_ID, video)
                    else:
                        await self.client.send_file(
                            TARGET_GROUP_ID,
                            content['media'][0],
                            caption=caption
                        )
                        logger.info(f"Sent 1 video to target group {TARGET_GROUP_ID}")
                elif content['media_type'] == 'document':
                    if len(content['media']) > 1:
                        await self.client.send_file(
                            TARGET_GROUP_ID,
                            content['media'],
                            caption=caption
                        )
                        logger.info(f"Sent {len(content['media'])} documents to target group {TARGET_GROUP_ID}")
                    else:
                        await self.client.send_file(
                            TARGET_GROUP_ID,
                            content['media'][0],
                            caption=caption
                        )
                        logger.info(f"Sent 1 document to target group {TARGET_GROUP_ID}")
                elif content['media_type'] == 'audio':
                    if len(content['media']) > 1:
                        await self.client.send_file(
                            TARGET_GROUP_ID,
                            content['media'],
                            caption=caption
                        )
                        logger.info(f"Sent {len(content['media'])} audio files to target group {TARGET_GROUP_ID}")
                    else:
                        await self.client.send_file(
                            TARGET_GROUP_ID,
                            content['media'][0],
                            caption=caption
                        )
                        logger.info(f"Sent 1 audio file to target group {TARGET_GROUP_ID}")
            else:
                # Send text only
                if content['text']:
                    await self.client.send_message(
                        TARGET_GROUP_ID,
                        content['text']
                    )
                    logger.info(f"Sent text message to target group {TARGET_GROUP_ID}")
            
            logger.info(f"Message forwarded to target group {TARGET_GROUP_ID} successfully")
            
        except Exception as e:
            logger.error(f"Error forwarding to target: {e}")
    
    async def stop(self):
        """Stop the bot"""
        if self.client:
            try:
                await self.client.disconnect()
                logger.info("Bot stopped")
            except Exception as e:
                logger.error(f"Error stopping bot: {e}")


async def main():
    """Main function to run the bot"""
    bot = MessageForwarderBot()
    
    try:
        await bot.start()
    except KeyboardInterrupt:
        logger.info("Bot interrupted by user")
    except Exception as e:
        logger.error(f"Bot error: {e}")
    finally:
        try:
            await bot.stop()
        except Exception as e:
            logger.error(f"Error stopping bot: {e}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
