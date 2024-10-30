import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed

class YahooSportsScoresScraper:
    def __init__(self):
        """Initialize the scraper with the Yahoo Sports base URL."""
        self.base_url = 'https://sports.yahoo.com/nba/scoreboard/'

    def fetch_scores(self, date):
        """Fetch game scores for a specific date."""
        date_str = date.strftime('%Y-%m-%d')
        url = f'{self.base_url}?confId=&dateRange={date_str}&schedState='
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.text, date_str
        else:
            print(f"Failed to fetch data for {date_str}. Status code: {response.status_code}")
            return None, date_str

    def parse_scores(self, html_content, date_str):
        """Parse scores from the fetched HTML content."""
        soup = BeautifulSoup(html_content, 'html.parser')
        scores = []

        no_games_message = soup.find('span', string=lambda x: x and 'No games in NBA Scores are scheduled on' in x)
        if no_games_message:
            scores.append({
                'Date': date_str,
                'Home Team': 'N/A',
                'Away Team': 'N/A',
                'Home Score': 'N/A',
                'Away Score': 'N/A',
                'Highlights Link': 'No games scheduled'
            })
            return scores

        games = soup.find_all('li', class_=lambda x: x and 'Bgc(bg-mod)' in x and 'Pos(r)' in x and 'Mb(20px)' in x and 'D(ib)' in x)
        for game in games:
            try:
                teams = game.find_all('li', class_=lambda x: x and 'D(tb) team' in x)
                if len(teams) == 2:
                    home_team_name_elem = teams[1].find('span', class_=lambda x: x and 'YahooSans Fw(700)! Fz(14px)!' in x)
                    away_team_name_elem = teams[0].find('span', class_=lambda x: x and 'YahooSans Fw(700)! Fz(14px)!' in x)
                    home_team_score_elem = teams[1].find('span', class_=lambda x: x and 'YahooSans Fw(700)! Va(m) Fz(24px)!' in x)
                    away_team_score_elem = teams[0].find('span', class_=lambda x: x and 'YahooSans Fw(700)! Va(m) Fz(24px)!' in x)

                    if home_team_name_elem and away_team_name_elem and home_team_score_elem and away_team_score_elem:
                        home_team_name = home_team_name_elem.text
                        away_team_name = away_team_name_elem.text
                        home_team_score = int(home_team_score_elem.text)
                        away_team_score = int(away_team_score_elem.text)

                        # Extract the highlights link if available
                        highlights_elem = game.find('a', class_="D(b) Px(20px) Py(8px) C(#000) Bgc(#ededf3)")
                        highlights_link = f"https://sports.yahoo.com{highlights_elem['href']}" if highlights_elem else "No highlights available"

                        score_info = {
                            'Date': date_str,
                            'Home Team': home_team_name,
                            'Home Score': home_team_score,
                            'Away Team': away_team_name,
                            'Away Score': away_team_score,
                            'Highlights Link': highlights_link
                        }
                        scores.append(score_info)

            except Exception as e:
                print(f"Error parsing game on {date_str}: {e}")

        print(f"{date_str} - Done Processing.")
        return scores

    def save_to_csv(self, scores, start_date, end_date):
        """Save scores to a CSV file with date range in the filename."""
        df = pd.DataFrame(scores)
        # Sort the data by date in ascending order
        df['Date'] = pd.to_datetime(df['Date'])  # Convert to datetime for sorting
        df = df.sort_values(by='Date')           # Sort by the date column
        filename = f'nba_scores_{start_date.strftime("%Y%m%d")}_to_{end_date.strftime("%Y%m%d")}.csv'
        df.to_csv(filename, index=False)
        print(f"Scores saved to {filename}")

    def scrape_historical_scores(self, start_date, end_date):
        """Scrape historical scores between two dates using concurrency."""
        current_date = start_date
        date_list = []

        while current_date <= end_date:
            date_list.append(current_date)
            current_date += timedelta(days=1)

        all_scores = []

        # Using ThreadPoolExecutor to handle concurrency for each day
        with ThreadPoolExecutor() as executor:
            future_to_date = {executor.submit(self.fetch_scores, date): date for date in date_list}

            for future in as_completed(future_to_date):
                html_content, date_str = future.result()
                if html_content:
                    parsed_scores = self.parse_scores(html_content, date_str)
                    all_scores.extend(parsed_scores)

        if all_scores:
            self.save_to_csv(all_scores, start_date, end_date)


if __name__ == "__main__":
    start_date = datetime(2024, 9, 24)  # Adjust start date
    end_date = datetime(2024, 10, 24)   # Adjust end date
    scraper = YahooSportsScoresScraper()
    scraper.scrape_historical_scores(start_date, end_date)
