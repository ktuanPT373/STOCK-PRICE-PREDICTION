from flask import Flask, render_template, request
import pandas as pd
from read_the_data import read_the_data
from crawling_data import fetch_stock_data
from LinReg import Lr_implement
from KNN import KNN_implement
from Tree import Tree_implement
import sys
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    name = request.form['name']
    opun = float(request.form['opun'])
    high = float(request.form['high'])
    low = float(request.form['low'])
    volume = float(request.form['volume'])
    # def loading_animation():
    #     chars = ['.', '..', '...', '....']
    #     for _ in range(10):  
    #         for char in chars:
    #             sys.stdout.write(f'\rFetching{char}')
    #             sys.stdout.flush()
    #             time.sleep(0.3) 

    # loading_animation()
    stock_data = fetch_stock_data(name, '10y')

    data = pd.DataFrame({'Open': [opun], 'High': [high], 'Low': [low], 'Volume': [volume]})

    read_the_data(stock_data)

    model = request.form['model'].upper()
    time.sleep(3)

    if model == 'LR':
        accu,final = Lr_implement(stock_data, data)
    elif model == 'TR':
        accu,final = Tree_implement(stock_data, data)
    elif model == 'KN':
        accu,final = KNN_implement(stock_data, data)
    else:
        return "Invalid input. Please choose LR, TR, or KN."

    return render_template('result.html', accu=round(accu*100), final=round(final[0],4))

if __name__ == '__main__':
    app.run(debug=True)
