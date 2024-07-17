import requests
from bs4 import BeautifulSoup
import json
import time
import re
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email_notification(product_details):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Amazon Product Details Scraped Successfully"

    body = json.dumps(product_details, indent=4)
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print("Email notification sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

def validate_url(url):
    amazon_url_pattern = re.compile(r"https?://(www\.)?amazon\.(com|in|co\.uk|ca|de|fr|jp)/.*")
    return re.match(amazon_url_pattern, url)

def scrape_amazon_product(url, max_retries=5):
    if not validate_url(url):
        print("Invalid Amazon URL.")
        return
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
    }
    retry_count = 0
    product_details = {}

    logging.basicConfig(filename='scrape_amazon.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

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

                features = soup.find('div', id='feature-bullets')
                if features:
                    product_details['Features'] = features.get_text().strip()

                questions = soup.find('a', class_='a-link-normal askATFLink')
                if questions:
                    product_details['Customer Questions'] = questions.get_text().strip()

                for key, value in product_details.items():
                    print(f"{key}: {value}")
                
                with open('product_details.json', 'w') as file:
                    json.dump(product_details, file, indent=4)

                send_email_notification(product_details)
                logging.info("Product details fetched and saved successfully.")
                break
            else:
                retry_count += 1
                wait_time = 2 ** retry_count
                print(f"Retrying in {wait_time} seconds... ({retry_count}/{max_retries})")
                time.sleep(wait_time)
        except requests.exceptions.RequestException as e:
            retry_count += 1
            wait_time = 2 ** retry_count
            logging.error(f"Request failed: {e}. Retrying in {wait_time} seconds... ({retry_count}/{max_retries})")
            time.sleep(wait_time)
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            break

    if retry_count == max_retries:
        print("Max retries reached. Failed to fetch the product details.")
        logging.error("Max retries reached. Failed to fetch the product details.")
    else:
        print("Product details fetched successfully.")
        logging.info("Product details fetched successfully.")

if __name__ == "__main__":
    url = input("Enter the Amazon product URL: ")
    max_retries = int(input("Enter the number of retry attempts: "))
    scrape_amazon_product(url, max_retries)
