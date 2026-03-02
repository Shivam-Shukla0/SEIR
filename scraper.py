import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def scrape(website_link):
    if not website_link.startswith("http") and not website_link.startswith("https"):
        website_link = "https://" + website_link

    try:
        r_made = requests.get(website_link, headers={"User-Agent": "Mozilla/5.0"})
    except:
        return

    if r_made.status_code != 200:
        return

    filter_html_page = BeautifulSoup(r_made.text, "html.parser")

    if filter_html_page.title and filter_html_page.title.string:
        print(filter_html_page.title.string.strip())
    else:
        print("")

    for tag in filter_html_page(["script", "style"]):
        tag.decompose()

    body_tag_content = filter_html_page.find("body")
    if body_tag_content:
        text = body_tag_content.get_text()
        for line in text.split("\n"):
            clean = line.strip()
            if clean:
                print(clean)

    for anchor_tag_in_page in filter_html_page.find_all("a", href=True):
        print(urljoin(website_link, anchor_tag_in_page["href"]))


if __name__ == "__main__":
    if len(sys.argv) == 2:
        scrape(sys.argv[1])
