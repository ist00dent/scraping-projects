# Yahoo Sports NBA Scores Scraper

**A Python scraper designed to collect and update NBA game scores from Yahoo Sports.** 

## Overview

This project allows users to scrape historical game scores from the NBA using Yahoo Sports’ website and save the data in a structured CSV format. The scraper retrieves scores for a specified date range, making it ideal for data analysis or archiving historical NBA scores.

## Features

- **Historical Data Scraping**: Collects NBA game scores for a specified date range.
- **Concurrent Data Fetching**: Uses multithreading to efficiently gather data for each date, improving the scraping speed.
- **Data Storage**: Saves scores in a CSV file, organized in sequential date order, for easy access and analysis.
- **Error Handling**: Provides user-friendly error messages if the data retrieval fails.

## Skills Demonstrated

- **Web Scraping**: Efficiently scraping web data with requests and BeautifulSoup.
- **Data Manipulation**: Using Pandas to organize and store the retrieved data.
- **Concurrent Processing**: Leveraging ThreadPoolExecutor for faster data retrieval.
- **Date Management**: Handling flexible date ranges for scraping historical data.

## Usage

1. **Install the required libraries**:
   ```bash
   pip install -r requirements.txt
   ```
   
2. **Adjust the Date Range**: Edit the **start_date** and **end_date** variables in main.py to specify the date range you want to scrape.

3. **Run the scraper**:
   ```bash
   python main.py
   ``` 
   
4. **View the Output**: After execution, find the generated CSV file named in the format nba_scores_<start_date>_to_<end_date>.csv containing the game scores.

## Contributing

   Feel free to fork this repository and submit pull requests for improvements and enhancements.

## Disclaimer

This project is intended for educational purposes. Please ensure that you comply with the terms of service of Yahoo Sports or any other website you scrape.



