from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import re
import pandas as pd
from seleniumbase import Driver
import traceback


# Function to check the social media platform based on the URL
def check_platform(url):
    if "instagram.com" in url:
        return "instagram"
    elif "facebook.com" in url:
        return "facebook"
    elif "tiktok.com" in url:
        return "tiktok"
    else:
        return "unknown"


# Function to get a new WebDriver instance
def get_driver():
    return Driver(uc=True, headless2=True)  # Using undetected-chromedriver


# Function to scrape TikTok profile
def scrape_tiktok(url):
    try:
        driver = get_driver()  # Get a new driver for each profile
        driver.get(url)

        # Get Account Name
        try:
            name_text = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//h1[contains(@data-e2e,'user-title')]"))
            ).text
            print(f"Name: {name_text}")
        except NoSuchElementException:
            print("Name not found.")
            name_text = "N/A"

        # Get following count
        try:
            following_count = driver.find_element(By.XPATH, "//strong[contains(@title, 'Following')]").text
            print(f"Following: {following_count}")
        except NoSuchElementException:
            print("Following count not found.")
            following_count = "N/A"

        # Get followers count
        try:
            followers_count = driver.find_element(By.XPATH, "//strong[contains(@title, 'Followers')]").text
            print(f"Followers: {followers_count}")
        except NoSuchElementException:
            print("Followers count not found.")
            followers_count = "N/A"

        # Get likes count
        try:
            likes_count = driver.find_element(By.XPATH, "//strong[contains(@title, 'Likes')]").text
            print(f"Likes: {likes_count}")
        except NoSuchElementException:
            print("Likes count not found.")
            likes_count = "N/A"

        driver.quit()
        return name_text, followers_count, likes_count, following_count

    except Exception as e:
        print(f"Error scraping TikTok profile {url}: {e}")
        traceback.print_exc()  # Log the stack trace for debugging
        return None


# Function to scrape Instagram profile
def scrape_instagram(url):
    try:
        driver = get_driver()  # Get a new driver for each profile
        driver.get(url)

        # Check if "Something went wrong" message appears
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Something went wrong')]"))
            )
            print(f"Instagram not available for {url}, skipping...")
            driver.quit()
            return None  # Instagram not available
        except:
            pass  # No error means Instagram is accessible

        # Wait for the account name (header) to be visible
        try:
            account_name = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//h2[contains(@style, 'base-line-clamp')]"))
            ).text
            print(f"Account Name: {account_name}")
        except NoSuchElementException:
            print("Account name not found.")
            account_name = "N/A"

        # Get the followers count
        try:
            followers_button = driver.find_element(By.XPATH, "//button[contains(text(),'followers')]")
            followers_count = followers_button.find_element(By.XPATH, ".//span").get_attribute("title")
            print(f"Followers: {followers_count}")
        except NoSuchElementException:
            print("Followers count not found.")
            followers_count = "N/A"

        driver.quit()
        return account_name, followers_count, None  # Instagram has no likes field

    except Exception as e:
        print(f"Error scraping Instagram profile {url}: {e}")
        traceback.print_exc()  # Log the stack trace for debugging
        return None


# Function to scrape Facebook profile
def scrape_facebook(url):
    try:
        driver = get_driver()  # Get a new driver for each profile
        driver.get(url)

        # Get Account Name
        try:
            name_text = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//h1"))
            ).text
            print(f"Name: {name_text}")
        except NoSuchElementException:
            print("Name not found.")
            name_text = "N/A"

        # Get likes count
        try:
            likes_element = driver.find_element(By.XPATH, "//a[contains(@href, 'friends_likes')]")
            likes_count = parse_number_from_text(likes_element.text)  # Extract number from the text
            print(f"Likes: {likes_count}")
        except NoSuchElementException:
            print("Likes count not found.")
            likes_count = "N/A"

        # Get followers count
        try:
            followers_elements = driver.find_element(By.XPATH, "//a[contains(@href, 'followers')]")
            followers_count = parse_number_from_text(followers_elements.text)
            print(f"Followers: {followers_count}")
        except NoSuchElementException:
            print("Followers count not found.")
            followers_count = "N/A"

        # Get following count
        try:
            following_elements = driver.find_element(By.XPATH, "//a[contains(@href, 'following')]")
            following_count = parse_number_from_text(following_elements.text)
            print(f"Following: {following_count}")
        except NoSuchElementException:
            print("Following count not found.")
            following_count = "N/A"

        driver.quit()
        return name_text, followers_count, likes_count, following_count

    except Exception as e:
        print(f"Error scraping Facebook profile {url}: {e}")
        traceback.print_exc()  # Log the stack trace for debugging
        return None


# Function to parse the number from text (removing words like 'likes' or 'followers')
def parse_number_from_text(text):
    # Use regex to extract the number part and check for 'K' or 'M'
    match = re.search(r'([\d\.]+)([KM]?)', text)
    if match:
        number = match.group(1)  # Get the number part
        unit = match.group(2).upper()  # Get the unit part ('K' or 'M')
        return f"{number}{unit}"
    return None


# Function to remove empty lines and read URLs from the text file
def read_urls_from_file(file_path):
    with open(file_path, 'r') as file:
        urls = [url.strip() for url in file.readlines() if url.strip()]  # Remove empty lines
    return urls


# Function to save the results to an Excel file using pandas with xlsxwriter
def save_to_excel(results, output_file):
    # Create a pandas DataFrame from the results
    df = pd.DataFrame(results, columns=['Name', 'Followers', 'Likes', 'Following', 'Link', 'Social Media Platform'])

    # Write the DataFrame to an Excel file with xlsxwriter engine
    with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)

# Main function to process profiles sequentially
def scrape_profiles(file_path, output_file):
    urls = read_urls_from_file(file_path)
    results = []

    for url in urls:
        platform = check_platform(url)
        print(f"Scraping URL: {url}")

        if platform == "instagram":
            result = scrape_instagram(url)
            if result:
                account_name, followers_count, _ = result
                results.append([account_name, followers_count, "", "", url, "instagram"])

        elif platform == "facebook":
            result = scrape_facebook(url)
            if result:
                name_text, followers_count, likes_count, following_count = result
                results.append([name_text, followers_count, likes_count, following_count, url, "facebook"])

        elif platform == "tiktok":
            result = scrape_tiktok(url)
            if result:
                name_text, followers_count, likes_count, following_count = result
                results.append([name_text, followers_count, likes_count, following_count, url, "tiktok"])

        else:
            print(f"Unknown platform for {url}")

    print("Saving results to excel")

    # Save the results to an Excel file
    save_to_excel(results, output_file)

    return len(urls)


# Ensure the script runs only when executed as the main program
if __name__ == '__main__':
    # Example usage: Pass the file path containing Instagram/Facebook URLs and output Excel file
    number = scrape_profiles('social_media_profiles.txt', 'social_media_profiles.xlsx')
    print(f"Done Scraping {number} links")
