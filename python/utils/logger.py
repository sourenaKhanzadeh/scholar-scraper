from loguru import logger
import os

# Create log directory if it doesn't exist
log_dir = "../shared/logs"
os.makedirs(log_dir, exist_ok=True)

# Configure loguru
logger.add(f"{log_dir}/scraper.log", rotation="10 MB", retention="7 days", level="DEBUG", format="<green>{time}</green> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>")
