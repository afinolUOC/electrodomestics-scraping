import urllib3
import re
from bs4 import BeautifulSoup
import pandas as pd


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


'''
def product_scrapper(url):
    data = dict()
    html = download(url)
    soup = BeautifulSoup(html, features="html.parser")
    data["product-name"] = soup.find(class_="product-name").string
    data["price"] = soup.find(class_="iva-included").span.string
    data["ref"] = soup.find(class_="reference").span.string
    data["marca"] = soup.find(class_="productPagePrices").a["title"]
    data["val-points"] = soup.find(class_="val-points").string
    data["val-quantity"] = soup.find(class_="val-quantity").string
    if soup.find(class_="stock__status").span.img["src"] == "https://static.electrocosto.com/images/icons/verified.svg":
        data["stock"] = "Disponible"
    else:
        data["stock"] = "No Disponible"
    data["product-sending-value"] = soup.find(class_="sending-price-wrapper").find(class_="product-sending-value").string

    print(data)
'''


def product_scrapper_v2(urls):
    verified = "https://static.electrocosto.com/images/icons/verified.svg"
    def scrapper_dict_setup(urllist) -> dict:
        # preparem les keys comunes del dict
        setup_dict = dict()
        setup_dict["product-name"] = []
        setup_dict["price"] = []
        setup_dict["ref"] = []
        setup_dict["marca"] = []
        setup_dict["val-points"] = []
        setup_dict["val-quantity"] = []
        setup_dict["stock"] = []
        setup_dict["product-sending-value"] = []
        # fem que busqui totes les característiques de decripció del prod i que les afegeixi al dict
        for url in urllist:
            html = download(url)
            soup = BeautifulSoup(html, features="html.parser")
            for atr in soup.find_all(class_="product-table-atributes"):
                elements = atr.find_all("td")
                for i in range(0, len(elements), 2):
                    setup_dict[elements[i].string.replace("\n", "").replace(" ", "")] = []
        return setup_dict

    def data_scrapper(urllist, data_dict) -> dict:
        count = 0
        for url in urllist:
            # les característiques generals apareixen a totes les URL, i les predefinim
            html = download(url)
            soup = BeautifulSoup(html, features="html.parser")
            data_dict["product-name"].append(soup.find(class_="product-name").string)
            data_dict["price"].append(soup.find(class_="iva-included").span.string)
            data_dict["ref"].append(soup.find(class_="reference").span.string)
            data_dict["marca"].append(soup.find(class_="productPagePrices").a["title"])
            data_dict["val-points"].append(soup.find(class_="val-points").string)
            data_dict["val-quantity"].append(soup.find(class_="val-quantity").string)
            if soup.find(class_="stock__status").span.img["src"] == verified:
                data_dict["stock"].append("Disponible")
            else:
                data_dict["stock"].append("No Disponible")
            data_dict["product-sending-value"].append(soup.find(class_="sending-price-wrapper").find(
                class_="product-sending-value").string)
            # per la resta de característiques hem d'anar vigilant que tinguin el nombre d'elements adequats
            # ja que de forma normal si l'element no apareix al html de la web no s'afegirà al dict
            for atr in soup.find_all(class_="product-table-atributes"):
                elements = atr.find_all("td")
                for i in range(0, len(elements), 2):
                    key = elements[i].string.replace("\n", "").replace(" ", "")
                    value = elements[i+1].string.replace("\n", "").replace(" ", "")
                    # cada element que anem a afegir mirem que tingui el nombre de entrades corresponent a les url que
                    # portem revisades, si es menor anem afegint elements NULL fins que tingui la llargada que toca
                    while len(data_dict[key]) < count:
                        data_dict[key].append("NULL")
                    data_dict[key].append(value)
            count += 1

        # fem un ultim repas de que tots els elements tinguin la llargada que toca
        for key in data_dict.keys():
            while len(data_dict[key]) < len(urllist):
                data_dict[key].append("NULL")

        return data_dict

    return data_scrapper(urls, scrapper_dict_setup(urls))


# print(download("https://www.electrocosto.com/sitemap.xml"))
# crawl_sitemap("https://www.electrocosto.com/sitemap.xml")
# soup("https://www.electrocosto.com/lavadoras")
# product_scrapper("https://www.electrocosto.com/frigorificos-combis/balay-3kfe776xe-inox")
neveras = product_scrapper_v2(["https://www.electrocosto.com/frigorificos-combis/balay-3kfe776xe-inox",
                               "https://www.electrocosto.com/frigorificos-dos-puertas/indesit-taa-5-1",
                               "https://www.electrocosto.com/frigorificos-combis/beko-b1rche-363-w-blanco"])
neveras_data = pd.DataFrame.from_dict(neveras)
print(neveras_data)
