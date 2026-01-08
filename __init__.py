from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
import requests

                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html') #commit

@app.route("/contact/")
def MaPremiereAPI():
    return render_template("contact.html")

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)
  
@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def mongraphique1():
    return render_template("histogramme.html")

@app.route("/commits/")
def commits_page():
    return render_template("commits.html")

@app.route('/commits-data/')
def commits_data():
    url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits'
    response = requests.get(url)
    commits_json = response.json()

    # Dictionnaire minute -> nombre de commits
    minutes_count = {}

    for commit in commits_json:
        # "2024-02-11T11:57:27Z" dans commit["commit"]["author"]["date"]
        date_string = commit.get("commit", {}).get("author", {}).get("date")
        if not date_string:
            continue
        date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        minute = date_object.minute
        minutes_count[minute] = minutes_count.get(minute, 0) + 1

    # Transformer en liste exploitable côté JS
    results = []
    for minute, count in sorted(minutes_count.items()):
        results.append({"minute": minute, "count": count})

    return jsonify(results=results)


if __name__ == "__main__":
  app.run(debug=True)
