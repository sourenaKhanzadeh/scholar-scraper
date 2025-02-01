Component	Language	Purpose
Scraper Engine	Python	Uses Playwright/Selenium to extract Google Scholar data. Handles CAPTCHAs & proxies.
Data Processing	Rust	Parses, cleans, and structures extracted data asynchronously.
API Server	Go	Exposes scraped data via REST API, connects with PostgreSQL.
Task Scheduler	Elixir	Manages periodic scraping jobs, retries, and concurrency.
Load Balancer	Go	Distributes scraping requests across multiple proxies.
AI-based CAPTCHA Solver	Python	Uses AI/ML to solve CAPTCHAs.
Data Analysis & NLP	Haskell	Processes extracted research data with NLP techniques.
Database	PostgreSQL	Stores scraped research data efficiently.