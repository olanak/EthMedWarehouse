import os
import logging
from datetime import datetime
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
import asyncpg  # Async PostgreSQL library
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

# Configure channels 
CHANNELS = [
    {
        "name": "DoctorsET",
        "handle": "@DoctorsET",  # Use @username instead of URL
        "active": True,
        "scrape_images": False
    },
    {
        "name": "Chemed",
        "handle": "@CheMed123",  # Replace with actual handle (e.g., @ChemedET)
        "active": True,
        "scrape_images": True  # Only scrape images here
    },
    {
        "name": "lobelia4cosmetics",
        "handle": "@lobelia4cosmetics",
        "active": True,
        "scrape_images": False
    },
    {
        "name": "yetenaweg",
        "handle": "@yetenaweg",
        "active": True,
        "scrape_images": False
    },
    {
        "name": "EAHCI",
        "handle": "@EAHCI",
        "active": True,
        "scrape_images": False
    }
]

# Configure logging
logging.basicConfig(
    filename="logs/scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
# Update save_message_to_db
async def save_message_to_db(conn, text, channel_name):
    # Replace None/empty text with a placeholder
    text = text or "No text"
    await conn.execute(
        "INSERT INTO raw_messages (channel_name, message_text) VALUES ($1, $2)",
        channel_name, text
    )
    logging.info(f"Saved message from {channel_name}")
    
async def save_image_to_db(conn, image_path, caption, channel_name):
    """Save image metadata to PostgreSQL."""
    await conn.execute(
        """INSERT INTO raw_images (channel_name, image_path, caption)
           VALUES ($1, $2, $3)""",
        channel_name, image_path, caption
    )
    logging.info(f"Saved image {image_path} from {channel_name}")

async def scrape_channel(client, conn, channel):
    try:
        # Use the @username handle instead of URL
        entity = await client.get_entity(channel["handle"])
        logging.info(f"Scraping {channel['name']} ({channel['handle']})...")

        messages = await client(GetHistoryRequest(
            peer=entity,
            limit=1000,  # Adjust based on rate limits
            offset_date=None,
            offset_id=0,
            max_id=0,
            min_id=0,
            add_offset=0,
            hash=0,
        ))

        for msg in messages.messages:
            # Extract text (handle empty values)
            text = msg.message or "No text"  # Use msg.message instead of msg.text
            await save_message_to_db(conn, text, channel["name"])

          # Download images only for Chemed
            if channel["scrape_images"] and msg.media:
                image_dir = f"data/images/{channel['name']}"
                os.makedirs(image_dir, exist_ok=True)
                image_path = f"{image_dir}/{msg.id}.jpg"
                await client.download_media(msg.media, file=image_path)
                await save_image_to_db(conn, image_path, msg.text, channel["name"])

    except Exception as e:
        logging.error(f"Error in {channel['name']}: {str(e)}")

async def main():
    # Connect to PostgreSQL
    conn = await asyncpg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )

    # Initialize Telegram client
    async with TelegramClient(
        "ethio_scraper",
        int(os.getenv("TELEGRAM_API_ID")),
        os.getenv("TELEGRAM_API_HASH")
    ) as client:
        for channel in CHANNELS:
            if channel["active"]:
                await scrape_channel(client, conn, channel)

    await conn.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())