import re
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
            "Twilio": r"AC[a-z0-9]{32}",
            "Hunter.io": r"[a-zA-Z0-9]{40}",
            "Google Gemini": r"AIza[0-9A-Za-z-_]{35}",
            "Claude": r"sk-ant-api03-[a-zA-Z0-9-_]{93}",
            "Grok": r"xai-[a-zA-Z0-9]{48}",
            "Generic API Key": r"(?:api_key|apikey|secret|token|auth_token)[\"']?\s*[:=]\s*[\"']?([a-zA-Z0-9-_]{16,64})[\"']?"
        }

    def hunt(self, content):
        found_keys = []
        for service, pattern in self.patterns.items():
            matches = re.findall(pattern, content)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0]
                found_keys.append({"service": service, "key": match})
        
        if found_keys:
            logger.info(f"Found {len(found_keys)} potential API keys.")
        return found_keys

    def validate_key(self, service, key):
        # Placeholder for actual validation logic
        # In a real scenario, this would make an API call to the service's "whoami" or "usage" endpoint
        logger.info(f"Validating {service} key: {key}")
        # For now, we'll just assume it's valid for demonstration purposes
        return True
