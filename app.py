import flask
from flask import request, render_template
import pandas as pd
from flask_cors import CORS, cross_origin
import os



# file should be saved somewhere else, should not be a part of build folder
csv_path = "./words4.csv"


def readCSV():
    cols = ["function","book","word","pg","definition","sentence","question","category","sample","synonyms","choices"]
    data = pd.read_csv(csv_path, sep=',', usecols=cols, na_values=[''], doublequote=True,
                          skipinitialspace='True')
    data = data.replace("\"\"", "\"")
    
    return data

print('***Backend Running***')

def retrieveData(data):
    # data = readCSV()

    json_data = data.to_json(orient="records")
    
    json_list = json_data.replace("\\", "")
    
    print(json_list)
    return json_list


app = flask.Flask(__name__, template_folder='template')
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

print('***Backend Running***')


@app.route('/')
def home():
    return render_template('create.html')


@app.route('/getData', methods=['GET'])
def getData():
    data = readCSV()
    return retrieveData(data)


@app.route('/sendData', methods=['GET', 'POST'])
@cross_origin()
def sendData():
    if request.method == "POST":
        postData = pd.json_normalize(request.form)
        data = readCSV()
        newData = pd.concat([data, postData], ignore_index=True)
        # adding new data into csv
        os.remove(csv_path)
        newData.to_csv(csv_path, index=False)
    return request.form


@app.route('/filterBy', methods=['GET', 'POST'])
@cross_origin()
def filterBy():
    data = readCSV()
    filterOptions = request.get_json()  # get filterOptions from request
    if (filterOptions['category'] == "All") & (filterOptions['book'] == "All"):
        newData = data[((data['function'] == "c") | (data['function'] == "b")) ]
    elif (filterOptions['category'] == "All") & (filterOptions['book'] != "All"):
        newData = data[(data['book'] == filterOptions['book']) & ((data['function'] == "c") | (data['function'] == "b")) ]
    elif (filterOptions['category'] != "All") & (filterOptions['book'] == "All"):
        newData = data[(data['category'] == filterOptions['category']) & ((data['function'] == "c") | (data['function'] == "b")) ]
    else:
        newData = data[(data['category'] == filterOptions['category']) & (data['book'] == filterOptions['book']) & ((data['function'] == "c") | (data['function'] == "b")) ]
    
    print(newData)
    return retrieveData(newData)
@app.route('/filterForQuiz', methods=['GET', 'POST'])
@cross_origin()
def filterForQuiz():
    data = readCSV()
    filterOptions = request.get_json()  # get filterOptions from request
    if (filterOptions['category'] == "All") & (filterOptions['book'] == "All"):
        newData = data[((data['function'] == "q") | (data['function'] == "b")) ]
    elif (filterOptions['category'] == "All") & (filterOptions['book'] != "All"):
        newData = data[(data['book'] == filterOptions['book']) & ((data['function'] == "q") | (data['function'] == "b")) ]
    elif (filterOptions['category'] != "All") & (filterOptions['book'] == "All"):
        newData = data[(data['category'] == filterOptions['category']) & ((data['function'] == "q") | (data['function'] == "b")) ]
    else:
        newData = data[(data['category'] == filterOptions['category']) & (data['book'] == filterOptions['book']) & ((data['function'] == "q") | (data['function'] == "b")) ]
    print(newData)
    return retrieveData(newData)
