import asyncio
import logging
from scraper import ScholarScraper
import sys

# Fix for Playwright not working with asyncio on Windows
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def main():
    try:
        query = "Reinforcement Learning Smart Contracts"
        scraper = ScholarScraper()
        results = await scraper.scrape(query)
        
        if not results:
            logging.warning("No results found.")
            return
        
        for idx, result in enumerate(results):
            title = result.get('title', 'No Title')
            link = result.get('link', 'No Link')
            snippet = result.get('snippet', 'No Snippet')
            citation_info = result.get('citation_info', 'No Citation Info')
            
            logging.info(f"{idx+1}. {title} ({link})")
            logging.info(f"Snippet: {snippet}")
            logging.info(f"Citations: {citation_info}")
            logging.info("-" * 80)
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
