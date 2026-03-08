import re
import asyncio
import aiohttp
from loguru import logger

class KeyHunter:
    def __init__(self):
        self.patterns = {
            "Tavily AI": r"tvly-[a-zA-Z0-9]{32}",
            "Shodan": r"[a-zA-Z0-9]{32}",
            "FullContact": r"[a-zA-Z0-9]{16}",
            "Censys API": r"[a-zA-Z0-9]{32}",
            "BinaryEdge API": r"[a-zA-Z0-9]{32}",
            "GreyNoise API": r"[a-zA-Z0-9]{32}",
            "IBM X-Force API": r"[a-zA-Z0-9]{32}",
            "Twilio SID": r"AC[a-z0-9]{32}",
            "Twilio Token": r"[a-f0-9]{32}",
            "Hunter.io": r"[a-zA-Z0-9]{40}",
            "Google Gemini": r"AIza[0-9A-Za-z-_]{35}",
            "Claude": r"sk-ant-api03-[a-zA-Z0-9-_]{93}",
            "Grok": r"xai-[a-zA-Z0-9]{48}",
            "Slack Token": r"xox[baprs]-[0-9a-zA-Z]{10,48}",
            "AWS Access Key": r"AKIA[0-9A-Z]{16}",
            "GitHub Token": r"gh[pousr]_[a-zA-Z0-9]{36}",
            "Generic API Key": r"(?:api_key|apikey|secret|token|auth_token)[\"']?\s*[:=]\s*[\"']?([a-zA-Z0-9-_]{16,64})[\"']?"
        }

    def hunt(self, content):
        found_keys = []
        for service, pattern in self.patterns.items():
            matches = re.findall(pattern, content)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0]
                # Avoid duplicates
                if not any(k['key'] == match for k in found_keys):
                    found_keys.append({"service": service, "key": match})
        
        if found_keys:
            logger.info(f"Found {len(found_keys)} potential API keys.")
        return found_keys

    async def validate_key(self, service, key):
        """
        Asynchronously validate the discovered key.
        Currently implements validation for Shodan as an example.
        """
        logger.info(f"Validating {service} key: {key[:8]}...")
        
        if service == "Shodan":
            url = f"https://api.shodan.io/api-info?key={key}"
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, timeout=10) as response:
                        if response.status == 200:
                            logger.success(f"Confirmed VALID Shodan key: {key}")
                            return True
                        else:
                            logger.warning(f"Invalid Shodan key (Status: {response.status})")
                            return False
            except Exception as e:
                logger.error(f"Error validating Shodan key: {e}")
                return False
        
        # Default behavior for other services (placeholder)
        # In production, add validation logic for each service here.
        return True
