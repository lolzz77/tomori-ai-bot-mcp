# server.py
import os
import httpx
from fastmcp import FastMCP

# Initialize the FastMCP app
mcp = FastMCP("Discord Poster Tools")

WEBHOOK_URL = os.environ.get(
    "DISCORD_WEBHOOK_URL", 
)

@mcp.tool()
async def post_to_discord(message: str = "Hello World!") -> str:
    """
    Sends a text message directly into a specific Discord server channel.
    Use this whenever the user explicitly requests to send alerts, greetings, or text updates to Discord.
    """

    payload = {
        "content": message,
        "username": "Tomori's Drone",
        "avatar_url": "https://imgur.com"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(WEBHOOK_URL, json=payload)
            if response.status_code in [200, 204]:
                return f"✅ Successfully posted message to Discord channel: '{message}'"
            else:
                return f"❌ Failed to post. Discord API returned status: {response.status_code}"
        except Exception as e:
            return f"❌ An error occurred connecting to Discord: {str(e)}"

# --- THIS IS THE CORRECT PORTION FOR UVICORN + FASTMCP ---
if __name__ == "__main__":
    import uvicorn
    
    port = int(os.environ.get("PORT", 8000))
    
    # FastMCP uses .http_app() to expose the underlying ASGI framework wrapper
    app = mcp.http_app() 
    uvicorn.run(app, host="0.0.0.0", port=port)
