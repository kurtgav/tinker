import discord
from src.interfaces.base import BotInterface

class DiscordInterface(BotInterface):
    def __init__(self, agent, token: str):
        super().__init__(agent)
        self.token = token
        
        intents = discord.Intents.default()
        intents.message_content = True
        
        self.client = self._create_client(intents)

    def _create_client(self, intents):
        client = discord.Client(intents=intents)

        @client.event
        async def on_ready():
            print(f'[Discord] Logged in as {client.user} (ID: {client.user.id})')
            if self.agent:
                print('[Discord] Agent connected.')
            else:
                print('[Discord] WARNING: No agent connected.')

        @client.event
        async def on_message(message):
            if message.author == client.user:
                return

            # Check if the bot is mentioned
            if client.user in message.mentions:
                content = message.content.replace(f'<@{client.user.id}>', '').strip()
                
                if not content:
                    await message.channel.send("Hello! I am Tinker. How can I help you?")
                    return

                if not self.agent:
                    await message.channel.send("I'm having trouble initializing my brain. Please check the logs.")
                    return

                try:
                    await message.channel.send("Thinking... 🧠")
                    
                    # Fetch fetch history
                    history = []
                    async for msg in message.channel.history(limit=10):
                        if msg.id == message.id: continue # Skip current command
                        role = "assistant" if msg.author == client.user else "user"
                        history.append({"role": role, "content": msg.content})
                    
                    # History is usually newest first from Discord, dependent on API but usually iterator is newest -> oldest
                    # We want oldest -> newest for context
                    history.reverse()

                    # Offload to agent
                    response = self.agent.process_message(content, history=history, user_id=str(message.author.id))
                    
                    if len(response) > 2000:
                        # Create a temporary file
                        import io
                        file = discord.File(io.StringIO(response), filename="response.txt")
                        await message.channel.send("Response is too long, attaching as file:", file=file)
                    else:
                        await message.channel.send(response)
                except Exception as e:
                    await message.channel.send(f"Oops! I encountered an error: {e}")

        return client

    async def start(self):
        print("[Discord] Starting...")
        try:
            await self.client.start(self.token)
        except Exception as e:
            print(f"[Discord] Error starting client: {e}")

    async def stop(self):
        print("[Discord] Stopping...")
        await self.client.close()
