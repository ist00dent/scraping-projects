# Social Media Profile Scraper

**A web scraper for extracting profile information from Instagram, Facebook, and TikTok.**

## Overview

This project uses SeleniumBase to scrape selected details from social media profiles on Instagram, Facebook, and TikTok. Extracted information includes names, follower counts, likes, and other profile metrics. The data is saved in an Excel file for easy access and analysis.

## Features

- **Supports Multiple Platforms**: Scrapes Instagram, Facebook, and TikTok profiles using platform-specific XPaths.
- **Error Handling and Retry Logic**: Built-in mechanisms handle unexpected errors, maximizing profile scraping success.
- **Excel Output**: Organizes and saves scraped data in an Excel file for easy viewing and further processing.
- **Platform Detection**: Identifies the platform from the URL, ensuring correct data extraction for each profile.

## Skills Demonstrated

- **Web Scraping**: Proficient in utilizing web scraping techniques to gather data from dynamic websites.
- **Error Handling**: Effective handling of timeouts and retries to improve the reliability of web data extraction.
- **Data Manipulation**: Leveraging Pandas for data organization and outputting to Excel format.

## Usage

1. **Install the required libraries**:
   ```bash
   pip install -r requirements.txt
    ```

2. **Add profile URLs to the input file**:
   Add Instagram, Facebook, or TikTok profile URLs to social_media_profiles.txt, one per line.

3. **Run the scraper**:
    ```bash
    python main.py
   ```

4. **Check the generated Excel file**: The output Excel file, **social_media_profiles.xlsx**, will contain details for each scraped profile, including name, followers, likes, following, and link.


## Example Platforms Scraped

This project demonstrates scraping social media profiles using random links chosen solely for testing purposes. These profiles are used as **examples only** and do not represent any endorsement or affiliation. Always respect each platform’s terms of service and copyright regulations.


## Contributing

Feel free to fork this repository and submit pull requests for further improvements and enhancements, such as adding multithreading capabilities or additional social media platforms.