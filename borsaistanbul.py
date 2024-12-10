# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 23:46:45 2024

@author: dzhu
"""
import requests
import zipfile
from io import BytesIO
from datetime import datetime
import os

def download_borsa_istanbul_data(date=None):
    # If no date provided, use current date
    if date is None:
        date = datetime.now()
    
    # Format date as YYYYMMDD
    date_str = date.strftime('%Y%m%d')
    
    # Construct the URL
    base_url = "https://borsaistanbul.com/data/bapbultenozet"#"https://borsaistanbul.com/en/sayfa/3619/debt-securities-market-data/data/bapbultenozet"
    file_name = f"bultenozet_{date_str}.zip"
    url = f"{base_url}/{file_name}"
    
    try:
        # Send GET request to download the file
        print(f"Downloading {file_name}...")
        response = requests.get(url, timeout=30)
        
        # Raise an exception for bad status codes
        response.raise_for_status()
        
        # Create output directory if it doesn't exist
        output_dir = "borsa_istanbul_data"
        os.makedirs(output_dir, exist_ok=True)
        
        # Extract the zip file
        with zipfile.ZipFile(BytesIO(response.content)) as zip_ref:
            zip_ref.extractall(output_dir)
            
        print(f"Successfully downloaded and extracted to {output_dir}/")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")
        return False
    except zipfile.BadZipFile:
        print("Error: Downloaded file is not a valid zip file")
        return False

def combine_csv_files(directory):
    csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]
    combined_df = pd.concat([pd.read_csv(os.path.join(directory, f)) for f in csv_files])
    combined_file_path = os.path.join(directory, 'combined_data.csv')
    combined_df.to_csv(combined_file_path, index=False)
    print(f"Combined CSV saved to {combined_file_path}")

if __name__ == "__main__":
    dates = ["20241205", "20241206", "20241207"]  # Add your list of dates here
    for date_str in dates:
        download_and_extract_borsa_istanbul_data(date_str)
    
    combine_csv_files("borsa_istanbul_data")
