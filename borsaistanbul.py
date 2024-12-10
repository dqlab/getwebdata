import requests
import zipfile
from io import BytesIO
import os
import pandas as pd
from datetime import datetime, timedelta

def generate_date_list(start_date_str, end_date_str):
    start_date = datetime.strptime(start_date_str, '%Y%m%d')
    end_date = datetime.strptime(end_date_str, '%Y%m%d')
    
    date_list = []
    current_date = start_date
    while current_date <= end_date:
        if current_date.weekday() < 5:  # Only weekdays
            date_list.append(current_date.strftime('%Y%m%d'))
        current_date += timedelta(days=1)
    
    return date_list

def download_and_extract_borsa_istanbul_data(date_str):
    base_url = "https://borsaistanbul.com/en/sayfa/3619/debt-securities-market-data/data/bapbultenozet"
    file_name = f"bultenozet_{date_str}.zip"
    url = f"{base_url}/{file_name}"
    
    try:
        print(f"Downloading {file_name}...")
        response = requests.get(url, timeout=30)
        
        if response.status_code == 404:
            print(f"File {file_name} does not exist. Skipping.")
            return None
        
        response.raise_for_status()
        
        output_dir = "borsa_istanbul_data"
        os.makedirs(output_dir, exist_ok=True)
        
        with zipfile.ZipFile(BytesIO(response.content)) as zip_ref:
            zip_ref.extractall(output_dir)
        
        print(f"Successfully downloaded and extracted to {output_dir}/")
        return output_dir
        
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")
        return None
    except zipfile.BadZipFile:
        print("Error: Downloaded file is not a valid zip file")
        return None

def combine_csv_files(directory):
    csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]
    combined_df = pd.concat([pd.read_csv(os.path.join(directory, f)) for f in csv_files])
    combined_file_path = os.path.join(directory, 'combined_data.csv')
    combined_df.to_csv(combined_file_path, index=False)
    print(f"Combined CSV saved to {combined_file_path}")

if __name__ == "__main__":
    start_date = "20231201"  # Format: YYYYMMDD
    end_date = "20231215"    # Format: YYYYMMDD
    
    dates = generate_date_list(start_date, end_date)
    print(f"Downloading data for dates: {dates}")
    
    for date_str in dates:
        download_and_extract_borsa_istanbul_data(date_str)
    
    combine_csv_files("borsa_istanbul_data")
