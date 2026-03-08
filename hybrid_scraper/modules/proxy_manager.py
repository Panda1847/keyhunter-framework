import asyncio
import aiohttp
import random
from loguru import logger

class ProxyManager:
    def __init__(self):
        self.proxies = []
        self.active_proxy = None
        self.request_count = 0
        self.max_requests_per_proxy = random.randint(5, 15)
        self.sources = [
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
            "https://raw.githubusercontent.com/jetkai/proxy-list/main/archive/http.txt",
            "https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/http.txt",
            "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt"
        ]

    async def fetch_proxies(self):
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
                                if ":" in line:
                                    new_proxies.add(line.strip())
                except Exception as e:
                    logger.error(f"Error fetching from {source}: {e}")
        
        self.proxies = list(new_proxies)
        logger.info(f"Fetched {len(self.proxies)} potential proxies.")
        if self.proxies:
            await self.rotate_proxy()

    async def rotate_proxy(self):
        if not self.proxies:
            await self.fetch_proxies()
        
        if self.proxies:
            self.active_proxy = random.choice(self.proxies)
            self.request_count = 0
            self.max_requests_per_proxy = random.randint(5, 15)
            logger.info(f"Rotated to new proxy: {self.active_proxy}")
        else:
            logger.warning("No proxies available to rotate.")

    def get_proxy(self):
        self.request_count += 1
        if self.request_count >= self.max_requests_per_proxy:
            logger.info("Proxy request limit reached. Triggering pre-emptive rotation.")
            asyncio.create_task(self.rotate_proxy())
        
        if self.active_proxy:
            return f"http://{self.active_proxy}"
        return None

    async def report_failure(self):
        logger.warning(f"Proxy {self.active_proxy} failed. Rotating immediately.")
        await self.rotate_proxy()
