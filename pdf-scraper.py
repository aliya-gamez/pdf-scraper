import re
import os
from urllib.parse import urlparse, unquote
from io import BytesIO as bi

import requests as rq
import pandas as pd
from bs4 import BeautifulSoup as bs
from bs4 import SoupStrainer as ss
from pypdf import PdfReader as pr

DOMAIN = "career.fsu.edu"
GET_PDF_TITLES = False #this takes a while, a long while, so im setting it false unless needed

def loadPageLinks(url):
    r = rq.get(url)
    if r.status_code != 200:
        print(f'Failed to Load: {url}')
        return
    print(f'Scraping: {url}')
    content = bs(r.text,'html.parser',parse_only=ss('a',href=internalFilter))
    for c in content:
        c.clear()
    return content

def pdfFilter(href):
    p = re.compile(rf"(?:{re.escape(DOMAIN)}|/).+\.pdf$")
    return href and p.search(href)

def internalFilter(href):
    p = re.compile(rf"(?:{re.escape(DOMAIN)}|^/)")
    return href and p.search(href)

def getPdfFilename(href):
    path = urlparse(href).path
    filename = os.path.basename(path)
    filename = unquote(filename)
    return filename

def getPdfTitle(href):
    if GET_PDF_TITLES == False: return 'Titles Scraping Disabled'
    r = rq.get(href)
    file = bi(r.content)
    reader = pr(file)
    return reader.metadata.title;

def convertRelativeUrl(href):
    if href.startswith("/"): href = "https://" + DOMAIN + href
    return href

def main():
    rows = []
    #content = loadPageLinks("https://"+DOMAIN)
    content = loadPageLinks("https://career.fsu.edu/resources/career-guides")
    for c in content:
        # grab HREF from link list (c) and convert to actual url for 
        href = convertRelativeUrl(c.get('href'));
        if(href) and pdfFilter(href): 
            columns = {
                "url": href,
                "file name": getPdfFilename(href),
                "title": getPdfTitle(href)
            }
            rows.append(columns)

    # Output to CSV
    df = pd.DataFrame(rows)
    df.to_csv("pdf_list.csv", index=False, encoding="utf-8-sig")

if __name__ == "__main__":
    main()