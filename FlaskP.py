import pandas as pd
from flask import Flask, render_template, request
from scripts.atalho_real import predict_atalho_real
from scripts.atalho_mercado import predict_atalho_mercado
from scripts.atalho_alvalade import predict_atalho_alvalade
from scripts.sumaya import predict_sumaya

import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('restaurant_form.html')

@app.route('/atalho_real')
def atalho_real():
    return render_template('process_data.html', restaurant='Atalho Real')

@app.route('/atalho_mercado')
def atalho_mercado():
    return render_template('process_data.html', restaurant='Atalho do Mercado')

@app.route('/atalho_alvalade')
def atalho_alvalade():
    return render_template('process_data.html', restaurant='Atalho de Alvalade')

@app.route('/sumaya')
def sumaya():
    return render_template('process_data.html', restaurant='Sumaya')

@app.route('/run_code', methods=['POST'])
def run_code():
    product_description = request.form['product']
    prediction_month = int(request.form['month'])
    prediction_year = int(request.form['year'])

    if request.form['restaurant'] == 'Atalho Real':
        result = pd.read_csv(r"C:\Users\simoe\Documents\IronHack\final_project_joao\clean_data\atalho_real.csv")
        output = predict_atalho_real(result, product_description, prediction_month, prediction_year)
    elif request.form['restaurant'] == 'Atalho do Mercado':
        result = pd.read_csv(r"C:\Users\simoe\Documents\IronHack\final_project_joao\clean_data\atalho_mercado.csv")
        output = predict_atalho_mercado(result, product_description, prediction_month, prediction_year)
    elif request.form['restaurant'] == 'Atalho de Alvalade':
        result = pd.read_csv(r"C:\Users\simoe\Documents\IronHack\final_project_joao\clean_data\atalho_alvalade.csv")
        output = predict_atalho_alvalade(result, product_description, prediction_month, prediction_year)
    elif request.form['restaurant'] == 'Sumaya':
        result = pd.read_csv(r"C:\Users\simoe\Documents\IronHack\final_project_joao\clean_data\sumaya.csv")
        output = predict_sumaya(result, product_description, prediction_month, prediction_year)
    else:
        output = "Invalid restaurant name"

    return render_template('process_data.html', result=output, restaurant = request.form["restaurant"])

if __name__ == '__main__':
    app.run(debug=True, port=8000)
