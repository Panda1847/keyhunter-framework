# Hybrid Web Scraper/Crawler for API Key Discovery

## Overview
This is a professional-grade hybrid web scraper and crawler designed for Kali Linux. It incorporates advanced anti-detection features and intelligent proxy rotation to discover and validate API keys for various OSINT, AI, and telecom intelligence platforms.

## Features
*   **Anti-Detection Engine**: Uses `curl_cffi` for TLS fingerprint spoofing and `nodriver` for CDP-free browser automation.
*   **Intelligent Proxy Manager**: Fetches fresh proxies from multiple sources and rotates them pre-emptively to avoid detection.
*   **Hybrid Crawler**: Supports both static and dynamic crawling for comprehensive coverage.
*   **API Key Hunter**: Scans content for potential API keys using a library of regex patterns for 20+ services.
*   **Asynchronous Validation**: Validates discovered keys asynchronously to maintain high performance.

## Supported Services
*   Tavily AI
*   Shodan
*   FullContact
*   Censys API
*   BinaryEdge API
*   GreyNoise API
*   IBM X-Force API
*   Twilio
*   Hunter.io
*   Google Gemini
*   Claude
*   Grok
*   ...and more!

## Installation
1.  Clone the repository or download the source code.
2.  Run the installer script:
    ```bash
    chmod +x install.sh
    ./install.sh
    ```

## Usage
1.  Activate the virtual environment:
    ```bash
    source venv/bin/activate
    ```
2.  Run the scraper:
    ```bash
    python3 main.py --urls <url1> <url2> ...
    ```
    To enable dynamic crawling for all URLs:
    ```bash
    python3 main.py --urls <url1> <url2> ... --dynamic
    ```

## Disclaimer
This tool is for educational and authorized security testing purposes only. Unauthorized use of this tool against targets without permission is illegal and unethical.
