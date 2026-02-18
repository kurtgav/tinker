import os
import asyncio
import logging
from dotenv import load_dotenv
from src.agent.react_agent import ReactAgent
from src.interfaces.discord import DiscordInterface

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    # Load environment variables
    load_dotenv()
    
    # Initialize Agent
    try:
        agent = ReactAgent()
        logger.info("ReactAgent initialized.")
    except Exception as e:
        logger.error(f"Failed to initialize ReactAgent: {e}")
        return

    interfaces = []

    # Initialize Discord Interface
    discord_token = os.getenv('DISCORD_TOKEN')
    if discord_token:
        discord_bot = DiscordInterface(agent, discord_token)
        interfaces.append(discord_bot)
    else:
        logger.warning("DISCORD_TOKEN not found. Discord interface will not start.")

    # Future: Initialize iMessage Interface here
    from src.interfaces.imessage import IMessageInterface
    # Enable iMessage by default or via env
    if os.getenv('ENABLE_IMESSAGE', 'true').lower() == 'true':
        imessage_bot = IMessageInterface(agent)
        interfaces.append(imessage_bot)
    else:
        logger.info("iMessage interface disabled via env.")

    if not interfaces:
        logger.error("No interfaces enabled. Exiting.")
        return

    # Start all interfaces
    # For now, we only have Discord which is blocking-ish in its run/start method if using client.run
    # But we refactored to use client.start which is async.
    
    tasks = [interface.start() for interface in interfaces]
    
    try:
        logger.info("Starting interfaces...")
        await asyncio.gather(*tasks)
    except KeyboardInterrupt:
        logger.info("Stopping...")
    finally:
        for interface in interfaces:
            await interface.stop()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # Handle Request to Exit gracefully
        pass
