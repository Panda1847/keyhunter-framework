import asyncio
import aiohttp
import random
import os
from typing import List, Optional
from loguru import logger

class ProxyManager:
    def __init__(self, use_proxies: bool = True):
        self.use_proxies = use_proxies
        self.proxies: List[str] = []
        self.active_proxy: Optional[str] = None
        self.request_count = 0
        self.max_requests_per_proxy = random.randint(5, 15)
        self.sources = [
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
            "https://raw.githubusercontent.com/jetkai/proxy-list/main/archive/http.txt",
            "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/http.txt",
            "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt"
        ]

    async def fetch_proxies(self) -> None:
        """Fetch fresh proxies from multiple public sources."""
        if not self.use_proxies:
            logger.info("Proxy usage is disabled.")
            return

        logger.info("Fetching fresh proxies from sources...")
        new_proxies = set()
        async with aiohttp.ClientSession() as session:
            for source in self.sources:
                try:
                    async with session.get(source, timeout=10) as response:
                        if response.status == 200:
                            text = await response.text()
                            lines = text.splitlines()
                            for line in lines:
                                if ":" in line and "." in line:
                                    new_proxies.add(line.strip())
                except Exception as e:
                    logger.debug(f"Error fetching from {source}: {e}")
        
        self.proxies = list(new_proxies)
        logger.info(f"Fetched {len(self.proxies)} potential proxies.")
        if self.proxies:
            await self.rotate_proxy()
        else:
            logger.warning("No proxies found, falling back to direct connection.")

    async def rotate_proxy(self) -> None:
        """Rotate to a new random proxy from the pool."""
        if not self.use_proxies or not self.proxies:
            self.active_proxy = None
            return

        self.active_proxy = random.choice(self.proxies)
        self.request_count = 0
        self.max_requests_per_proxy = random.randint(5, 15)
        logger.info(f"Rotated to new proxy: {self.active_proxy}")

    def get_proxy(self) -> Optional[str]:
        """Get the current active proxy URL."""
        if not self.use_proxies or not self.active_proxy:
            return None

        self.request_count += 1
        if self.request_count >= self.max_requests_per_proxy:
            logger.debug("Proxy request limit reached. Triggering rotation.")
            asyncio.create_task(self.rotate_proxy())
        
        return f"http://{self.active_proxy}"

    async def report_failure(self) -> None:
        """Report a failure with the current proxy and trigger rotation."""
        if self.active_proxy:
            logger.warning(f"Proxy {self.active_proxy} failed. Rotating...")
            if self.active_proxy in self.proxies:
                self.proxies.remove(self.active_proxy)
            await self.rotate_proxy()
