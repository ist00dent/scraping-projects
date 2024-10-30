import time
import pandas as pd
from selenium.webdriver.common.by import By
from seleniumbase import Driver
from lxml import html
from seleniumbase.common.exceptions import TimeoutException


class ShopifyScraper:
    def __init__(self):
        """Initialize the Selenium driver in headless mode."""
        self.driver = Driver(headless2=True)

    def fetch_html(self, url, wait_element='body', retries=3, max_wait_time=15):
        """Fetch HTML content from the given URL with retry logic.

        Args:
            url (str): The URL to fetch.
            wait_element (str): The XPath or CSS selector for an element to wait for.
            retries (int): Number of retries in case of failure.
            max_wait_time (int): Maximum time to wait for the element to load.

        Returns:
            str: The HTML content of the page or None if failed.
        """
        for attempt in range(retries):
            try:
                self.driver.open(url)
                self.driver.wait_for_element(wait_element, by=By.XPATH, timeout=max_wait_time)  # Extend wait time
                return self.driver.get_page_source()
            except TimeoutException:
                print(f"Attempt {attempt + 1} failed; retrying...")
                time.sleep(2)
        print(f"Failed to fetch page after {retries} attempts.")
        return None

    def parse_products(self, html_content):
        """Parse product details from the HTML content of a category page."""
        products = []
        tree = html.fromstring(html_content)

        product_list = tree.xpath('//ul[contains(@class, "products")]/li[contains(@class, "product")]')
        for product in product_list:
            product_id = product.get('data-product-id')
            name = product.xpath('.//h2[@class="title"]/text()')
            name = name[0].strip() if name else 'N/A'
            color = product.xpath('.//h4[@class="color"]/text()')
            color = color[0].strip() if color else 'N/A'
            price = product.xpath('.//p[contains(@class, "price")]/span[contains(@class, "money")]/text()')
            price = price[0].strip() if price else 'N/A'

            product = {
                'Product ID': product_id,
                'Name': name,
                'Color': color,
                'Price': price
            }

            if name == "N/A" or color == "N/A" or price == "N/A" or product in products:
                continue

            products.append(product)

        if not products:
            print("No products found in this category.")

        return products

    def save_to_excel(self, shop_name, category_name, all_products):
        """Save product details to an Excel file."""
        df = pd.DataFrame(all_products)
        filename = f"{shop_name}_{category_name}.xlsx"
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=category_name, index=False)
        print(f"Data saved to {filename} with sheet '{category_name}'")

    def scrape(self, category_url):
        """Main function to fetch and print product details for a specific category."""
        base_url = "https://thursdayboots.com"

        # Adjusted to wait for a specific category section
        category_html = self.fetch_html(category_url, wait_element='//section[contains(@class, "product-group")]', max_wait_time=20)

        if not category_html:
            print("Unable to load category page.")
            return

        all_products = self.parse_products(category_html)

        if all_products:
            shop_name = base_url.split('//')[1].split('.')[0]
            category_name = category_url.split('/')[-1]  # Get the last part of the category URL
            self.save_to_excel(shop_name, category_name, all_products)
        else:
            print("No products found.")

    def close(self):
        """Close the Selenium driver."""
        self.driver.quit()


if __name__ == "__main__":
    category = 'https://thursdayboots.com/collections/boots'  # Change this to your desired category URL
    shop_scraper = ShopifyScraper()
    shop_scraper.scrape(category)
    shop_scraper.close()
