#! /usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from utils.logger import logger
from utils.config import load_config
from scraper.data_cleaner import DataCleaner

class ScholarScraper:
    def __init__(self):
        self.config = load_config()
        self.ua = UserAgent()
        self.base_url = "https://scholar.google.com"
        self.headers = {"User-Agent": self.ua.random}
        self.session = requests.Session()

    def search(self, query):
        search_url = f"{self.base_url}/scholar?q={query}"
        try:
            response = self.session.get(search_url, headers=self.headers)
            response.raise_for_status()
            results = self.parse_results(response.text)

            logger.debug(f"Scraped {len(results)} results before cleaning.")
            cleaner = DataCleaner(results)
            cleaned_results = cleaner.process()
            return cleaned_results
        except requests.RequestException as e:
            logger.error(f"Error fetching search results: {e}")
            return []


    def parse_results(self, html):
        soup = BeautifulSoup(html, "lxml")
        results = []
        for entry in soup.select(".gs_ri"):
            title = entry.select_one(".gs_rt").get_text(strip=True) if entry.select_one(".gs_rt") else "No Title"
            author_info = entry.select_one(".gs_a").get_text(strip=True) if entry.select_one(".gs_a") else "No Authors"
            abstract = entry.select_one(".gs_rs").get_text(strip=True) if entry.select_one(".gs_rs") else "No Abstract"
            # Extract the link to the article   
            link = entry.select_one(".gs_rt a")["href"] if entry.select_one(".gs_rt a") else "No Link"
            results.append({
                "title": title,
                "authors": author_info,
                "abstract": abstract,
                "link": link
            })
        return results

if __name__ == "__main__":
    scraper = ScholarScraper()
    query = "Reinforcement Learning Smart Contracts"
    results = scraper.search(query)

    if not results.empty:
        print(results.to_string(index=False))  # Display full DataFrame without index
    else:
        logger.warning("No results found after cleaning.")
