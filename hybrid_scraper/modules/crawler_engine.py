import asyncio
import aiohttp
from curl_cffi import requests
import nodriver as nd
from loguru import logger
from .proxy_manager import ProxyManager
from .key_hunter import KeyHunter

class CrawlerEngine:
    def __init__(self, proxy_manager: ProxyManager, key_hunter: KeyHunter):
        self.proxy_manager = proxy_manager
        self.key_hunter = key_hunter
        self.visited_urls = set()
        self.queue = asyncio.Queue()

    async def crawl_static(self, url):
        if url in self.visited_urls:
            return
        self.visited_urls.add(url)
        
        proxy = self.proxy_manager.get_proxy()
        logger.info(f"Crawling static page: {url} using proxy: {proxy}")
        
        try:
            response = requests.get(
                url,
                impersonate="chrome131",
                proxies={"http": proxy, "https": proxy} if proxy else None,
                timeout=15
            )
            if response.status_code == 200:
                content = response.text
                found_keys = self.key_hunter.hunt(content)
                for key_info in found_keys:
                    logger.success(f"Discovered potential {key_info['service']} key: {key_info['key']}")
                    # Perform asynchronous validation
                    asyncio.create_task(self.key_hunter.validate_key(key_info['service'], key_info['key']))
            else:
                logger.warning(f"Failed to crawl {url}. Status code: {response.status_code}")
                if response.status_code in [403, 429]:
                    await self.proxy_manager.report_failure()
        except Exception as e:
            logger.error(f"Error crawling {url}: {e}")
            await self.proxy_manager.report_failure()

    async def crawl_dynamic(self, url):
        if url in self.visited_urls:
            return
        self.visited_urls.add(url)
        
        proxy = self.proxy_manager.get_proxy()
        logger.info(f"Crawling dynamic page: {url} using proxy: {proxy}")
        
        try:
            browser = await nd.start(
                browser_args=[f"--proxy-server={proxy}"] if proxy else []
            )
            page = await browser.get(url)
            await page.sleep(5)  # Wait for JS to load
            
            content = await page.get_content()
            found_keys = self.key_hunter.hunt(content)
            for key_info in found_keys:
                logger.success(f"Discovered potential {key_info['service']} key: {key_info['key']}")
                # Perform asynchronous validation
                asyncio.create_task(self.key_hunter.validate_key(key_info['service'], key_info['key']))
            
            await browser.stop()
        except Exception as e:
            logger.error(f"Error crawling dynamic page {url}: {e}")
            await self.proxy_manager.report_failure()

    async def run(self, start_urls):
        for url in start_urls:
            await self.queue.put(url)
        
        while not self.queue.empty():
            url = await self.queue.get()
            # For demonstration, we'll alternate between static and dynamic crawling
            if "dynamic" in url:
                await self.crawl_dynamic(url)
            else:
                await self.crawl_static(url)
            self.queue.task_done()
