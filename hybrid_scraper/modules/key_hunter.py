import re
import asyncio
import aiohttp
from typing import List, Dict, Any
from loguru import logger

class KeyHunter:
    def __init__(self):
        # Professional regex patterns for common services
        # Patterns are ordered and refined to minimize false positives
        self.patterns = {
            "Tavily AI": r"\btvly-[a-zA-Z0-9]{32}\b",
            "Google Gemini": r"\bAIza[0-9A-Za-z-_]{35}\b",
            "Claude": r"\bsk-ant-api03-[a-zA-Z0-9-_]{93}\b",
            "Grok": r"\bxai-[a-zA-Z0-9]{48}\b",
            "Slack Token": r"\bxox[baprs]-[0-9a-zA-Z]{10,48}\b",
            "AWS Access Key": r"\bAKIA[0-9A-Z]{16}\b",
            "GitHub Token": r"\bgh[pousr]_[a-zA-Z0-9]{36}\b",
            "Twilio SID": r"\bAC[a-z0-9]{32}\b",
            "Twilio Token": r"\b[a-f0-9]{32}\b",
            "Hunter.io": r"\b[a-zA-Z0-9]{40}\b",
            "Shodan": r"\b[a-zA-Z0-9]{32}\b",
            "FullContact": r"\b[a-zA-Z0-9]{16}\b",
            "Censys API": r"\b[a-zA-Z0-9]{32}\b",
            "BinaryEdge API": r"\b[a-zA-Z0-9]{32}\b",
            "GreyNoise API": r"\b[a-zA-Z0-9]{32}\b",
            "IBM X-Force API": r"\b[a-zA-Z0-9]{32}\b",
            "Generic Secret": r"(?:api_key|apikey|secret|token|auth_token)[\"']?\s*[:=]\s*[\"']?([a-zA-Z0-9-_]{16,64})[\"']?"
        }

    def hunt(self, content: str) -> List[Dict[str, str]]:
        """Scan content for potential API keys using regex patterns."""
        found_keys = []
        seen_keys = set()

        for service, pattern in self.patterns.items():
            matches = re.findall(pattern, content)
            for match in matches:
                # Handle capture groups in generic pattern
                if isinstance(match, tuple):
                    match = match[0]
                
                # Deduplicate and avoid overlaps (prefer specific patterns)
                if match not in seen_keys:
                    found_keys.append({"service": service, "key": match})
                    seen_keys.add(match)
        
        return found_keys

    async def validate_key(self, service: str, key: str) -> bool:
        """Asynchronously validate the discovered key."""
        if service == "Shodan":
            return await self._validate_shodan(key)
        
        # Default: just log the discovery if no validator is implemented
        return True

    async def _validate_shodan(self, key: str) -> bool:
        url = f"https://api.shodan.io/api-info?key={key}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as response:
                    if response.status == 200:
                        logger.success(f"VALID Shodan Key: {key}")
                        return True
                    else:
                        logger.debug(f"Invalid Shodan Key: {key}")
                        return False
        except Exception as e:
            logger.error(f"Shodan validation error: {e}")
            return False
