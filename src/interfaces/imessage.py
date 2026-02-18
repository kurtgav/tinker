import os
import sqlite3
import asyncio
import subprocess
from src.interfaces.base import BotInterface

DB_PATH = os.path.expanduser("~/Library/Messages/chat.db")

class IMessageInterface(BotInterface):
    def __init__(self, agent):
        super().__init__(agent)
        self.running = False
        self.last_message_id = self._get_last_message_id()

    def _get_last_message_id(self):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT MAX(ROWID) FROM message")
            result = cursor.fetchone()
            conn.close()
            return result[0] if result and result[0] else 0
        except sqlite3.OperationalError:
            print("[iMessage] Error access chat.db. Ensure Full Disk Access is granted to your terminal/IDE.")
            return 0
        except Exception as e:
            print(f"[iMessage] Error reading last message ID: {e}")
            return 0

    async def start(self):
        self.running = True
        print("[iMessage] Starting polling loop...")
        print(f"[iMessage] Initial last_message_id: {self.last_message_id}")
        
        while self.running:
            try:
                await self._poll()
            except Exception as e:
                print(f"[iMessage] Error in poll loop: {e}")
            await asyncio.sleep(2)  # Poll every 2 seconds

    async def stop(self):
        print("[iMessage] Stopping...")
        self.running = False

    async def _poll(self):
        try:
            conn = sqlite3.connect(DB_PATH)
            # Row factory to access columns by name if needed, but simple tuple is fine for now
            cursor = conn.cursor()
            
            # Fetch new messages since last_message_id
            # text NOT NULL ensuring it's a text message
            query = """
                SELECT message.ROWID, message.text, handle.id
                FROM message
                JOIN handle ON message.handle_id = handle.ROWID
                WHERE message.ROWID > ? AND message.text IS NOT NULL AND message.is_from_me = 0
                ORDER BY message.ROWID ASC
            """
            
            cursor.execute(query, (self.last_message_id,))
            rows = cursor.fetchall()
            conn.close()

            for row in rows:
                msg_id, text, sender = row
                self.last_message_id = msg_id
                
                # Check for trigger
                if "@Tinker" in text or "@tinker" in text:
                    print(f"[iMessage] Received from {sender}: {text}")
                    await self._process_message(text, sender)

        except sqlite3.OperationalError:
            print("[iMessage] Permission denied. Please grant Full Disk Access.")
            self.running = False # Stop to avoid spamming logs
        except Exception as e:
            print(f"[iMessage] Polling error: {e}")

    async def _process_message(self, text: str, sender: str):
        # Notify
        await self._send_reply(sender, "Thinking... 🧠")
        
        # Clean text
        clean_text = text.replace("@Tinker", "").replace("@tinker", "").strip()
        
        if not clean_text:
            await self._send_reply(sender, "Hello! I am Tinker. How can I help you?")
            return

        try:
            # Agent processing
            # For iMessage, history fetching is efficiently hard without more complex SQL queries
            # For now, we will pass empty history, but we MUST pass the sender as user_id for Long-term memory
            response = self.agent.process_message(clean_text, history=[], user_id=sender)
            await self._send_reply(sender, response)
        except Exception as e:
            await self._send_reply(sender, f"Oops! Error: {e}")

    async def _send_reply(self, recipient: str, message: str):
        # Use osascript to send iMessage
        # Note: escaping quotes is important
        safe_message = message.replace('"', '\\"')
        
        script = f'''
        tell application "Messages"
            set targetService to 1st service whose service type = iMessage
            set targetBuddy to buddy "{recipient}" of targetService
            send "{safe_message}" to targetBuddy
        end tell
        '''
        
        try:
            # run osascript
            proc = await asyncio.create_subprocess_exec(
                'osascript', '-e', script,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = await proc.communicate()
            
            if proc.returncode != 0:
                print(f"[iMessage] Error sending reply: {stderr.decode()}")
            else:
                print(f"[iMessage] Sent reply to {recipient}")
        except Exception as e:
            print(f"[iMessage] Failed to execute osascript: {e}")
