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
     ```
```bash
# For scraping and cleaning
pip install -r data_scraping/requirements.txt

# For object detection
pip install -r object_detection/requirements.txt

# For FastAPI
pip install -r api/requirements.txt
```
