import os

# Save the downloads
download_dir = os.path.join(os.getcwd(), "downloads")
os.makedirs(download_dir, exist_ok=True)

# Save the cleaned files
cleaned_dir = os.path.join(os.getcwd(), "cleaned")
os.makedirs(cleaned_dir, exist_ok=True)

import asyncio
from playwright.async_api import async_playwright

async def download_google_trends_data():
    print("Starting Google Trends data download...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(accept_downloads=True)

        page = await context.new_page()
        url = (
            "https://trends.google.com/trends/explore?geo=IN&q=office%20chair&hl=en-GB"
        )

        max_retries = int(os.getenv("MAX_RETRIES", 5))
        for attempt in range(max_retries):
            await asyncio.sleep(5)
            response = await page.goto(url)
            if response.status == 429:
                print(f"Retry {attempt + 1}/{max_retries} - Received 429 status code")
                await asyncio.sleep(
                    5 + 2**attempt
                )
                continue
            elif response.status != 200:
                print(f"Error: Failed to load page (status {response.status})")
                await browser.close()
                return
            print("Page loaded successfully")
            break
        await page.wait_for_load_state("networkidle", timeout=60000)
        await page.wait_for_selector("button.export", state="visible", timeout=20000)

        download_buttons = await page.query_selector_all("button.export")
        download_buttons = [
            button for button in download_buttons if await button.is_visible()
        ]

        if len(download_buttons) < 4:
            print(
                f"Expected 4 download buttons, but found {len(download_buttons)}. Please check if all buttons are loaded properly."
            )
            await browser.close()
            return
        file_names = [
            "Interest_Over_Time.csv",
            "Interest_By_SubRegion.csv",
            "Related_Topics.csv",
            "Related_Queries.csv",
        ]

        for idx, button in enumerate(download_buttons[:4]):
            print(f"Downloading: {file_names[idx]}")
            await button.scroll_into_view_if_needed()
            async with page.expect_download() as download_info:
                await button.click()
            download = await download_info.value
            file_name = file_names[idx]
            await download.save_as(os.path.join(download_dir, file_name))
            print(f"Downloaded {file_name}")
        await browser.close()
        print("All files downloaded successfully")
import http.client

conn = http.client.HTTPSConnection("api.scrapingant.com")

conn.request("GET", "/v2/general?url=https%3A%2F%2Fexample.com&x-api-key=60c5558ddac64f19bd8bb2124556f078&proxy_country=US")

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))


import pandas as pd
import csv

def clean_related_data(file_path, output_top_path, output_rising_path, columns):
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        return
    print(f"Cleaning {os.path.basename(file_path)}...")
    with open(file_path, "r", encoding="utf-8-sig") as file:
        csv_reader = csv.reader(file)
        lines = []
        for line in csv_reader:
            lines.append(line)
    top_start = next(i for i, line in enumerate(lines) if line and line[0] == "TOP") + 1
    rising_start = (
        next(i for i, line in enumerate(lines) if line and line[0] == "RISING") + 1
    )

    top_data = lines[top_start : rising_start - 1]
    rising_data = lines[rising_start:]

    top_df = pd.DataFrame(top_data, columns=columns)
    rising_df = pd.DataFrame(rising_data, columns=columns)

    top_df = top_df[:-1]
    rising_df = rising_df[:-1]

    top_df.to_csv(output_top_path, index=False, encoding="utf-8-sig")
    rising_df.to_csv(output_rising_path, index=False, encoding="utf-8-sig")
    print("Cleaned data saved for TOP and RISING queries")

def clean_interest_by_subregion_data(file_path, output_path):
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        return
    print(f"Cleaning {os.path.basename(file_path)}...")
    with open(file_path, "r", encoding="utf-8-sig") as file:
        csv_reader = csv.reader(file)
        lines = []
        for line in csv_reader:
            lines.append(line)
    region_data = pd.DataFrame(lines[3:], columns=["Region", "Interest"])
    
    region_data = region_data[:-1]

    region_data.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"Cleaned data saved: {output_path}")

def clean_interest_over_time_data(file_path, output_path):
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        return
    print(f"Cleaning data from: {file_path}")
    df = pd.read_csv(file_path, skiprows=2)

    if df.shape[1] >= 2:
        if df.shape[1] != 2:
            print(f"Warning: Found {df.shape[1]} columns, using first two")
        cleaned_df = df.iloc[:, [0, 1]]
        cleaned_df.columns = ["Week", "Search Interest"]

        # Remove last row from cleaned_df

        cleaned_df = cleaned_df[:-1]

        cleaned_df.to_csv(output_path, index=False, encoding="utf-8-sig")
        print(f"Cleaned data saved: {os.path.basename(output_path)}")
    else:
        print("Error: File has unexpected number of columns")

if __name__ == "__main__":
    asyncio.run(download_google_trends_data())

    clean_related_data(
        os.path.join(download_dir, "Related_Topics.csv"),
        os.path.join(cleaned_dir, "cleaned_top_topics.csv"),
        os.path.join(cleaned_dir, "cleaned_rising_topics.csv"),
        ["Topics", "Interest"],
    )

    clean_related_data(
        os.path.join(download_dir, "Related_Queries.csv"),
        os.path.join(cleaned_dir, "cleaned_top_queries.csv"),
        os.path.join(cleaned_dir, "cleaned_rising_queries.csv"),
        ["Query", "Interest"],
    )

    clean_interest_by_subregion_data(
        os.path.join(download_dir, "Interest_By_SubRegion.csv"),
        os.path.join(cleaned_dir, "cleaned_region_data.csv"),
    )

    clean_interest_over_time_data(
        os.path.join(download_dir, "Interest_Over_Time.csv"),
        os.path.join(cleaned_dir, "cleaned_interest_over_time.csv"),
    )

    print("Data download and cleaning completed!")

from selenium import webdriver

# Initialize the browser driver
driver = webdriver.Chrome()

# Open the webpage
driver.get("http://www.example.com")

# Retrieve browser cookies
cookies = driver.get_cookies()

# Print the cookies
for cookie in cookies:
    print(cookie)

# Close the browser
driver.quit()
