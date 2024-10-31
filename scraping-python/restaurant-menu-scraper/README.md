# Restaurant Menu Scraper

**A web scraper designed to extract product information from restaurant menus.**

## Overview

This project utilizes SeleniumBase to scrape product details from a specified restaurant menu page. The information retrieved includes categories, subcategories, product names, descriptions, and prices. The scraped data is then saved into an Excel file for easy analysis and reference.

## Features

- **Headless Browsing**: The scraper operates in headless mode, allowing it to run without displaying a browser window.
- **HTML Fetching with Retry Logic**: Implements robust error handling with retry attempts to ensure successful page loading.
- **Dynamic Data Parsing**: Utilizes XPath for precise selection and extraction of product details from the HTML content.
- **Excel Output**: Saves the scraped data into an Excel file sorted alphabetically by category, using Pandas for easy viewing and further processing.

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
   
3. **Specify the menu URL**: Modify the menu_url variable in main.py to point to the desired restaurant menu page.

4. **Check the generated Excel file**: After execution, find the output Excel file named **dominos_pizza_menu.xlsx** containing the product details.


## Sample Restaurant to Scrape

This project uses the following restaurant website as a sample: [Domino's Pizza Philippines](https://www.dominospizza.ph/pages/order/menu)

**Important Note**: The site referenced in this project is **not** owned by me. This scraper is intended for **educational and illustrative purposes only**. Ensure compliance with the respective website's terms of service and copyright regulations when using this scraper.

## Contributing

Feel free to fork this repository and submit pull requests for improvements and enhancements.