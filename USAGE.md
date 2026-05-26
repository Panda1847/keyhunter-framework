# Usage Guide: KeyHunter Framework

## Basic Command
The framework is designed to be simple yet powerful. The primary entry point is the root-level `main.py`.

```bash
python3 main.py --urls https://target.com
```

## Advanced Crawling
To explore deeper into a domain, use the `--depth` flag. KeyHunter will extract internal links and follow them recursively.

```bash
python3 main.py --urls https://target.com --depth 3
```

## Dynamic Content
For Single Page Applications (SPAs) or sites that require JavaScript to render, use the `--dynamic` flag.

```bash
python3 main.py --urls https://spa-target.com --dynamic
```

## Concurrency and Performance
You can adjust the number of concurrent crawl tasks to speed up the process.

```bash
python3 main.py --urls https://target.com --concurrency 10
```

## Troubleshooting Proxies
If you are experiencing network issues or want to run a scan from your own IP, use `--no-proxy`.

```bash
python3 main.py --urls https://target.com --no-proxy
```

## Example Output
KeyHunter uses professional logging to display results in real-time:

```text
2026-05-26 10:00:00 | INFO     | Initializing KeyHunter Framework...
2026-05-26 10:00:01 | INFO     | [Depth 1] Crawling static: https://target.com
2026-05-26 10:00:02 | SUCCESS  | Found Shodan key on https://target.com: abc...123
2026-05-26 10:00:02 | SUCCESS  | VALID Shodan Key: abc...123
```
