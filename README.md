# Ethiopian Medical Data Warehouse

A scalable data pipeline to scrape, clean, and analyze Ethiopian medical business data from Telegram channels, integrated with object detection (YOLO) and FastAPI.

---

## 📂 Repository Structure
.
├── scripts/
│ ├── scraper.py # Telegram scraper script
│── data/images/ # Downloaded images (Chemed channel)
├── data_cleaning/
│ ├── medical_warehouse/ # DBT project
│ │ ├── models/
│ │ │ └── staging/ # SQL models (stg_messages, stg_images)
│ │ ├── dbt_project.yml # DBT config
│ │ └── profiles.yml # PostgreSQL connection
│── requirements.txt # DBT and dependencies
├── .env # Environment variables (API keys, DB credentials)
├── logs/scraper.log # Logs from scraping
└── README.md # Project documentation
