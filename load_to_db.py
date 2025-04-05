from sqlalchemy import create_engine, types
import pandas as pd
import urllib.parse

def load_to_postgresql(df):
    # URL encode the password, because it contains a special character (@)
    password = urllib.parse.quote_plus("Ganesha@0707")

    db_url = f"postgresql://postgres:{password}@db.tsrykeqtjbllyugqoppt.supabase.co:5432/assignment"
    engine = create_engine(db_url)

    try:
        # Load the DataFrame to the PostgreSQL table 'assignment'
        df.to_sql('assignment', engine, if_exists='replace', index=False, dtype={
            'date': types.Date(),
            'location_key': types.String(50),
            'new_confirmed': types.Integer(),
            'new_deceased': types.Integer(),
            'new_recovered': types.Integer(),
            'new_tested': types.Integer(),
            'cumulative_confirmed': types.Integer(),
            'cumulative_deceased': types.Integer(),
            'cumulative_recovered': types.Integer(),
            'cumulative_tested': types.Integer()
        })
        print("Data loaded successfully into PostgreSQL")
    except Exception as e:
        print(f"Error loading data into PostgreSQL: {e}")

# Step 1: Read the CSV file into a DataFrame
csv_file_path = '/content/ASSIGNMENT/output/final_cleaned_data.csv'  # Replace with the path to your CSV file
df = pd.read_csv(csv_file_path)

# Step 2: Call the function to load the DataFrame into PostgreSQL
load_to_postgresql(df)
