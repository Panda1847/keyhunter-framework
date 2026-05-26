import asyncio
import argparse
import sys
from typing import List
from loguru import logger

# Fix imports for root-level execution
try:
    from modules.proxy_manager import ProxyManager
    from modules.key_hunter import KeyHunter
    from modules.crawler_engine import CrawlerEngine
except ImportError:
    from hybrid_scraper.modules.proxy_manager import ProxyManager
    from hybrid_scraper.modules.key_hunter import KeyHunter
    from hybrid_scraper.modules.crawler_engine import CrawlerEngine

async def main() -> None:
    """
    Main entry point for the KeyHunter Framework.
    Parses arguments and initializes the crawler engine.
    """
    parser = argparse.ArgumentParser(
        description="KeyHunter Framework: Advanced API Key Discovery & Intelligence",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--urls", nargs="+", help="Starting URLs for crawling", required=True)
    parser.add_argument("--dynamic", action="store_true", help="Enable dynamic crawling for all URLs")
    parser.add_argument("--depth", type=int, default=1, help="Crawl depth")
    parser.add_argument("--concurrency", type=int, default=5, help="Number of concurrent crawler tasks")
    parser.add_argument("--no-proxy", action="store_true", help="Disable proxy rotation")
    
    args = parser.parse_args()

    # Configure logger
    logger.remove()
    logger.add(
        sys.stderr, 
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>",
        level="INFO"
    )

    logger.info("Initializing KeyHunter Framework...")
    
    try:
        proxy_manager = ProxyManager(use_proxies=not args.no_proxy)
        await proxy_manager.fetch_proxies()
        
        key_hunter = KeyHunter()
        crawler_engine = CrawlerEngine(
            proxy_manager=proxy_manager, 
            key_hunter=key_hunter,
            max_depth=args.depth,
            concurrency=args.concurrency
        )
        
        logger.info(f"Starting crawl on {len(args.urls)} URLs with depth {args.depth}...")
        
        await crawler_engine.run(args.urls, is_dynamic=args.dynamic)
        
        logger.info("Crawl completed successfully.")
    except Exception as e:
        logger.error(f"Framework initialization failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.warning("KeyHunter interrupted by user. Shutting down...")
    except Exception as e:
        logger.critical(f"Unhandled exception: {e}")
