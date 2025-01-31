# Example using asyncpg (install with !pip install asyncpg)
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

async def check_cleaned_data():
    conn = await asyncpg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )
    
    # Check first 5 cleaned messages
    messages = await conn.fetch("SELECT * FROM stg_messages LIMIT 5")
    print("Cleaned Messages Sample:")
    for msg in messages:
        print(msg['cleaned_text'][:50], "...")
    
    # Check valid images
    images = await conn.fetch("SELECT valid_image_path FROM stg_images WHERE valid_image_path IS NOT NULL LIMIT 5")
    print("\nValid Images Sample:")
    for img in images:
        print(img['valid_image_path'])
    
    await conn.close()

# Run the check
import asyncio
asyncio.run(check_cleaned_data())