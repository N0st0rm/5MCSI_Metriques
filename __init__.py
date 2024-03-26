from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
import requests
from datetime import datetime
from jinja2 import Template
                                                                                                                                       
app = Flask(__name__)

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
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html')

response = requests.get('https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits')
commits_data = response.json()

commits_per_minute = {}
for commit in commits_data:
    commit_date = commit['commit']['author']['date']
    date_object = datetime.strptime(commit_date, '%Y-%m-%dT%H:%M:%SZ')
    minute = date_object.minute
    commits_per_minute[minute] = commits_per_minute.get(minute, 0) + 1

minutes = list(commits_per_minute.keys())
commits_count = list(commits_per_minute.values())

with open('graph_commits.html', 'r') as file:
    template_content = file.read()

template = Template(template_content)
rendered_html = template.render(minutes=minutes, commits_count=commits_count)

with open('rendered_graph_commits.html', 'w') as output_file:
    output_file.write(rendered_html)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def monhistogramme():
    return render_template("histogramme.html")
  
if __name__ == "__main__":
  app.run(debug=True)
