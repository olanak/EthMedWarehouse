import os
import json
import logging
import torch
from PIL import Image
import asyncpg
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/detection.log"),
        logging.StreamHandler()
    ]
)

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

async def detect_objects():
    try:
        # Connect to PostgreSQL
        conn = await asyncpg.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
        )
        logging.info("Connected to PostgreSQL")

        # Fetch Chemed images from cleaned data
        images = await conn.fetch("""
            SELECT valid_image_path FROM stg_images 
            WHERE channel_name = 'Chemed' AND valid_image_path IS NOT NULL
        """)
        logging.info(f"Found {len(images)} images to process")

        for img_record in images:
            image_path = img_record['valid_image_path']
            if not os.path.exists(image_path):
                logging.warning(f"Skipping missing image: {image_path}")
                continue

            try:
                # Open image and get dimensions
                img = Image.open(image_path)
                img_width, img_height = img.size

                # Run YOLO inference
                logging.info(f"Processing image: {image_path}")
                results = model(img)
                detections = results.pandas().xyxy[0]

                # Process each detection
                for _, det in detections.iterrows():
                    try:
                        # Extract data
                        label = det['name']
                        confidence = round(float(det['confidence']), 2)

                        # Validate and cast coordinates
                        xmin = float(det['xmin'])
                        ymin = float(det['ymin'])
                        xmax = float(det['xmax'])
                        ymax = float(det['ymax'])

                        # Validate bounding box
                        if (xmin >= xmax) or (ymin >= ymax) or (xmax > img_width) or (ymax > img_height):
                            logging.warning(f"Invalid bbox in {image_path}: [{xmin}, {ymin}, {xmax}, {ymax}]")
                            continue

                        # Serialize bounding box to JSON string
                        bounding_box = json.dumps({
                            "xmin": xmin,
                            "ymin": ymin,
                            "xmax": xmax,
                            "ymax": ymax,
                            "width": xmax - xmin,
                            "height": ymax - ymin
                        })

                        # Insert into PostgreSQL
                        await conn.execute("""
                            INSERT INTO detections (image_path, label, confidence, bounding_box)
                            VALUES ($1, $2, $3, $4)
                        """, image_path, label, confidence, bounding_box)

                    except Exception as det_error:
                        logging.error(f"Failed to process detection in {image_path}: {str(det_error)}", exc_info=True)

                logging.info(f"Processed {len(detections)} detections for {image_path}")

            except Exception as img_error:
                logging.error(f"Error processing {image_path}: {str(img_error)}", exc_info=True)

        logging.info("Detection completed successfully")

    except Exception as e:
        logging.critical(f"Fatal error: {str(e)}", exc_info=True)
    finally:
        if 'conn' in locals():
            await conn.close()

if __name__ == "__main__":
    import asyncio
    os.makedirs("logs", exist_ok=True)
    asyncio.run(detect_objects())