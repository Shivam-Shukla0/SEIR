import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def scrape_page(website_link):
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
    elements = filter_html_page(["script", "style"])
    while len(elements) > 0:
        elements[0].decompose()
        elements = filter_html_page(["script", "style"])
    body_tag_content = filter_html_page.find("body")
    if body_tag_content:
        text = body_tag_content.get_text()
        lines = text.split("\n")
        i = 0
        while i < len(lines):
            cleaned_content = lines[i].strip()
            if cleaned_content:
                print(cleaned_content)
            i += 1
    for anchor_tag_in_page in filter_html_page.find_all("a", href=True):
        print(urljoin(website_link, anchor_tag_in_page["href"]))

if __name__ == "__main__":
    if len(sys.argv) == 2:
        scrape_page(sys.argv[1])