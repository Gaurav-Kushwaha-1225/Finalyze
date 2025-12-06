# read json and download all annual reports via links no fails shoulf be there
import json
import requests
import os
from pathlib import Path
from tqdm import tqdm

def download_annual_reports(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    for company, info in tqdm(data.items(), desc="Downloading reports"):
        url = info.get("url")
        if url:
            response = requests.get(url)
            if response.status_code == 200:
                file_path = Path(f"{company.replace(' ', '_')}.pdf")
                with open(file_path, 'wb') as report_file:
                    report_file.write(response.content)
            else:
                print(f"Failed to download report for {company}")

            print(f"No URL found for {company}")    

if __name__ == "__main__":
    json_file = 'data.json'  # Example JSON file
    download_annual_reports(json_file)