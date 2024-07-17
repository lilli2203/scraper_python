import requests
from bs4 import BeautifulSoup
import json
import time

def scrape_snapdeal_product(url, max_retries=5):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }
    retry_count = 0
    product_details = {}

    while retry_count < max_retries:
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                

                product_name = soup.find('h1', {'class': 'pdp-e-i-head'})
                if product_name:
                    product_details['Name'] = product_name.get_text().strip()
                

                product_price = soup.find('span', {'class': 'payBlkBig'})
                if product_price:
                    product_details['Price'] = product_price.get_text().strip()
                

                product_description = soup.find('div', {'class': 'detailssubbox'})
                if product_description:
                    product_details['Description'] = product_description.get_text().strip()
                

                            rating = soup.find('span', {'class': 'avrg-rating'})
                if rating:
                    product_details['Rating'] = rating.get_text().strip()
                

                                reviews = soup.find('div', {'class': 'numbr-review'})
                if reviews:
                    product_details['Reviews'] = reviews.get_text().strip()
                
                availability = soup.find('div', {'class': 'availability'})
                if availability:
                    product_details['Availability'] = availability.get_text().strip()

                for key, value in product_details.items():
                    print(f"{key}: {value}")
                
                with open('snapdeal_product_details.json', 'w') as file:
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
    url = input("Enter the Snapdeal product URL: ")
    max_retries = int(input("Enter the number of retry attempts: "))
    scrape_snapdeal_product(url, max_retries)
