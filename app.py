from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
from lxml import etree
import requests
import json

app = Flask(__name__)

@app.route('/mercadolibre', methods=['GET'])
def mercadolibre():

    lista_titulos = []
    lista_urls = []
    lista_precios = []

    url = 'https://listado.mercadolibre.com.ar/celular'
    r = requests.get(url)
    if r.status_code==200:
        soup = BeautifulSoup(r.content, 'html.parser')

        titulos = soup.find_all('h2', attrs={'class': 'ui-search-item__title shops__item-title'})
        titulos = [i.text for i in titulos]
        lista_titulos.extend(titulos)

        urls = soup.find_all('a', attrs={'class': 'ui-search-item__group__element shops__items-group-details ui-search-link'})
        urls = [i.get('href') for i in urls]
        lista_urls.extend(urls)

        dom = etree.HTML(str(soup))
        
        precios = dom.xpath('//li[@class="ui-search-layout__item shops__layout-item"]//div[@class="ui-search-result__content-columns shops__content-columns"]//div[@class="ui-search-result__content-column ui-search-result__content-column--left shops__content-columns-left"]/div[1]/div/div/div[@class="ui-search-price__second-line shops__price-second-line"]//span[@class="price-tag-amount"]/span[2]')
        precios = [i.text for i in precios]
        lista_precios.extend(precios)

    return jsonify({'datos':{
        "titulos": lista_titulos,
        "urls": lista_urls,
        "precios": lista_precios,
    }})

if __name__ =="__main__":
    app.run(debug=True, host="0.0.0.0")
