import pandas as pd
from prophet import Prophet
import warnings
import emoji
import requests

def predict_atalho_real(result, product_description, prediction_month, prediction_year):
    product_data = pd.DataFrame()
    product_data['ds'] = result[result['description'].str.lower() == product_description.lower()]['date']
    product_data['y_perfect'] = result[result['description'].str.lower() == product_description.lower()]['perfect price']
    product_data['y_avg'] = result[result['description'].str.lower() == product_description.lower()]['avg price']

    model_perfect = Prophet()
    model_avg = Prophet()

    product_data_perfect = product_data[['ds', 'y_perfect']].rename(columns={'y_perfect': 'y'})
    product_data_avg = product_data[['ds', 'y_avg']].rename(columns={'y_avg': 'y'})

    model_perfect.fit(product_data_perfect)
    model_avg.fit(product_data_avg)

    prediction_date = pd.DataFrame({'ds': [f'{prediction_year}-{prediction_month:02d}-01']})

    perfect_prediction = model_perfect.predict(prediction_date)
    avg_prediction = model_avg.predict(prediction_date)

    predicted_perfect_price = perfect_prediction['yhat'].values[0]
    predicted_avg_price = avg_prediction['yhat'].values[0]

    formatted_perfect_price = f'{predicted_perfect_price:.2f}' + '€'
    formatted_avg_price = f'{predicted_avg_price:.2f}' + '€'

    product_data['ds']= pd.to_datetime(product_data['ds'])

    previous_years_data = product_data[product_data['ds'].dt.month == prediction_month]
    average_previous_years_price = previous_years_data['y_avg'].mean()

    formatted_previous_years_price = f'{average_previous_years_price:.2f}' + '€'

    if predicted_perfect_price > average_previous_years_price:
        emoji_perfect = emoji.emojize('💰')
    else:
        emoji_perfect = emoji.emojize('❌')
    
    if predicted_avg_price > average_previous_years_price:
        emoji_avg = emoji.emojize('💰')
    else:
        emoji_avg = emoji.emojize('❌')

    return '''
        Predicted Perfect Price: {} {}<br>
        Predicted Average Price: {} {}<br>
        Average Price for Same Month in Previous Years: {}<br>
    '''.format(formatted_perfect_price, emoji_perfect, formatted_avg_price, emoji_avg, formatted_previous_years_price)
