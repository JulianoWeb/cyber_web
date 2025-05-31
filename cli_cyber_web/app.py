from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/status', methods=['GET', 'POST'])
def status():
    result = None
    if request.method == 'POST':
        url = request.form['url']
        try:
            response = requests.get(url, timeout=5)
            result = f"{url} - {response.status_code} {response.reason}"
        except Exception as e:
            result = f"Erro: {e}"
    return render_template('status.html', result=result)

@app.route('/cep', methods=['GET', 'POST'])
def cep():
    data = None
    if request.method == 'POST':
        cep = request.form['cep']
        url = f"https://viacep.com.br/ws/{cep}/json/"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
        else:
            data = {"erro": "CEP não encontrado!"}
    return render_template('cep.html', data=data)

@app.route('/crawler', methods=['GET', 'POST'])
def crawler():
    links = []
    if request.method == 'POST':
        url = request.form['url']
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            links = [link['href'] for link in soup.find_all('a', href=True)]
        except Exception as e:
            links = [f"Erro: {e}"]
    return render_template('crawler.html', links=links)

if __name__ == '__main__':
    app.run(debug=True)
