# Usage Guide for KeyHunter Framework

This guide provides detailed instructions on how to effectively use the KeyHunter Framework for API key discovery. Ensure you have completed the [installation steps](INSTALL.md) before proceeding.

## Activating the Virtual Environment

Always activate the Python virtual environment before running KeyHunter to ensure all dependencies are correctly loaded:

```bash
source venv/bin/activate
```

## Basic Usage: Static Crawling

To perform a basic static crawl on one or more URLs, use the `main.py` script with the `--urls` argument. This mode uses `curl_cffi` for fast and efficient content retrieval without full browser rendering.

```bash
python3 main.py --urls https://example.com https://api.example.org/docs
```

Replace `https://example.com` and `https://api.example.org/docs` with your target URLs.

## Advanced Usage: Dynamic Crawling

For websites that heavily rely on JavaScript to render content (e.g., Single Page Applications), enable dynamic crawling using the `--dynamic` flag. This mode utilizes `nodriver` for headless browser automation, allowing KeyHunter to execute JavaScript and interact with dynamic elements.

```bash
python3 main.py --urls https://dynamic-app.com --dynamic
```

**Note**: Dynamic crawling is generally slower and more resource-intensive than static crawling due to the overhead of launching a headless browser.

## Interpreting Results

KeyHunter logs its findings directly to the console using `loguru`. Successful API key discoveries will be highlighted with `SUCCESS` messages, indicating the service and the discovered key.

```
[INFO] Initializing Hybrid Scraper...
[INFO] Fetching fresh proxies from sources...
[INFO] Fetched 150 potential proxies.
[INFO] Rotated to new proxy: 192.168.1.1:8080
[INFO] Starting crawl on 1 URLs...
[INFO] Crawling static page: https://example.com using proxy: http://192.168.1.1:8080
[SUCCESS] Found valid Tavily AI key: tvly-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
[INFO] Crawl completed.
```

### KeyHunter Output Fields

| Field | Description |
|---|---|
| `service` | The identified service associated with the API key (e.g., Tavily AI, Shodan, Google Gemini). |
| `key` | The discovered API key string. |

## Proxy Management

KeyHunter automatically manages proxy rotation to enhance stealth and bypass rate limiting. If a proxy fails or reaches its request limit, the system will automatically rotate to a new one. You do not need to configure proxies manually.

## Customizing API Key Patterns

To extend KeyHunter's capabilities or refine existing patterns, you can modify the `patterns` dictionary within `modules/key_hunter.py`. Each entry consists of a service name and a regular expression.

**Example**: Adding a new service pattern

```python
# modules/key_hunter.py

class KeyHunter:
    def __init__(self):
        self.patterns = {
            # ... existing patterns ...
            "NewService API": r"ns-[a-zA-Z0-9]{40}",
        }
```

After modifying, save the file and run KeyHunter as usual. Your new patterns will be automatically included in the scanning process.

## Troubleshooting

Refer to the [INSTALL.md](INSTALL.md) for common installation issues. For usage-specific problems, consider:

*   **Network Connectivity**: Ensure your machine has internet access, especially for proxy fetching and target website access.
*   **Target Website Changes**: Websites frequently update their structure. If KeyHunter fails to find keys on a previously working target, the website's HTML/JS structure might have changed, requiring pattern adjustments or dynamic crawling.
*   **Log Analysis**: Review the `loguru` output for `ERROR` or `WARNING` messages, which can provide clues about issues during crawling or key discovery.

For further assistance, please open an issue on the [KeyHunter Framework GitHub Issues](https://github.com/Panda1847/keyhunter-framework/issues) page.
