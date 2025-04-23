import os
import asyncio
import pandas as pd
import csv
from playwright.async_api import async_playwright

# Directory to save the downloads
download_dir = os.path.join(os.getcwd(), "downloads")
os.makedirs(download_dir, exist_ok=True)

# Directory to save the cleaned files
cleaned_dir = os.path.join(os.getcwd(), "cleaned")
os.makedirs(cleaned_dir, exist_ok=True)

# Function to download CSVs from Google Trends page asynchronously
async def download_google_trends_data():
    print("Starting Google Trends data download...")
    async with async_playwright() as p:
        # Launch a headless browser
        browser = await p.chromium.launch(headless=True)
        # Create a new browser context with download capabilities
        context = await browser.new_context(accept_downloads=True)
        # Open a new page in the browser
        page = await context.new_page()
        # URL of the Google Trends page
        url = "https://trends.google.com/trends/explore?geo=IN&q=office%20chair&hl=en-GB"

        # Retry logic to handle rate limiting (429 Too Many Requests)
        max_retries = int(os.getenv("MAX_RETRIES", 5))
        for attempt in range(max_retries):
            await asyncio.sleep(5)  # Initial delay to avoid immediate rate limiting
            response = await page.goto(url)
            if response.status == 429:
                # If rate limited, retry with exponential backoff
                print(f"Retry {attempt + 1}/{max_retries} - Received 429 status code")
                await asyncio.sleep(5 + 2**attempt)  # Adding a base delay to further reduce rate limiting issues
                continue
            elif response.status != 200:
                # If the page fails to load, print an error and close the browser
                print(f"Error: Failed to load page (status {response.status})")
                await browser.close()
                return
            print("Page loaded successfully")
            break

        # Wait for the page to fully load and be idle
        await page.wait_for_load_state("networkidle", timeout=60000)
        # Wait for the download buttons to be visible
        await page.wait_for_selector("button.export", state="visible", timeout=20000)

        # Query all export buttons on the page
        download_buttons = await page.query_selector_all("button.export")
        # Filter out only the visible buttons
        download_buttons = [button for button in download_buttons if await button.is_visible()]

        # Check if the expected number of download buttons are found
        if len(download_buttons) < 4:
            print(f"Expected 4 download buttons, but found {len(download_buttons)}. Please check if all buttons are loaded properly.")
            await browser.close()
            return

        # List of file names to save the downloaded data
        file_names = [
            "Interest_Over_Time.csv",
            "Interest_By_SubRegion.csv",
            "Related_Topics.csv",
            "Related_Queries.csv",
        ]

        # Loop through the download buttons and download each CSV file
        for idx, button in enumerate(download_buttons[:4]):
            print(f"Downloading: {file_names[idx]}")
            # Scroll to the button to ensure it is interactable
            await button.scroll_into_view_if_needed()
            # Wait for the download to start after clicking the button
            async with page.expect_download() as download_info:
                await button.click()
            # Save the downloaded file with the specified name
            download = await download_info.value
            file_name = file_names[idx]
            await download.save_as(os.path.join(download_dir, file_name))
            print(f"Downloaded {file_name}")

        # Close the browser after all downloads are complete
        await browser.close()
        print("All files downloaded successfully")

