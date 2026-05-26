import sys
import os

# Add the current directory to sys.path to allow importing from hybrid_scraper
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'hybrid_scraper')))

from hybrid_scraper.main import main
import asyncio

if __name__ == "__main__":
    asyncio.run(main())
