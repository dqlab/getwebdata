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

if __name__ == "__main__":
    # Example usage: download today's data
    # download_borsa_istanbul_data()
    
    # Or download data for a specific date
    specific_date = datetime(2024, 12, 4)
    download_borsa_istanbul_data(specific_date)