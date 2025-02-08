#! /usr/bin/env python3
import os
from dotenv import load_dotenv

load_dotenv()

def load_config():
    return {
        "PROXY": os.getenv("PROXY", None),
        "TIMEOUT": int(os.getenv("TIMEOUT", 10)),
        "RETRIES": int(os.getenv("RETRIES", 3)),
        "DATA_DIR": os.getenv("DATA_DIR", "../shared/data/raw")
    }