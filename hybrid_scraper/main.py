import asyncio
import argparse
from loguru import logger
from modules.proxy_manager import ProxyManager
from modules.key_hunter import KeyHunter
from modules.crawler_engine import CrawlerEngine

async def main():
    parser = argparse.ArgumentParser(description="KeyHunter Framework: Advanced API Key Discovery & Intelligence")
    parser.add_argument("--urls", nargs="+", help="Starting URLs for crawling", required=True)
    parser.add_argument("--dynamic", action="store_true", help="Enable dynamic crawling for all URLs")
    parser.add_argument("--depth", type=int, default=1, help="Crawl depth (default: 1)")
    args = parser.parse_args()

    logger.info("Initializing KeyHunter Framework...")
    
    proxy_manager = ProxyManager()
    await proxy_manager.fetch_proxies()
    
    key_hunter = KeyHunter()
    crawler_engine = CrawlerEngine(proxy_manager, key_hunter)
    
    logger.info(f"Starting crawl on {len(args.urls)} URLs with depth {args.depth}...")
    
    # Run crawling and validation concurrently
    if args.dynamic:
        tasks = [crawler_engine.crawl_dynamic(url) for url in args.urls]
        await asyncio.gather(*tasks)
    else:
        await crawler_engine.run(args.urls)
    
    logger.info("Crawl completed.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("KeyHunter interrupted by user.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
