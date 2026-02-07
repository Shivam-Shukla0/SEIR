import sys
import requests
from bs4 import BeautifulSoup


def fetch_page(url: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    return response.text


def normalize_url(url: str):
    if not url.startswith(("https://", "http://")):
        return "https://" + url
    return url


def extract_text_and_links(html: str):
    soup = BeautifulSoup(html, "html.parser")

    title_text = ""
    if soup.title and soup.title.text:
        title_text = soup.title.text.strip()

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    body = soup.body if soup.body else soup
    body_text = body.get_text(separator="\n", strip=True)

    links = []
    for link in soup.find_all("a", href=True):
        links.append(link["href"])

    return title_text, body_text, links


def main():
    if len(sys.argv) != 2:
        print("Usage: python crawler.py <URL>")
        return 1

    url = normalize_url(sys.argv[1].strip())
    html = fetch_page(url)
    title_text, body_text, links = extract_text_and_links(html)

    print("=== TITLE ===")
    print(title_text)
    print("=== BODY ===")
    print(body_text)
    print("=== LINKS ===")
    for link in links:
        print(link)

    return 0
if __name__ == "__main__":
    raise SystemExit(main())
