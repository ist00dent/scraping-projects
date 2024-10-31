import time
import pandas as pd
from selenium.webdriver.common.by import By
from seleniumbase import Driver
from seleniumbase.common.exceptions import TimeoutException
from concurrent.futures import ThreadPoolExecutor, as_completed


class RestaurantMenuScraper:
    def __init__(self):
        """Initialize the Selenium driver."""
        self.driver = Driver(headless2=True)

    def fetch_html(self, url, wait_element='body', retries=3, max_wait_time=15):
        """Fetch HTML content from the given URL with retry logic."""
        for attempt in range(retries):
            try:
                self.driver.open(url)
                self.driver.wait_for_element(wait_element, by=By.XPATH, timeout=max_wait_time)
                return True
            except TimeoutException:
                print(f"Attempt {attempt + 1} failed; retrying...")
                time.sleep(2)
        print(f"Failed to fetch page after {retries} attempts.")
        return False

    def parse_subcategory_products(self, subcategory_section, category_name):
        """Parse product details within a specific subcategory section, adding category name."""
        subcategory_name = subcategory_section.find_element(By.XPATH, './/header//h2').text.strip()
        products = []

        product_elements = subcategory_section.find_elements(By.XPATH,
                                                             './/div[contains(@class, "media--national-menu-product")]')
        for product in product_elements:
            name = product.find_element(By.XPATH, './/h3[@class="media__title"]//a').text.strip() or 'N/A'
            description = product.find_element(By.XPATH,
                                               './/div[contains(@class,"media__product-description")]').text.strip() or 'N/A'
            price = product.find_element(By.XPATH,
                                         './/div[@class="subtext " or @class="subtext media__product-price"]').text.strip() or 'N/A'

            product_data = {
                'Category': category_name,
                'Subcategory': subcategory_name,
                'Name': name,
                'Description': description,
                'Price': price
            }

            if name != "N/A" and price != "N/A" and product_data not in products:
                products.append(product_data)

        print(f"{subcategory_name} (Subcategory) -- Done Processing")
        return products

    def scrape_category_subcategories(self, category_url, category_name):
        """Scrape products for subcategories within a single category."""
        all_products = []

        if not self.fetch_html(category_url, '//div[contains(@id, "js-categoryArea")]'):
            return []

        print(f"{category_name} (Category) -- Processing")

        subcategory_sections = self.driver.find_elements(By.XPATH,
                                                         '//section[contains(@class, "card category category-order__")]')
        for section in subcategory_sections:
            subcategory_products = self.parse_subcategory_products(section, category_name)
            all_products.extend(subcategory_products)

        return all_products

    def close(self):
        """Close the Selenium driver."""
        self.driver.quit()


def get_categories(url):
    """Fetch category URLs and names from the main menu page."""
    category_card = '//div[contains(@class, "card__body category-panel")]'
    temp_scraper = RestaurantMenuScraper()

    if not temp_scraper.fetch_html(url, category_card):
        temp_scraper.close()
        return []

    category_elements = temp_scraper.driver.find_elements(By.XPATH, f'{category_card}//a[@href]')
    category_data = [
        {
            'url': el.get_attribute('href'),
            'name': el.find_element(By.XPATH, './/h2[contains(@class, "media__title")]').text.strip()
        }
        for el in category_elements
    ]

    temp_scraper.close()
    return category_data


def main(url):
    categories = get_categories(url)
    print(f"Found {len(categories)} categories to process.")

    all_products = []

    with ThreadPoolExecutor() as executor:
        future_to_category = {
            executor.submit(scrape_category_products, category['url'], category['name']): category
            for category in categories
        }

        for future in as_completed(future_to_category):
            try:
                category_products = future.result()
                all_products.extend(category_products)
            except Exception as e:
                print(f"Error processing category: {e}")

    save_to_excel(all_products)


def scrape_category_products(category_url, category_name):
    """Creates a new scraper instance per category and processes products."""
    scraper = RestaurantMenuScraper()
    try:
        category_products = scraper.scrape_category_subcategories(category_url, category_name)
        print(f"{category_name} (Category) -- Done Processing")
    finally:
        scraper.close()
    return category_products


def save_to_excel(all_products):
    """Save product details to an Excel file, sorted alphabetically by category."""
    filename = "dominos_pizza_menu.xlsx"
    if all_products:
        df = pd.DataFrame(all_products)
        df.sort_values(by="Category", inplace=True)  # Sort alphabetically by category
        df.to_excel(filename, index=False)
        print(f"Data saved to {filename}")
    else:
        print("No products found to save.")


if __name__ == "__main__":
    menu_url = 'https://www.dominospizza.ph/pages/order/menu'
    main(menu_url)
