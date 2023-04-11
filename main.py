import urllib3
import re
from bs4 import BeautifulSoup


# la funció download permet accedir a les url i ens retorna el codi html
def download(url, user_agent="ws", num_retries=2):
    print("Downloading", url)
    headers = {"User-agent", user_agent}
    http = urllib3.PoolManager()
    r = http.request('GET', url)
    html = r.data.decode('utf-8')
    return html


# petit bot que retorna els links del sitemap
def crawl_sitemap(url):
    sitemap = download(url)
    links = re.findall('<loc>(.*?)</loc>', sitemap)
    for link in links:

        print(link)


# de la url donada retorna una llista amb els links dels productes
# falta implementar el scroll de la pàgina
def soup(url):
    html = download(url)
    soup = BeautifulSoup(html, features="html.parser")
    a = soup.div
    links = []
    for card in a.find_all(class_="recomender-block-item"):
        links.append(url + card.a["href"])
    print(links)


# print(download("https://www.electrocosto.com/sitemap.xml"))
# crawl_sitemap("https://www.electrocosto.com/sitemap.xml")
soup("https://www.electrocosto.com/lavadoras")
