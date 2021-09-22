import flask
from flask import request,render_template
import pandas as pd

cols=["pg","word","definition","sentence","category","sample","synonyms"]
data = pd.read_csv('./ISLT_data.csv', sep=',', engine='python', usecols=cols,na_values = [''])
json_data = data.to_json(orient = "records")
print(json_data)

app = flask.Flask(__name__)


@app.route('/getData')
def home():
    return json_data
@app.route("/", methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        print(request.form)
    return render_template('create.html')