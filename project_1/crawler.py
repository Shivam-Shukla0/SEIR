
import sys
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


# simple hash banana
def makeHash(word):
    p = 53
    mod = 2 ** 64
    ans = 0

    for i in range(len(word)):
        ch = word[i]
        ans = ans + ord(ch) * (p ** i)

    ans = ans % mod
    return ans


# creating simhash function
def makeSimHash(wordCount):
    bits = []

    for i in range(64):
        bits.append(0)

    for word in wordCount:
        count = wordCount[word]
        h = makeHash(word)

        for i in range(64):
            bit = (h >> i) & 1
            if bit == 1:
                bits[i] = bits[i] + count
            else:
                bits[i] = bits[i] - count

    finalHash = 0
    for i in range(64):
        if bits[i] > 0:
            value = 1
            for j in range(i):
                value = value * 2
            finalHash = finalHash + value

    return finalHash


# common bits count
def countCommonBits(h1, h2):
    xorValue = h1 ^ h2
    binary = bin(xorValue)
    ones = binary.count("1")
    return 64 - ones


# website scrape karna
def scrapePage(url):

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

    # title printing
    if soup.title != None:
        print(soup.title.text.strip())

    # printing body text only removing script and style
    tags = soup.find_all(["script", "style"])
    for t in tags:
        t.decompose()

    bodyText = ""
    body = soup.find("body")
    if body != None:
        bodyText = body.text

        lines = bodyText.split("\n")
        for line in lines:
            line = line.strip()
            if line != "":
                print(line)

    # All links printing 
    links = soup.find_all("a")
    for a in links:
        link = a.get("href")
        if link != None:
            print(urljoin(url, link))

    # word frequency
    words = re.findall("[a-z0-9]+", bodyText.lower())

    wordCount = {}
    for w in words:
        if w in wordCount:
            wordCount[w] = wordCount[w] + 1
        else:
            wordCount[w] = 1

    # frequency print
    for w in sorted(wordCount, key=wordCount.get, reverse=True):
        print(w + ":", wordCount[w])

    # sample hash
    print("\n--- Word Hash Sample ---")
    count = 0
    for w in wordCount:
        print(w + ":", makeHash(w))
        count = count + 1
        if count == 5:
            break

    # printing simhash value
    simHashValue = makeSimHash(wordCount)
    print("\nSimhash:", simHashValue)

    return wordCount, simHashValue


# main
if len(sys.argv) < 3:
    print("Enter at least 2 URLs to compare")
else:
    freq1, hash1 = scrapePage(sys.argv[1])
    freq2, hash2 = scrapePage(sys.argv[2])

    common = countCommonBits(hash1, hash2)
    print("\nCommon bits between pages:", common, "/64")