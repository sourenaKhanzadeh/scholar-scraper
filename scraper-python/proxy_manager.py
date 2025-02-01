import random
import yaml
import logging
import pathlib

# Load configurations
with open(pathlib.Path(__file__).parent / "config.yaml", "r") as config_file:

    config = yaml.safe_load(config_file)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ProxyManager:
    def __init__(self):
        self.proxies = config.get("proxies", [])
        if not self.proxies:
            logging.warning("No proxies found in config.yaml. Scraping may be blocked.")

    def get_random_proxy(self):
        """Returns a random proxy from the list."""
        if not self.proxies:
            return None
        return random.choice(self.proxies)

    def rotate_proxy(self):
        """Rotates the proxy by randomly selecting another one."""
        return self.get_random_proxy()

# Example usage
if __name__ == "__main__":
    proxy_manager = ProxyManager()
    proxy = proxy_manager.get_random_proxy()
    logging.info(f"Using proxy: {proxy}")
