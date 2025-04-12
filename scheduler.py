import schedule
import time
from etl_pipeline import etl_pipeline

def job():
    print("Running ETL pipeline...")
    etl_pipeline()

# Schedule the ETL pipeline to run every day at midnight
schedule.every().day.at("02:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
