import discord
import os
import asyncio
import subprocess

# Load env
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
IMAGE_PATH = os.path.abspath("src/Tinker-logo.png")

async def update_discord():
    print(f"[Discord] Updating avatar from {IMAGE_PATH}...")
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f"[Discord] Logged in as {client.user}")
        try:
            with open(IMAGE_PATH, 'rb') as f:
                avatar_bytes = f.read()
            await client.user.edit(avatar=avatar_bytes)
            print("[Discord] Avatar updated successfully!")
        except Exception as e:
            print(f"[Discord] Error updating avatar: {e}")
        finally:
            await client.close()

    await client.start(TOKEN)

def update_imessage_contact():
    print(f"[iMessage] Attempting to set Contact image for 'Tinker'...")
    # AppleScript to set image for contact named "Tinker" or "Self"
    # Note: access to Contacts requires permission
    
    script = f'''
    tell application "Contacts"
        try
            set image of person "Tinker" to read (POSIX file "{IMAGE_PATH}")
            return "Success"
        on error
            return "Contact 'Tinker' not found or permission denied"
        end try
    end tell
    '''
    
    try:
        proc = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
        if "Success" in proc.stdout:
            print("[iMessage] Contact 'Tinker' image updated.")
        else:
            print(f"[iMessage] Could not update contact: {proc.stdout.strip()}")
            print("To fix: Create a contact named 'Tinker' in your Mac Contacts app and add the email/phone you use for the bot.")
    except Exception as e:
        print(f"[iMessage] Error running AppleScript: {e}")

async def main():
    if TOKEN:
        await update_discord()
    else:
        print("[Discord] No token found.")
    
    # Check if on Mac
    if os.uname().sysname == "Darwin":
        update_imessage_contact()

if __name__ == "__main__":
    asyncio.run(main())
