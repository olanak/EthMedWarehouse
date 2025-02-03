# Ethiopian Medical Data Warehouse

A scalable data pipeline to collect, clean, and analyze Ethiopian medical business data from Telegram channels, integrated with object detection (YOLO) and a FastAPI for data access.

---

## ✨ Features

- **Telegram Scraping**: Collect text and images from Ethiopian medical channels.
- **Data Cleaning**: Deduplicate, validate, and standardize raw data using DBT.
- **Object Detection**: Detect medical products (e.g., pills, syringes) with YOLOv5.
- **Star Schema**: Optimized data warehouse for analytics (fact/dimension tables).
- **REST API**: FastAPI endpoints to query cleaned data and detection results.

---

## 🛠️ Prerequisites

- Python 3.8+
- PostgreSQL 14+
- [Telegram API ID & Hash](https://my.telegram.org/auth)
- `DBT`, `FastAPI`, and `YOLOv5` dependencies (see installation below).

---

## 🚀 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/Ethiopian-Medical-Data-Warehouse.git
   cd Ethiopian-Medical-Data-Warehouse
   pip install -r requirements.txt
     ```
2. **Install dependencies**:
    ```bash
   pip install -r requirements.txt
     ```
3. **Setup environments**:
   Create a .env file (use .env.template).
   Add Telegram API credentials and PostgreSQL details.
   
## ⚙️ Configuration
   .env File
   
     ```bash
      TELEGRAM_API_ID=your_api_id
      TELEGRAM_API_HASH=your_api_hash
      DB_HOST=localhost
      DB_PORT=5432
      DB_NAME=ethio_medical
      DB_USER=postgres
      DB_PASSWORD=your_password
    ```
  ## Database Setup
   **Run the PostgreSQL setup scripts**:
 ```bash
        -- Create raw tables
CREATE TABLE raw_messages (...);
CREATE TABLE raw_images (...);

-- Create star schema tables
CREATE TABLE fact_medical (...);
CREATE TABLE dim_product (...);
 ```
## 🖥️ Usage
1. **Scrape Data**:
    ```bash
   python data_scraping/scraper.py
    ```
2. **Clean Data with DBT**:
    ```bash
   cd data_cleaning/medical_warehouse
   dbt run  # Transform raw data into staging tables
   dbt test  # Validate data quality
    ```
3. **Run Object Detection**:
   ```bash
   python object_detection/detect.py
   ```
4. **Start FastAPI Server**:
    ```bash
   uvicorn api.main:app --reload
      ```
## 📊 Project Structure Details

   Directory	              Purpose
data_scraping	      Scripts to scrape Telegram channels and store raw data.
data_cleaning        DBT models for data transformation and quality checks.
object_detection	   YOLOv5 scripts to detect medical products in images.
    api	            FastAPI endpoints to query cleaned data and detection results.
   docs	            Schema diagrams and project documentation.

## 📅 Roadmap
-**Real-Time Alerts**: Slack/email notifications for high-confidence detections.
-**Geospatial Analytics**: Integrate PostGIS for location-based insights.
-**User Authentication**: Add OAuth2 to FastAPI endpoints.
-**Dashboard**: Build a Power BI/Tableau dashboard for business users.

## 🤝 Contributing
1. Fork the repository.
2. Create a feature branch (git checkout -b feature/your-feature).
3. Commit changes (git commit -m 'Add your feature').
4. Push to the branch (git push origin feature/your-feature).
5. Open a Pull Request.
   
## 📜 License
This project is licensed under the Apache License 2.0.


   
