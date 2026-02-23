import sys
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def scrape_page(url):

    if url.startswith("http") == False:
        url = "https://" + url

    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    except:
        print("website is not opening")
        return {}, 0

    if response.status_code != 200:
        print("page is not loading")
        return {}, 0

    soup = BeautifulSoup(response.text, "html.parser")

    if soup.title != None:
        print(soup.title.text.strip())

    tags = soup.find_all(["script", "style"])
    for t in tags:
        t.decompose()

    texts_in_body = ""
    body = soup.find("body")
    if body != None:
        texts_in_body = body.text

        lines = texts_in_body.split("\n")
        for line in lines:
            line = line.strip()
            if line != "":
                print(line)

    links_in_page = soup.find_all("a")
    for a in links_in_page:
        link = a.get("href")
        if link != None:
            print(urljoin(url, link))

    words_in_page = re.findall("[a-z0-9]+", texts_in_body.lower())

    dictionary_of_words = {}
    for w in words_in_page:
        if w in dictionary_of_words:
            dictionary_of_words[w] = dictionary_of_words[w] + 1
        else:
            dictionary_of_words[w] = 1

    for w in sorted(dictionary_of_words, key=dictionary_of_words.get, reverse=True):
        print(w + ":", dictionary_of_words[w])

    sim_hash_value = make_sim_hash(dictionary_of_words)
    print("\nSimhash:", sim_hash_value)

    return dictionary_of_words, sim_hash_value


def make_hash(word):
    p = 53
    rem = 2 ** 64
    answer = 0

    for i in range(len(word)):
        character = word[i]
        answer = answer + ord(character) * (p ** i)

    answer = answer % rem
    return answer


def make_sim_hash(dictionary_of_words):
    bits = []

    for i in range(64):
        bits.append(0)

    for word in dictionary_of_words:
        count = dictionary_of_words[word]
        h = make_hash(word)

        for i in range(64):
            bit = (h >> i) & 1
            if bit == 1:
                bits[i] = bits[i] + count
            else:
                bits[i] = bits[i] - count

    final_hash_value = 0
    for i in range(64):
        if bits[i] > 0:
            value = 1
            for j in range(i):
                value = value * 2
            final_hash_value = final_hash_value + value

    return final_hash_value


def counting_common_bits(h1, h2):
    final_xorValue = h1 ^ h2
    binary_of_xor = bin(final_xorValue)
    common_ones = binary_of_xor.count("1")
    return 64 - common_ones


if len(sys.argv) < 3:
    print("Enter at least 2 URLs to compare")
else:
    freq1, hash1 = scrape_page(sys.argv[1])
    freq2, hash2 = scrape_page(sys.argv[2])

    common = counting_common_bits(hash1, hash2)
    print("\nCommon bits between pages:", common, "/64")