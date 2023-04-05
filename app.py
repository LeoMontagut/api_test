from flask import Flask, jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route("/amazon", methods=['GET'])
def amazon():
    search_word = "televisor"
    url = f"https://www.amazon.com/s?k={search_word}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0',
        'referer': 'https://google.com'
    }
    r = requests.get(url,headers=headers)
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        try:
            urls = soup.find('div', attrs={
                "class": "s-main-slot s-result-list s-search-results sg-row"
            }).find_all("a", attrs={
                "class": "a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"
            })
            urls = ['https://www.amazon.com' + i.get('href') for i in urls[:5]]
        except:
            urls = []
        
        return jsonify({'data': urls})

    return jsonify({'STATUS CODE': r.status_code})



# //div[@class="s-main-slot s-result-list s-search-results sg-row"]//a[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]



if __name__ =="__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")
