import pandas as pd
import json
import requests
import gspread
from pymongo import MongoClient
from datetime import datetime
from config.db_config import DB_CONFIG
from load_to_db import load_to_postgresql

# === [1] Extract: Google Sheets ===
def extract_google_sheets():
    gc = gspread.service_account(filename=DB_CONFIG["google_creds_path"])
    sh = gc.open_by_url(DB_CONFIG["google_sheet_url"])
    ws = sh.sheet1
    return pd.DataFrame(ws.get_all_records())

# === [2] Extract: CSV File ===
def extract_csv():
    return pd.read_csv(DB_CONFIG["csv_file_path"])

# === [3] Extract: JSON File ===
def extract_json():
    with open(DB_CONFIG["json_file_path"]) as f:
        return pd.DataFrame(json.load(f))

# === [4] Extract: API Data ===
def extract_api():
    url = DB_CONFIG["api_url"]
    response = requests.get(url)
    api_records = response.json().get("results", [])
    return pd.DataFrame(api_records)

# === [5] Extract: MongoDB ===
def extract_mongo():
    client = MongoClient(DB_CONFIG["mongodb_url"])
    db = client[DB_CONFIG["mongodb_db"]]
    collection = db[DB_CONFIG["mongodb_collection"]]
    mongo_data = pd.DataFrame(list(collection.find()))
    mongo_data.drop(columns=["_id"], inplace=True, errors="ignore")
    return mongo_data

# === Common Cleaning Steps ===
def standardize_columns(df):
    df.columns = df.columns.astype(str).str.lower().str.replace(" ", "_")
    return df

def clean_data(df):
    df.replace("", pd.NA, inplace=True)
    df.ffill(inplace=True)
    df.drop_duplicates(inplace=True)
    return df

def format_dates(df, date_columns):
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce').dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    return df

def validate_data(df, numeric_cols):
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            df = df[df[col].isna() | (df[col] >= 0)]
    return df

def aggregate_data(df):
    required_columns = ["date", "location_key", "new_confirmed", "new_deceased", "new_recovered", "new_tested", 
                        "cumulative_confirmed", "cumulative_deceased", "cumulative_recovered", "cumulative_tested"]
    
    if all(col in df.columns for col in required_columns):
        return df.groupby(["date", "location_key"]).agg({
            "new_confirmed": "sum",
            "new_deceased": "sum",
            "new_recovered": "sum",
            "new_tested": "sum",
            "cumulative_confirmed": "max",
            "cumulative_deceased": "max",
            "cumulative_recovered": "max",
            "cumulative_tested": "max"
        }).reset_index()
    else:
        print("Missing columns for aggregation:", [col for col in required_columns if col not in df.columns])
        return df

# Main ETL function
def etl_pipeline():
    # Extract data from different sources
    google_data = extract_google_sheets()
    csv_data = extract_csv()
    json_data = extract_json()
    api_data = extract_api()
    mongo_data = extract_mongo()

    all_dataframes = [google_data, csv_data, json_data, api_data, mongo_data]
    cleaned_dfs = []

    numeric_cols = [
        "new_confirmed", "new_deceased", "new_recovered", "new_tested",
        "cumulative_confirmed", "cumulative_deceased", "cumulative_recovered", "cumulative_tested"
    ]

    for df in all_dataframes:
        df = standardize_columns(df)
        df = clean_data(df)
        df = format_dates(df, ["date", "collection_date", "submission_date", "created", "updated"])
        df = validate_data(df, numeric_cols)
        df = aggregate_data(df)
        cleaned_dfs.append(df)

    cleaned_dfs = [df for df in cleaned_dfs if not df.empty]
    if cleaned_dfs:
        final_df = pd.concat(cleaned_dfs, ignore_index=True, sort=False)
        final_df.to_csv(DB_CONFIG["output_csv_path"], index=False)
        print("✅ All sources cleaned and merged into final_cleaned_data.csv")
