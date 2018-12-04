import os

import requests
from flask import Flask, send_file, Response
from bs4 import BeautifulSoup

app = Flask(__name__)


def get_fact():
    response = requests.get("http://unkno.com")
    soup = BeautifulSoup(response.content, "html.parser")
    facts = soup.find_all("div", id="content")
    return " ".join(facts[0].getText().split())


def get_pig_latinized_url(fact):
    url = "https://hidden-journey-62459.herokuapp.com/piglatinize/"
    data = {'input_text': fact}
    r = requests.post(url, data=data, allow_redirects=False)
    return r.headers['Location']


@app.route('/')
def home():
    fact = get_fact()
    url = get_pig_latinized_url(fact)
    body = """
        <html>Click Me...</html>
        <br>
        <a href="{0}">{0}</a><br>
    """.format(url)
    return Response(response=body, mimetype='text/html')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6787))
    app.run(host='0.0.0.0', port=port)
