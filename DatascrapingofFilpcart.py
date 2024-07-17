import requests
from bs4 import BeautifulSoup
import csv
import re

def scrape_flipkart_product(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        product_name = soup.find('span', {'class': 'B_NuCI'}).text.strip()
        product_price = soup.find('div', {'class': '_30jeq3 _16Jk6d'}).text.strip()
        product_rating = soup.find('div', {'class': '_3LWZlK'}).text.strip() if soup.find('div', {'class': '_3LWZlK'}) else 'No rating'
        num_reviews = soup.find('span', {'class': '_2_R_DZ'}).text.strip() if soup.find('span', {'class': '_2_R_DZ'}) else 'No reviews'

        print('Product Name:', product_name)
        print('Product Price:', product_price)
        print('Product Rating:', product_rating)
        print('Number of Reviews:', num_reviews)

        product_data = {
            'Product Name': product_name,
            'Product Price': product_price,
            'Product Rating': product_rating,
            'Number of Reviews': num_reviews
        }

        save_to_csv(product_data)

    except requests.exceptions.RequestException as e:
        print('Request Error:', e)
    except AttributeError as e:
        print('Parsing Error: Unable to find the specified element', e)
    except Exception as e:
        print('Error:', str(e))

def save_to_csv(data):
    try:
        with open('product_data.csv', mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(data.values())
        print('Data saved to CSV successfully.')
    except Exception as e:
        print('Error saving data to CSV:', e)

def main():
    url = "https://www.flipkart.com/vbuyz-women-kurta-trouser-set/p/itma73b456672d89?pid=SWDG3TVW9WJBVHVG&lid=LSTSWDG3TVW9WJBVHVGEHSOAX&marketplace=FLIPKART&store=clo%2Fcfv&srno=b_1_1&otracker=browse&fm=organic&iid=en_ZJ8VXo0qkuIsTYsMPPFIndOvp-m0NJNnjARFM4kfEvEbDDBGnvUZozjGuqH0uhUIHztMFYTb3fTQaowFn1lMLw%3D%3D&ppt=browse&ppn=browse&ssid=xlwjsj1i9s0000001699096661063"
    scrape_flipkart_product(url)

if __name__ == "__main__":
    main()
