#🧪 ETL Pipeline – Ganesha Maheshwari
This project is an end-to-end ETL pipeline built using Python. It extracts data from five different sources (CSV, Google Sheets, JSON file, Public API, and MongoDB), performs cleaning, transformation, feature engineering, aggregation, and finally uploads the processed data into a PostgreSQL database hosted on Supabase.
ETL_Pipeline_GaneshaMaheshwari_22010221062/
├── etl_pipeline.py              # ETL main script
├── config/
│   └── credentials.json         # Google Sheets service account credentials
│   └── db_config.json           # Dummy config for Supabase (optional)
├── data/
│   ├── sample_data.csv          # Example CSV dataset (epidemiology.csv)
│   ├── sample_weather.json      # JSON dataset
│   └── google_sheet_sample.csv  # Exported version of Google Sheets (optional)
├── scheduler.py                 # Automates the ETL using schedule module
├── requirements.txt             # Python package dependencies
├── README.md                    # This documentation file
├── output/
│   └── final_cleaned_data.csv   # Final cleaned data stored locally
├── load_to_db.py                # Script to upload DataFrame to PostgreSQL (Supabase)
├── .github/
│   └── workflows/
│       └── ci_cd.yml            # GitHub Actions CI/CD for automation (optional)
└── report.pdf                   # PDF report detailing steps, results, and insights


#🚀 ETL Workflow
✅ 1. Extract
📄 CSV: epidemiology.csv

📊 Google Sheets: Imported using GSpread and credentials.json

🧾 JSON File: data.json

🌐 API: COVID-19 sequences from covid19dataportal.org

🍃 MongoDB: Remote collection from MongoDB Atlas

🔧 2. Transform
Column standardization (lowercase, underscore)

Handling missing values using forward-fill

Date formatting to ISO format

Type validation (numeric fields)

Feature engineering:

COVID Impact Score

Days since collection

Sequence length

Aggregation based on date and location_key

📤 3. Load
Final cleaned dataset is stored as CSV

Additionally, uploaded to a PostgreSQL database on Supabase using SQLAlchemy

#🛠️ Setup Instructions
#🔗 Clone the repository

git clone https://github.com/<your-username>/ETL_Pipeline_GaneshaMaheshwari_22010221062.git
cd ETL_Pipeline_GaneshaMaheshwari_22010221062

git clone https://github.com/<your-username>/ETL_Pipeline_GaneshaMaheshwari.git
cd ETL_Pipeline_GaneshaMaheshwari

#📦 Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
#🔑 Setup Google Sheets access
Place your credentials.json in the config/ directory.

Share your Google Sheet with the service account email.

#🗄️ MongoDB
Make sure your MongoDB Atlas cluster is accessible and the credentials in etl_pipeline.py are valid.

#🧪 Running the ETL Pipeline
bash
Copy
Edit
python etl_pipeline.py
This will:

Extract data from all sources

Clean and transform the data

Save the result to output/final_cleaned_data.csv

#🧬 Uploading to PostgreSQL (Supabase)
To upload your CSV or DataFrame directly to Supabase:

bash
Copy
Edit
python load_to_db.py
Make sure your DB credentials and sqlalchemy connection string are correct in load_to_db.py.

#⏰ Automate with Scheduler
bash
Copy
Edit
python scheduler.py
This script uses the schedule module to run your ETL at regular intervals (e.g., daily).

📋 Dependencies
pandas

sqlalchemy

psycopg2-binary

gspread

requests

pymongo

schedule

(Full list in requirements.txt)

#📄 License
This project is developed for academic purposes and is open for reuse or extension with credit.

✨ Acknowledgements
Supabase

Google Sheets API

MongoDB Atlas

COVID-19 Data Portal
