import requests
from bs4 import BeautifulSoup
import urllib2


hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

def download_file(file_name, download_url):
    try:
        req = urllib2.Request(download_url, headers=hdr)
        response = urllib2.urlopen(req)
        file = open(file_name + ".pdf", 'wb')
        file.write(response.read())
        file.close()
    except urllib2.HTTPError, e:
        print e.fp.read()

base_url = "https://www.google.com.sg/search?q=site:itg.com+filetype:pdf+trading"
prev_href = ""
for i in range(1000):
    x = i * 10
    url = base_url + "&start=%d" % x
    print url
    page = requests.get(url, verify=False)
    soup = BeautifulSoup(page.content)
    links = soup.findAll("a")
    downloaded = False
    for link in links:
        pos = link["href"].find("http://www.itg.com")
        href = ""
        if pos >= 0:
            href = link["href"][pos:]
        else:
            pos = link["href"].find("https://www.itg.com")
            if pos >= 0:
                href = link["href"][pos:]
        end_pos = href.find(".pdf")
        if end_pos < 0:
            continue
        href = href[:end_pos + 4]
        if href != "" and href != prev_href:
            print href
            prev_href = href
            download_file('./trading/' + href.split('/')[-1], href)
            downloaded = True
    if not downloaded:
        break