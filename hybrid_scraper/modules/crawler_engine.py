import asyncio
import re
from typing import Set, List, Optional
from urllib.parse import urljoin, urlparse
from curl_cffi import requests
import nodriver as nd
from loguru import logger

try:
    from .proxy_manager import ProxyManager
    from .key_hunter import KeyHunter
except ImportError:
    from hybrid_scraper.modules.proxy_manager import ProxyManager
    from hybrid_scraper.modules.key_hunter import KeyHunter

class CrawlerEngine:
    def __init__(self, proxy_manager: ProxyManager, key_hunter: KeyHunter, max_depth: int = 1, concurrency: int = 5):
        self.proxy_manager = proxy_manager
        self.key_hunter = key_hunter
        self.max_depth = max_depth
        self.concurrency = concurrency
        self.visited_urls: Set[str] = set()
        self.queue: asyncio.Queue = asyncio.Queue()
        self.semaphore = asyncio.Semaphore(concurrency)

    def is_valid_url(self, url: str, base_domain: str) -> bool:
        """Check if the URL is valid and belongs to the same domain."""
        parsed = urlparse(url)
        return bool(parsed.netloc) and parsed.netloc == base_domain

    def extract_links(self, html: str, base_url: str) -> List[str]:
        """Extract all absolute links from HTML content."""
        links = []
        pattern = r'href=["\'](https?://[^"\']+|/[^"\']+)["\']'
        matches = re.findall(pattern, html)
        
        base_domain = urlparse(base_url).netloc
        for match in matches:
            full_url = urljoin(base_url, match)
            if self.is_valid_url(full_url, base_domain):
                links.append(full_url)
        return links

    async def crawl_static(self, url: str, depth: int) -> None:
        """Perform static crawling using curl_cffi."""
        async with self.semaphore:
            if url in self.visited_urls or depth > self.max_depth:
                return
            self.visited_urls.add(url)
            
            proxy = self.proxy_manager.get_proxy()
            logger.info(f"[Depth {depth}] Crawling static: {url}")
            
            try:
                # Use run_in_executor for the blocking requests call
                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(
                    None,
                    lambda: requests.get(
                        url,
                        impersonate="chrome131",
                        proxies={"http": proxy, "https": proxy} if proxy else None,
                        timeout=15,
                        verify=False
                    )
                )
                
                if response.status_code == 200:
                    content = response.text
                    found_keys = self.key_hunter.hunt(content)
                    for key_info in found_keys:
                        logger.success(f"Found {key_info['service']} key on {url}: {key_info['key']}")
                        asyncio.create_task(self.key_hunter.validate_key(key_info['service'], key_info['key']))
                    
                    if depth < self.max_depth:
                        new_links = self.extract_links(content, url)
                        for link in new_links:
                            await self.queue.put((link, depth + 1))
                else:
                    logger.warning(f"Failed {url} (Status: {response.status_code})")
                    if response.status_code in [403, 429]:
                        await self.proxy_manager.report_failure()
            except Exception as e:
                logger.error(f"Error crawling {url}: {e}")
                await self.proxy_manager.report_failure()

    async def crawl_dynamic(self, url: str, depth: int) -> None:
        """Perform dynamic crawling using nodriver."""
        async with self.semaphore:
            if url in self.visited_urls or depth > self.max_depth:
                return
            self.visited_urls.add(url)
            
            proxy = self.proxy_manager.get_proxy()
            logger.info(f"[Depth {depth}] Crawling dynamic: {url}")
            
            browser = None
            try:
                browser = await nd.start(
                    browser_args=[f"--proxy-server={proxy}"] if proxy else []
                )
                page = await browser.get(url)
                await page.sleep(5)
                
                content = await page.get_content()
                found_keys = self.key_hunter.hunt(content)
                for key_info in found_keys:
                    logger.success(f"Found {key_info['service']} key on {url}: {key_info['key']}")
                    asyncio.create_task(self.key_hunter.validate_key(key_info['service'], key_info['key']))
                
                if depth < self.max_depth:
                    new_links = self.extract_links(content, url)
                    for link in new_links:
                        await self.queue.put((link, depth + 1))
            except Exception as e:
                logger.error(f"Error dynamic crawling {url}: {e}")
                await self.proxy_manager.report_failure()
            finally:
                if browser:
                    await browser.stop()

    async def worker(self, is_dynamic: bool) -> None:
        """Worker task to process the crawl queue."""
        while True:
            try:
                url, depth = await self.queue.get()
                if is_dynamic:
                    await self.crawl_dynamic(url, depth)
                else:
                    await self.crawl_static(url, depth)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Worker error: {e}")
            finally:
                self.queue.task_done()

    async def run(self, start_urls: List[str], is_dynamic: bool = False) -> None:
        """Initialize and run the crawler workers."""
        for url in start_urls:
            await self.queue.put((url, 1))
        
        workers = []
        for _ in range(self.concurrency):
            worker = asyncio.create_task(self.worker(is_dynamic))
            workers.append(worker)
        
        await self.queue.join()
        
        for worker in workers:
            worker.cancel()
        
        await asyncio.gather(*workers, return_exceptions=True)
