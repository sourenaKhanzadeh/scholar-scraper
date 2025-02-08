#! /usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd
from utils.logger import logger

class DataCleaner:
    def __init__(self, raw_data):
        self.raw_data = pd.DataFrame(raw_data)

    def remove_duplicates(self):
        initial_count = len(self.raw_data)
        self.raw_data.drop_duplicates(subset=["title", "authors"], inplace=True)
        final_count = len(self.raw_data)
        logger.info(f"Removed {initial_count - final_count} duplicate records.")
        return self.raw_data

    def clean_authors(self):
        self.raw_data["authors"] = self.raw_data["authors"].apply(lambda x: ", ".join([author.strip() for author in x.split(",")]))
        logger.info("Cleaned author names.")
        return self.raw_data

    def process(self):
        self.remove_duplicates()
        self.clean_authors()
        logger.info("Data cleaning completed.")
        return self.raw_data

if __name__ == "__main__":
    sample_data = [
        {"title": "Reinforcement Learning Basics", "authors": "John Doe, Jane Smith", "abstract": "Introduction to RL."},
        {"title": "Reinforcement Learning Basics", "authors": "John Doe, Jane Smith", "abstract": "Introduction to RL."},
        {"title": "Advanced RL Techniques", "authors": "Alice Johnson, Bob Lee", "abstract": "Deep dive into RL."}
    ]

    cleaner = DataCleaner(sample_data)
    cleaned_data = cleaner.process()
    print(cleaned_data)
