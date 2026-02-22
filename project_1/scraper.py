import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def scrape(url):
    if not url.startswith("http"):
        url = "https://" + url

    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    except Exception as e:
        print("something went wrong:", e)
        return

    if r.status_code != 200:
        print("page not loaded, status:", r.status_code)
        return

    soup = BeautifulSoup(r.text, "html.parser")

    # print title
    title = soup.title
    if title:
        print(title.text.strip())

    # remove script and style before getting text
    for tag in soup(["script", "style"]):
        tag.decompose()

    # body text
    body = soup.find("body")
    if body:
        text = body.get_text(separator="\n", strip=True)
        for line in text.split("\n"):
            if line.strip():
                print(line.strip())

    # all links
    for a in soup.find_all("a"):
        href = a.get("href")
        if href:
            print(urljoin(url, href))


if len(sys.argv) < 2:
    print("give a url please")
else:
    scrape(sys.argv[1])