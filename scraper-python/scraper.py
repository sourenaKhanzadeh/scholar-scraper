import asyncio
from playwright.async_api import async_playwright
import random
import time
import yaml
import logging
from proxy_manager import ProxyManager
from captcha_solver import CaptchaSolver
import pathlib

# Load configurations
with open(pathlib.Path(__file__).parent / "config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ScholarScraper:
    def __init__(self):
        self.base_url = "https://scholar.google.com"
        self.proxy_manager = ProxyManager()
        self.captcha_solver = CaptchaSolver()
        self.user_agents = config.get("user_agents", [])
        
    async def _get_browser(self):
        """Launch a Playwright browser with proxy and stealth settings."""
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(headless=True)
        context = await browser.new_context(user_agent=random.choice(self.user_agents))  # Set user agent correctly
        return browser, context, playwright
    
    async def scrape(self, query):
        """Scrapes Google Scholar search results for the given query."""
        browser, context, playwright = await self._get_browser()
        page = await context.new_page()  # Create a page from the context
        
        # Navigate to Scholar search page
        search_url = f"{self.base_url}/scholar?q={query.replace(' ', '+')}"
        logging.info(f"Scraping: {search_url}")
        
        await page.goto(search_url, wait_until="domcontentloaded")
        
        # Handle CAPTCHA if detected
        if await page.query_selector("#gs_captcha_ccl"):  
            logging.warning("CAPTCHA detected! Attempting to solve...")
            captcha_image_path = "captcha_image.png"
            await page.screenshot(path=captcha_image_path)
            captcha_text = self.captcha_solver.solve(captcha_image_path)
            
            if captcha_text:
                await page.fill("input[name='captcha']", captcha_text)
                await page.click("input[type='submit']")
                time.sleep(2)
            else:
                logging.error("Failed to solve CAPTCHA. Retrying with new proxy...")
                await browser.close()
                return await self.scrape(query)
        
        # Extract search results
        results = await page.evaluate("""
            () => {
                let articles = [];
                document.querySelectorAll('.gs_r.gs_or.gs_scl').forEach(article => {
                    let title = article.querySelector('.gs_rt a')?.innerText || "No Title";
                    let link = article.querySelector('.gs_rt a')?.href || "";
                    let snippet = article.querySelector('.gs_rs')?.innerText || "";
                    let citation_info = article.querySelector('.gs_fl a')?.innerText || "";
                    
                    articles.push({ title, link, snippet, citation_info });
                });
                return articles;
            }
        """)
        
        await browser.close()
        await playwright.stop()
        return results

# Example usage
if __name__ == "__main__":
    async def main():
        query = "Reinforcement Learning Smart Contracts"
        scraper = ScholarScraper()
        results = await scraper.scrape(query)
        
        for idx, result in enumerate(results):
            logging.info(f"{idx+1}. {result['title']} ({result['link']})")
            logging.info(f"Snippet: {result['snippet']}")
            logging.info(f"Citations: {result['citation_info']}")
            logging.info("-" * 80)

    asyncio.run(main())
