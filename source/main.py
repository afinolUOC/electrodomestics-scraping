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


def product_scrapper_v2(url, section):
    verified = "https://static.electrocosto.com/images/icons/verified.svg"
    today = date.today()

    def url_blacklist(url):
        html = download(url + "robots.txt")
        banned_links = re.findall(r'Disallow:\s(.*?)\*', html)
        return banned_links

    def get_urls(url, section):
        expanded_url = seleniumScript.expand_section(section)
        html = download(expanded_url)
        soup = BeautifulSoup(html, features="html.parser")
        a = soup.div
        links = []
        for card in a.find_all(class_="recomender-block-item"):
            links.append(url + section + card.a["href"])
        return links

    def check_disallowed(url_list, disallow):
        disallow_pattern = '|'.join(disallow)
        for item in url_list:
            if re.search(disallow_pattern, url):
                url_list.pop(item)
        return url_list

    def scrapper_dict_setup(urllist) -> dict:
        print("Setting up Attributes")
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
        data_dict["date"] = []
        # fem que busqui totes les característiques de decripció del prod i que les afegeixi al dict
        for item in urllist:
            html = download(item)
            soup = BeautifulSoup(html, features="html.parser")
            for atr in soup.find_all(class_="product-table-atributes"):
                elements = atr.find_all("td")
                for i in range(0, len(elements), 2):
                    setup_dict[elements[i].string.replace("\n", "").replace(" ", "")] = []
            time.sleep(0.5)
        return setup_dict

    def data_scrapper(urllist, data_dict) -> dict:
        count = 0
        for url in urllist:
            print("Downloading", url)
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
            data_dict["date"] = today
            # per la resta de característiques hem d'anar vigilant que tinguin el nombre d'elements adequats
            # ja que de forma normal si l'element no apareix al html de la web no s'afegirà al dict
            for atr in soup.find_all(class_="product-table-atributes"):
                elements = atr.find_all("td")
                for i in range(0, len(elements), 2):
                    key = elements[i].string.replace("\n", "").replace(" ", "")
                    value = elements[i+1].string.replace("\n", "")
                    # cada element que anem a afegir mirem que tingui el nombre de entrades corresponent a les url que
                    # portem revisades, si es menor anem afegint elements NULL fins que tingui la llargada que toca
                    while len(data_dict[key]) < count:
                        data_dict[key].append("NULL")
                    data_dict[key].append(value)
            count += 1
            time.sleep(0.5)

        # fem un ultim repas de que tots els elements tinguin la llargada que toca
        for key in data_dict.keys():
            while len(data_dict[key]) < len(urllist):
                data_dict[key].append("NULL")

        return data_dict

    link_list = get_urls(url, section)
    blacklist = url_blacklist(url)
    clean_list = check_disallowed(link_list, blacklist)

    return data_scrapper(clean_list, scrapper_dict_setup(clean_list))


# print(re.findall(r'Disallow:\s(.*?)\*', download("https://www.electrocosto.com/robots.txt")))
# crawl_sitemap("https://www.electrocosto.com/sitemap.xml")
# get_urls("https://www.electrocosto.com/", "frigorificos")
# product_scrapper("https://www.electrocosto.com/frigorificos-combis/balay-3kfe776xe-inox")
'''
neveras = product_scrapper_v2(["https://www.electrocosto.com/frigorificos-combis/balay-3kfe776xe-inox",
                               "https://www.electrocosto.com/frigorificos-dos-puertas/indesit-taa-5-1",
                               "https://www.electrocosto.com/frigorificos-combis/beko-b1rche-363-w-blanco",
                               "https://www.electrocosto.com/frigorificos-americanos/kroms-kf-4p-80-ddix",
                               "https://www.electrocosto.com/frigorificos-dos-puertas/smeg-fab30rbe5",
                               "https://www.electrocosto.com/frigorificos-combis/bosch-kgn36vida",
                               "https://www.electrocosto.com/frigorificos-combis/lg-gbp61swpgn",
                               "https://www.electrocosto.com/frigorificos-combis/balay-3kfe778wi-blanco",
                               "https://www.electrocosto.com/frigorificos-combis/winia-wrn-bv300-npt",
                               "https://www.electrocosto.com/frigorificos-combis/balay-3kfe560wi-blanco"])

neveras_data = pd.DataFrame.from_dict(neveras)
neveras_data.to_csv("neveras.csv", index=False)
'''
