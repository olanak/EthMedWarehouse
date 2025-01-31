# Ethiopian Medical Data Warehouse

A scalable data pipeline to scrape, clean, and analyze Ethiopian medical business data from Telegram channels, integrated with object detection (YOLO) and FastAPI.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL 14+
- [Telegram API ID & Hash](https://my.telegram.org/auth)

### Installation
1. Clone the repo:
   ```bash
   git clone https://github.com/yourusername/Ethiopian-Medical-Data-Warehouse.git
   cd Ethiopian-Medical-Data-Warehouse
   ```
2. Install dependencies:
 ```bash
   pip install -r data_scraping/requirements.txt
   pip install -r data_cleaning/requirements.txt
 ```
3. Configure environment:
   Add Telegram API credentials and PostgreSQL details to .env:
    ```bash
    TELEGRAM_API_ID=your_api_id
    TELEGRAM_API_HASH=your_api_hash
    DB_HOST=localhost
    DB_PORT=5432
    DB_NAME=ethio_medical
    DB_USER=postgres
    DB_PASSWORD=your_password
    ```
📊 Usage
1. Data Scraping
Run the Telegram scraper:
 ```bash
python scripts/scraper.py
```
Output: Raw data in PostgreSQL tables raw_messages and raw_images.

2. Data Cleaning with DBT
  1. Navigate to the DBT project:
      ```bash
       cd data_cleaning/medical_warehouse
     ```
  2. Run transformations:
        ```bash
     dbt run  # Creates stg_messages and stg_images
     dbt test  # Validate data quality
        ```
✅ Progress (Tasks 1 & 2)
Task 1: Data Scraping
Channels Scraped: @DoctorsET, @Chemed, @lobelia4cosmetics, @yetenaweg, @EAHCI.

Images: 150+ scraped from @Chemed (stored in images/Chemed/).

Logs: Tracked errors and progress in scraper.log.

Task 2: Data Cleaning
Deduplication: Removed 50+ duplicates using message_hash.

Validation:

Non-null checks for valid_image_path.

Standardized timestamps and text fields.

Tables:

stg_messages: Cleaned messages with unique hashes.

stg_images: Validated image metadata.

🛠️ Challenges & Solutions
Null Values: Replaced empty text/captions with placeholders ("No text", "No caption").

DBT Source Errors: Fixed by defining raw_messages and raw_images in schema.yml.

Telegram Rate Limits: Added delays between requests to avoid bans.

➡️ Next Steps
Task 3: Object detection on @Chemed images using YOLOv5.

Task 4: Design star schema for analytics (fact_sales, dim_product).

Task 5: Expose data via FastAPI endpoints.

👥 Contributors
Olana Kenea

📜 License
This project is licensed under the Apache License 2.0.



      
     
