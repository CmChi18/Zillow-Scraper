# Zillow-Scraper
This web scraper takes home data from a file named 'Addresses.csv' and scrapes the Zillow listing data for that home. Each listing is added to 'listings.csv' and the current index is stored in 'start-num.txt' in case the script must be stopped (each scrape takes 1 to 3 seconds to avoid CAPTCHA). It also splits listings into different files of size 2000 to put into a Google Map.
