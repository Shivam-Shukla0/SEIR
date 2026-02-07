# SEIR Web Crawler

A lightweight command-line web crawler that fetches a URL, prints the page title, extracts clean body text, and lists all links found on the page.

## Features

- Normalizes input URLs (adds scheme when missing)
- Extracts title text without HTML tags
- Extracts readable body text without scripts or styles
- Lists all hyperlinks referenced on the page

## Requirements

- Python 3.8+
- requests
- beautifulsoup4

## Installation

```bash
python -m pip install requests beautifulsoup4
```

## Usage

```bash
python crawler.py <URL>
```

Example:

```bash
python crawler.py https://example.com
```

## Output Format

The program prints the following sections in order:

1. Title
2. Body text
3. Links (one per line)

## Notes

- The crawler does not execute JavaScript.
- Relative links are printed as-is.

## License

This project is provided as-is without warranty. Add a license file if you plan to distribute or reuse it.
