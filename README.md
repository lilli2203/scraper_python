# Web Scraper for Amazon, Snapdeal, and Flipkart

This web scraper extracts product details from Amazon, Snapdeal, and Flipkart, and compares their prices. It outputs the product name, price, and identifies the lowest price among the three platforms. The results are displayed in a tabulated format and saved to a CSV file.

## Features

- Scrapes product name and price from Amazon, Snapdeal, and Flipkart.
- Compares prices across these three e-commerce platforms.
- Displays results in a formatted table using the `tabulate` library.
- Saves the scraped data to a CSV file.
- Provides robust error handling and user feedback.

## Requirements

- Python 3.x
- Required Python packages:
  - `requests`
  - `beautifulsoup4`
  - `tabulate`

Install the required packages:
bash
Copy code
pip install requests beautifulsoup4 tabulate
Usage
Run the script:

bash
Copy code
python webscraper.py
Enter the product URLs:

The script will prompt you to enter the Amazon, Snapdeal, and Flipkart product URLs.
Example URLs:
Amazon: https://www.amazon.in/dp/B08L5V3P5M
Snapdeal: https://www.snapdeal.com/product/samsung-galaxy-m21-64gb/
Flipkart: https://www.flipkart.com/samsung-galaxy-f41/p/itmf3ac5a2ae8f4e
View the results:

The script will display the product details in a tabulated format.
The lowest price among the three platforms will be highlighted.
Check the CSV file:

The scraped data will be saved to a file named product_data.csv in the same directory as the script.
Example Output
diff
Copy code
<br>
+-----------+------------------------------+----------------+
| Website   | Product Name                 | Product Price  |
+-----------+------------------------------+----------------+
| Amazon    | Samsung Galaxy M21           | ₹12,499        |
| Snapdeal  | Samsung Galaxy M21           | ₹12,599        |
| Flipkart  | Samsung Galaxy F41           | ₹12,499        |
+-----------+------------------------------+----------------+
| Comparison|                              | Lowest Price: Amazon |
+-----------+------------------------------+----------------+
