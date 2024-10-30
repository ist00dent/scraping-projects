# Shopify Scraper

**A web scraper designed to extract product information from Shopify e-commerce websites.**

## Overview

This project utilizes SeleniumBase and lxml to scrape product details from a specified Shopify category page. The information retrieved includes product IDs, names, colors, and prices. The scraped data is then saved into an Excel file for easy analysis and reference.

## Features

- **Headless Browsing**: The scraper runs in headless mode, allowing it to operate without opening a browser window.
- **HTML Fetching with Retry Logic**: Implements robust error handling with retry attempts to ensure successful page loading.
- **Dynamic Data Parsing**: Utilizes XPath for precise selection and extraction of product details from the HTML content.
- **Excel Output**: Saves the scraped data into an Excel file using Pandas for easy viewing and further processing.

## Skills Demonstrated

- **Web Scraping**: Proficient in utilizing web scraping techniques to gather data from dynamic websites.
- **Error Handling**: Effective handling of timeouts and retries to improve the reliability of web data extraction.
- **Data Manipulation**: Leveraging Pandas for data organization and outputting to Excel format.

## Usage

1. **Install the required libraries**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the scraper**:
   ```bash
   python main.py
   ```
   
3. **Specify the category URL**: Modify the category variable in main.py to point to the desired Shopify category page.

4. **Check the generated Excel file**: After execution, find the output Excel file named <shop_name>_<category_name>.xlsx containing the product details.

## Sample E-commerce Site to Scrape
This project uses the following Shopify e-commerce website as a sample:
[Thursday Boots](https://thursdayboots.com/)

Example Category URL: [Boots Collection](https://thursdayboots.com/collections/boots)

**Important Note**: The site referenced in this project is not owned by me. This scraper is intended for educational and illustrative purposes only. Ensure compliance with the respective website's terms of service and copyright regulations when using this scraper.

## Contributing

   Feel free to fork this repository and submit pull requests for improvements and enhancements.

