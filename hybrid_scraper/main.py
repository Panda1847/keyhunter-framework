import asyncio
import argparse
from loguru import logger
from modules.proxy_manager import ProxyManager
from modules.key_hunter import KeyHunter
from modules.crawler_engine import CrawlerEngine

async def main():
    parser = argparse.ArgumentParser(description="Hybrid Web Scraper/Crawler for API Key Discovery")
    parser.add_argument("--urls", nargs="+", help="Starting URLs for crawling", required=True)
    parser.add_argument("--dynamic", action="store_true", help="Enable dynamic crawling for all URLs")
    args = parser.parse_args()

    logger.info("Initializing Hybrid Scraper...")
    
    proxy_manager = ProxyManager()
    await proxy_manager.fetch_proxies()
    
    key_hunter = KeyHunter()
    crawler_engine = CrawlerEngine(proxy_manager, key_hunter)
    
    logger.info(f"Starting crawl on {len(args.urls)} URLs...")
    
    if args.dynamic:
        for url in args.urls:
            await crawler_engine.crawl_dynamic(url)
    else:
        await crawler_engine.run(args.urls)
    
    logger.info("Crawl completed.")

if __name__ == "__main__":
    asyncio.run(main())
