import re
import os
from urllib.parse import urlparse,unquote,urljoin
from io import BytesIO as bi
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
from bs4 import SoupStrainer as ss
from pypdf import PdfReader as pr
from rich import print
from rich.console import Console
from rich.table import Table

DOMAIN = 'uhs.fsu.edu' # format: no https or www
GET_PDF_TITLES = False
CHECK_ACCESSIBLITY = False
PRINT_LENGTH = 75
SKIP_URL_STRINGS = [ 
    '/sites/',
    '/files/',
    '/blueprint/',
    '/seminole-success-stories/'
]

crawled_pages = set()
found_pdfs = set()
s = requests.Session() # session object for crawling

# 10 skipFilter:
def skipFilter(href):
    if any(keyword in href for keyword in SKIP_URL_STRINGS):
        print(f'[yellow]Skipped:[/yellow] {href[:PRINT_LENGTH]}')
        return False
    return True

# 9 getPdfTitle:
def getPdfTitle(href,name):
    if GET_PDF_TITLES == False: return None
    try:
        r = s.get(href)
        file = bi(r.content)
        reader = pr(file)
        return reader.metadata.title
    except: return None

# 8 getIMCEPath:
def getIMCEPath(href):
    path = urlparse(href).path
    if 'upcbnu746/files/' in path: return path.split('upcbnu746/files/')[1]
    elif '/files/' in path: return path.split('/files/')[1]
    return '-'

# 7 getPdfFilename:
def getPdfFilename(href):
    path = urlparse(href).path
    filename = os.path.basename(path)
    filename = unquote(filename)
    return filename

# 6 pdfFilter:
def pdfFilter(href):
    p = re.compile(rf'(?:{re.escape(DOMAIN)}|/).+\.pdf$')
    return href and p.search(href)

# 5 normalizeUrl:
def normalizeUrl(href):
    if href.startswith('/'): href = 'https://' + DOMAIN + href
    elif href.startswith('http://www.'): href = 'https://' + href.split('http://www.')[1]
    elif href.startswith('http://'): href = 'https://' + href.split('http://')[1]
    if href.endswith('/'): href = href[:-1]
    return href

# 4 interalFilter:
def internalFilter(href):
    p = re.compile(rf'(?:{re.escape(DOMAIN)}|^/)')
    return href and p.search(href)

# 3 loadPage:
def loadPage(url):
    if url in crawled_pages: return None
    crawled_pages.add(url)
    try: r = s.get(url,timeout=10)
    except: return None
    if r.status_code != 200:
        print(f'[red]Failed: [/red] {url[:PRINT_LENGTH]}')
        return None
    print(f'[cyan]Crawling:[/cyan] {url[:PRINT_LENGTH]}')
    return bs(r.text,'html.parser',parse_only=ss('a',href=internalFilter))

# 2 crawl:
def crawl(url,rows):
    links = loadPage(url) # sets links as BeautifulSoup object, else return
    if links is None: return 
    for link in links: # iterate through obj as element tags
        href = link.get('href')
        if not href: continue
        full_url = normalizeUrl(href) # return https:// version of link if relative

        if pdfFilter(full_url):
            if full_url in found_pdfs: continue
            found_pdfs.add(full_url)
            filename = getPdfFilename(full_url)
            imce = getIMCEPath(full_url)
            title = getPdfTitle(full_url,filename)
            columns = {
                "page_found_on":url,
                "pdf_url":full_url,
                "file_name":filename,
                "imce_path":imce
            }
            if GET_PDF_TITLES: columns['title'] = title
            rows.append(columns)
        elif internalFilter(full_url):
            if not skipFilter(full_url): continue
            if full_url not in crawled_pages:
                crawl(full_url,rows)

# 1 main:
def main():
    # variables
    rows = []
    domain = 'https://' + DOMAIN
    # code start
    crawl(domain,rows) # crawl
    # write to output folder
    directory = f'output/{DOMAIN}'
    if not os.path.exists(directory): os.makedirs(directory)
    df = pd.DataFrame(rows)
    df.to_csv(directory+"/pdf_list.csv",index=False,encoding="utf-8-sig")
    summary1 = df.groupby("page_found_on").size().reset_index(name="pdf_count")
    summary1.to_csv(directory+"/pdf_list_summary1.csv",index=False)
    summary2 = (
        df.groupby(["pdf_url","file_name","imce_path"])
        .agg(
            pages_found_on=("page_found_on",
                lambda x: "\n".join(dict.fromkeys(x))
            ),
            page_count=("page_found_on","nunique")
        )
        .reset_index()
    )

    summary2.to_csv(directory+"/pdf_list_summary2.csv",index=False)
    # print end results to console table
    print('\n')
    table = Table(title='Final Output',show_header=False)
    table.add_row('Pages crawled',str(len(crawled_pages)))
    table.add_row('PDFs found',str(len(found_pdfs)))
    console = Console()
    console.print(table)


if __name__ == "__main__":
    main()