# Function to clean and save "Related_Topics.csv" and "Related_Queries.csv"
def clean_related_data(file_path, output_top_path, output_rising_path, columns):
    # Check if the input file exists
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        return
    print(f"Cleaning {os.path.basename(file_path)}...")
    # Read the CSV file
    with open(file_path, "r", encoding="utf-8-sig") as file:
        csv_reader = csv.reader(file)
        lines = [line for line in csv_reader]

    # Find the start indices for TOP and RISING sections
    top_start = next(i for i, line in enumerate(lines) if line and line[0] == "TOP") + 1
    rising_start = next(i for i, line in enumerate(lines) if line and line[0] == "RISING") + 1

    # Extract data for TOP and RISING sections
    top_data = lines[top_start : rising_start - 1]
    rising_data = lines[rising_start:]

    # Create DataFrames for TOP and RISING data
    top_df = pd.DataFrame(top_data, columns=columns)
    rising_df = pd.DataFrame(rising_data, columns=columns)

    # Remove the last row from both DataFrames (usually empty or invalid data)
    top_df = top_df[:-1]
    rising_df = rising_df[:-1]

    # Save the cleaned data to separate CSV files
    top_df.to_csv(output_top_path, index=False, encoding="utf-8-sig")
    rising_df.to_csv(output_rising_path, index=False, encoding="utf-8-sig")
    print("Cleaned data saved for TOP and RISING queries")

# Function to clean and save "Interest_By_SubRegion.csv"
def clean_interest_by_subregion_data(file_path, output_path):
    # Check if the input file exists
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        return
    print(f"Cleaning {os.path.basename(file_path)}...")
    # Read the CSV file
    with open(file_path, "r", encoding="utf-8-sig") as file:
        csv_reader = csv.reader(file)
        lines = [line for line in csv_reader]

    # Create a DataFrame for the region data, skipping the first few rows
    region_data = pd.DataFrame(lines[3:], columns=["Region", "Interest"])

    # Remove the last row from the DataFrame (usually empty or invalid data)
    region_data = region_data[:-1]

    # Save the cleaned data to a CSV file
    region_data.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"Cleaned data saved: {output_path}")

# Function to clean and save "Interest_Over_Time.csv"
def clean_interest_over_time_data(file_path, output_path):
    # Check if the input file exists
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        return
    print(f"Cleaning data from: {file_path}")
    # Read the CSV file, skipping the first two rows
    df = pd.read_csv(file_path, skiprows=2)

    # Ensure the DataFrame has at least two columns
    if df.shape[1] >= 2:
        if df.shape[1] != 2:
            print(f"Warning: Found {df.shape[1]} columns, using first two")
        # Select only the first two columns and rename them
        cleaned_df = df.iloc[:, [0, 1]]
        cleaned_df.columns = ["Week", "Search Interest"]

        # Remove the last row from the DataFrame (usually empty or invalid data)
        cleaned_df = cleaned_df[:-1]

        # Save the cleaned data to a CSV file
        cleaned_df.to_csv(output_path, index=False, encoding="utf-8-sig")
        print(f"Cleaned data saved: {os.path.basename(output_path)}")
    else:
        print("Error: File has unexpected number of columns")

# Run the function using asyncio
if __name__ == "__main__":
    # Run the asynchronous function to download Google Trends data
    asyncio.run(download_google_trends_data())

    # Clean and save Related_Topics.csv
    clean_related_data(
        os.path.join(download_dir, "Related_Topics.csv"),
        os.path.join(cleaned_dir, "cleaned_top_topics.csv"),
        os.path.join(cleaned_dir, "cleaned_rising_topics.csv"),
        ["Topics", "Interest"],
    )

    # Clean and save Related_Queries.csv
    clean_related_data(
        os.path.join(download_dir, "Related_Queries.csv"),
        os.path.join(cleaned_dir, "cleaned_top_queries.csv"),
        os.path.join(cleaned_dir, "cleaned_rising_queries.csv"),
        ["Query", "Interest"],
    )

    # Clean and save Interest_By_SubRegion.csv
    clean_interest_by_subregion_data(
        os.path.join(download_dir, "Interest_By_SubRegion.csv"),
        os.path.join(cleaned_dir, "cleaned_region_data.csv"),
    )

    # Clean and save Interest_Over_Time.csv
    clean_interest_over_time_data(
        os.path.join(download_dir, "Interest_Over_Time.csv"),
        os.path.join(cleaned_dir, "cleaned_interest_over_time.csv"),
    )
    print("Data download and cleaning completed")
