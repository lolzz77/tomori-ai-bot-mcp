# server.py
import os
import httpx
from dotenv import load_dotenv
from urllib.parse import quote
from fastmcp import FastMCP
from module import utils

# Initialize the FastMCP app
mcp = FastMCP("Discord Poster Tools")

load_dotenv()
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
BOT_TOKEN = os.getenv('BOT_TOKEN')


@mcp.tool()
async def send_template_message(template_message: str) -> str:
    """
    Sends a text template to Discord through a webhook.
    Saves the sent message ID and channel ID to a local JSON file.

    Args:
        template_message: The complete Discord message content as a string.
    """
    import httpx

    if not isinstance(template_message, str):
        return (
            "Error: template_message must be a string. "
            f"Received type: {type(template_message).__name__}"
        )

    payload = {
        "content": template_message,
        "username": "Tomori's Drone",
        "avatar_url": "https://imgur.com",
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(
                WEBHOOK_URL,
                params={"wait": "true"},
                json=payload,
            )

            if response.status_code in (200, 201):
                data = response.json()

                message_id = data["id"]
                channel_id = data["channel_id"]

                file_path = utils.check_json_exists()
                json_data = utils.read_file(file_path)

                json_data["sent_template_message_id"] = message_id
                json_data["sent_template_channel_id"] = channel_id

                utils.write_file(json_data, file_path)

                return (
                    "Message sent successfully!\n"
                    f"Message ID: {message_id}\n"
                    f"Channel ID: {channel_id}"
                )

            return (
                f"Discord HTTP {response.status_code}: "
                f"{response.text}"
            )

        except Exception as e:
            return f"Error ({type(e).__name__}): {e}"


@mcp.tool()
async def react_emoji(emoji_to_react_message) -> str:
    """
    Gets the sent template message IDs from the JSON file,
    then adds a list of emojis defined by the user.

    Example input:
        ["👍", "❤️", "🎉"]
    """
    try:
        file_path = utils.check_json_exists()
        json_data = utils.read_file(file_path)

        # Get IDs saved by send_template_message()
        sent_template_message_id = json_data["sent_template_message_id"]
        sent_template_channel_id = json_data["sent_template_channel_id"]

        headers = {
            "Authorization": f"Bot {BOT_TOKEN}"
        }

        results = []

        async with httpx.AsyncClient() as client:
            for emoji in emoji_to_react_message:
                encoded_emoji = quote(emoji, safe="")

                url = (
                    f"https://discord.com/api/v10/channels/"
                    f"{sent_template_channel_id}/messages/"
                    f"{sent_template_message_id}/reactions/"
                    f"{encoded_emoji}/@me"
                )

                response = await client.put(url, headers=headers)

                if response.status_code == 204:
                    results.append(f"✅ Added {emoji}")
                else:
                    results.append(
                        f"❌ Failed {emoji}: "
                        f"{response.status_code} - {response.text}"
                    )

        return "\n".join(results)

    except KeyError as e:
        return f"❌ Missing message ID or channel ID in JSON file: {e}"
    except Exception as e:
        return f"❌ Error adding reactions: {str(e)}"


# --- THIS IS THE CORRECT PORTION FOR UVICORN + FASTMCP ---
if __name__ == "__main__":
    import uvicorn
    
    port = int(os.environ.get("PORT", 8000))
    
    # FastMCP uses .http_app() to expose the underlying ASGI framework wrapper
    app = mcp.http_app() 
    uvicorn.run(app, host="0.0.0.0", port=port)
