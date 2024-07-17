import requests
from bs4 import BeautifulSoup
import json
import time

def scrape_amazon_product(url, max_retries=5):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
    }
    retry_count = 0
    product_details = {}

    while retry_count < max_retries:
        try:
            response = requests.get(url, headers=headers)
            status_code = response.status_code

            if status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                product_name = soup.find('span', class_='a-size-large product-title-word-break')
                if product_name:
                    product_details['Name'] = product_name.get_text().strip()
                
                price_element = soup.find('span', class_='a-price-whole')
                price_fraction = soup.find('span', class_='a-price-fraction')
                if price_element and price_fraction:
                    product_details['Price'] = price_element.get_text().strip() + price_fraction.get_text().strip()

                rating = soup.find('span', class_='a-icon-alt')
                if rating:
                    product_details['Rating'] = rating.get_text().strip()
                
                reviews = soup.find('span', id='acrCustomerReviewText')
                if reviews:
                    product_details['Reviews'] = reviews.get_text().strip()
                
                availability = soup.find('div', id='availability')
                if availability:
                    product_details['Availability'] = availability.find('span').get_text().strip()

                for key, value in product_details.items():
                    print(f"{key}: {value}")
                
                with open('product_details.json', 'w') as file:
                    json.dump(product_details, file, indent=4)

                break
            else:
                retry_count += 1
                print(f"Retrying... ({retry_count}/{max_retries})")
                time.sleep(2)
        except requests.exceptions.RequestException as e:
            retry_count += 1
            print(f"Request failed: {e}. Retrying... ({retry_count}/{max_retries})")
            time.sleep(2)
        except Exception as e:
            print(f"An error occurred: {e}")
            break

    if retry_count == max_retries:
        print("Max retries reached. Failed to fetch the product details.")
    else:
        print("Product details fetched successfully.")

if __name__ == "__main__":
    url = input("Enter the Amazon product URL: ")
    max_retries = int(input("Enter the number of retry attempts: "))
    scrape_amazon_product(url, max_retries)
