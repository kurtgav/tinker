from abc import ABC, abstractmethod
import asyncio

class BotInterface(ABC):
    """Abstract base class for all bot interfaces (Discord, iMessage, CLI, etc.)"""
    
    def __init__(self, agent):
        self.agent = agent

    @abstractmethod
    async def start(self):
        """Start the interface (connect, listen, loop)."""
        pass

    @abstractmethod
    async def stop(self):
        """Stop the interface and cleanup."""
        pass
