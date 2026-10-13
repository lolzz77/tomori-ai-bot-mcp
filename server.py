# server.py
import os
import httpx
from fastmcp import FastMCP

# Initialize the FastMCP app
mcp = FastMCP("Discord Poster Tools")

# Paste your Discord Channel Webhook URL here 
# (Or set it as an Environment Variable named DISCORD_WEBHOOK_URL on Render)
WEBHOOK_URL = os.environ.get(
    "DISCORD_WEBHOOK_URL", 
)

@mcp.tool()
async def post_to_discord(message: str = "Hello World!") -> str:
    """
    Sends a text message directly into a specific Discord server channel.
    Use this whenever the user explicitly requests to send alerts, greetings, or text updates to Discord.
    """
    if not WEBHOOK_URL or "YOUR_DISCORD_WEBHOOK" in WEBHOOK_URL:
        return "❌ Error: The Discord Webhook URL has not been configured yet."

    payload = {
        "content": message,
        "username": "Tomori's Drone",
        "avatar_url": "https://imgur.com" # Optional avatar overlay
    }

    # Send an asynchronous post payload directly to Discord's API
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(WEBHOOK_URL, json=payload)
            if response.status_code in [200, 204]:
                return f"✅ Successfully posted message to Discord channel: '{message}'"
            else:
                return f"❌ Failed to post. Discord API returned status: {response.status_code}"
        except Exception as e:
            return f"❌ An error occurred connecting to Discord: {str(e)}"

if __name__ == "__main__":
    # Dynamic routing to match Render's environment profile
    port = int(os.environ.get("PORT", 8000))
    mcp.run(transport="http", host="0.0.0.0", port=port)
