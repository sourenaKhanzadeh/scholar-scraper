from fastapi import FastAPI, HTTPException
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scraper.scholar_scraper import ScholarScraper

app = FastAPI()

@app.get("/search")
def search_scholar(query: str):
    scraper = ScholarScraper()
    results = scraper.search(query)

    if results.empty:
        raise HTTPException(status_code=404, detail="No results found.")

    return results.to_dict(orient="records")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)