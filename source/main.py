import urllib3
import re
from bs4 import BeautifulSoup
import time
import pandas as pd
import seleniumScript
from datetime import date


# la funció download permet accedir a les url i ens retorna el codi html
def download(url):
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


def product_scrapper_v2(url, section_list, path=r'C:\Program Files\Mozilla Firefox\firefox.exe'):
    verified = "https://static.electrocosto.com/images/icons/verified.svg"
    today = date.today()

    def url_blacklist(url):
        html = download(url + r"\robots.txt")
        banned_links = re.findall(r'Disallow:\s(.*?)\*', html)
        return banned_links

    def get_urls(url, section_list, path=r'C:\Program Files\Mozilla Firefox\firefox.exe'):
        print("Loading content")
        links = dict()
        for section in section_list:
            html = seleniumScript.expand_section(section, path)
            soup = BeautifulSoup(html, features="html.parser")
            a = soup.div
            for card in a.find_all(class_="recomender-block-item"):
                links[url + card.a["href"]] = section
        return links

    def check_disallowed(url_list, disallow):
        print("Checking for disallowed urls")
        disallow_pattern = '|'.join(disallow)
        for item in url_list.keys():
            if re.search(disallow_pattern, url):
                url_list.pop(item)
        return url_list

    def scrapper_dict_setup() -> dict:
        print("Setting up Attributes")
        # preparem les keys comunes del dict
        setup_dict = dict()
        setup_dict["product-name"] = []
        setup_dict["product-type"] = []
        setup_dict["price"] = []
        setup_dict["ref"] = []
        setup_dict["marca"] = []
        setup_dict["val-points"] = []
        setup_dict["val-quantity"] = []
        setup_dict["stock"] = []
        setup_dict["product-sending-value"] = []
        setup_dict["date"] = []

        return setup_dict

    def data_scrapper(urllist, data_dict) -> dict:
        count = 0
        print("Scrapping data")
        for url in urllist.keys():
            # les característiques generals apareixen a totes les URL, i les predefinim
            html = download(url)
            soup = BeautifulSoup(html, features="html.parser")
            try:
                data_dict["product-name"].append(soup.find(class_="product-name").string)
            except:
                data_dict["product-name"].append("NULL")
            data_dict["product-type"].append(urllist[url])
            try:
                data_dict["price"].append(soup.find(class_="iva-included").span.string)
            except:
                data_dict["price"].append("NULL")
            try:
                data_dict["ref"].append(soup.find(class_="reference").span.string)
            except:
                data_dict["ref"].append("NULL")
            try:
                data_dict["marca"].append(soup.find(class_="productPagePrices").a["title"])
            except:
                data_dict["marca"].append("NULL")
            try:
                data_dict["val-points"].append(soup.find(class_="val-points").string)
            except:
                data_dict["val-points"].append("NULL")
            try:
                data_dict["val-quantity"].append(soup.find(class_="val-quantity").string)
            except:
                data_dict["val-quantity"].append("NULL")
            try:
                if soup.find(class_="stock__status").span.img["src"] == verified:
                    data_dict["stock"].append("Disponible")
                else:
                    data_dict["stock"].append("No Disponible")
            except:
                data_dict["stock"].append("NULL")
            try:
                data_dict["product-sending-value"].append(soup.find(class_="sending-price-wrapper").find(
                class_="product-sending-value").string)
            except:
                data_dict["product-sending-value"].append("NULL")
            data_dict["date"].append(today)
            # per la resta de característiques hem d'anar vigilant que tinguin el nombre d'elements adequats
            # ja que de forma normal si l'element no apareix al html de la web no s'afegirà al dict
            for atr in soup.find_all(class_="product-table-atributes"):
                elements = atr.find_all("td")
                for i in range(0, len(elements), 2):
                    key = elements[i].string.replace("\n", "").replace(" ", "").replace("\r", "")
                    try:
                        value = elements[i+1].string.replace("\n", "")
                    except:
                        value = "NULL"
                    # fem que busqui totes les característiques de decripció del prod i que les afegeixi al dict
                    if key not in data_dict.keys():
                        data_dict[key] = []
                    # cada element que anem a afegir mirem que tingui el nombre de entrades corresponent a les url que
                    # portem revisades, si es menor anem afegint elements NULL fins que tingui la llargada que toca
                    while len(data_dict[key]) < count:
                        data_dict[key].append("NULL")
                    data_dict[key].append(value)
            count += 1
            # time.sleep(0.5)

        # fem un ultim repas de que tots els elements tinguin la llargada que toca
        for key in data_dict.keys():
            while len(data_dict[key]) < len(urllist):
                data_dict[key].append("NULL")
        print("Scrapping complete")

        return data_dict

    link_list = get_urls(url, section_list)
    blacklist = url_blacklist(url)
    clean_list = check_disallowed(link_list, blacklist)

    return data_scrapper(clean_list, scrapper_dict_setup())


llista_categories = ["lavadoras", "microondas", "lavavajillas", "moviles", "televisores", "portatiles", "calentadores"]

electrodomestics = product_scrapper_v2("https://www.electrocosto.com", llista_categories)

electrodomestics_data = pd.DataFrame.from_dict(electrodomestics)
electrodomestics_data.to_csv("electrodomestics.csv", index=False)

