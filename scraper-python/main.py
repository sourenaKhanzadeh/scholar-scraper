import asyncio
import logging
from scraper import ScholarScraper
import sys
import json

sys.path.append(r"C:\Users\user\Desktop\scraper-python\parser-rust")

import parser_rust

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


def save_data(scraped_data):
    json_data = json.dumps(scraped_data)
    response = parser_rust.save_to_mongo(json_data)  # Call Rust function
    return response


if __name__ == "__main__":
    # asyncio.run(main())
    # data = [
    # {
    #     "title": "Reinforcement Learning for Smart Contracts",
    #     "link": "https://scholar.google.com/example",
    #     "snippet": "This paper explores RL in smart contract optimizations...",
    #     "citation_info": "Cited by 32"
    #     }
    # ]
    # cleaned_data = parser_rust.process_articles(json.dumps(data))
    # print(json.loads(cleaned_data))

    scraped_data = [
        {
            "title": "Reinforcement Learning for Smart Contracts",
            "link": "https://scholar.google.com/example",
            "snippet": "This paper explores RL in smart contract optimizations...",
            "citation_info": "Cited by 32"
        }
    ]

    result = save_data(scraped_data)
    print(result) 

