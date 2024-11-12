from flask import Flask, render_template
import requests
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

#Create a flask app instance named "app"
app = Flask('app')
#my api_key
API_KEY = '2JDYdPSbB875jbzMsxU5'

#Decorator defining a function to handle requests for the root path '/'
@app.route('/')
def index():
    # Fetch data from Nasdaq API for the three variables for Bitcoin metrics
    trade_volume_vs_ratio_url = f'https://data.nasdaq.com/api/v3/datasets/BCHAIN/TVTVR.json?api_key={API_KEY}&start_date=2015-01-01&end_date=2016-07-19'
    other_metric_url = f'https://data.nasdaq.com/api/v3/datasets/BCHAIN/MKPRU.json?api_key={API_KEY}&start_date=2015-01-01&end_date=2016-07-19'
#Note I used MKPRU Bitcoin Market Value as my other metric
    
    # uses request.get() to fetch the data from the API and stores it in JSON format
    trade_volume_vs_ratio_data = requests.get(trade_volume_vs_ratio_url).json()
    other_metric_data = requests.get(other_metric_url).json()
    # print(Trade_volume_vs_Volume_Ratio_data)

    # Process data: Create Pandas Dataframes from the JSON data for each metrics
    trade_volume_vs_Volume_Ratio_df = pd.DataFrame(trade_volume_vs_ratio_data['dataset']['data'], columns=trade_volume_vs_ratio_data['dataset']['column_names'])
    # transaction_volume_df = pd.DataFrame(transaction_volume_data['dataset']['data'], columns=transaction_volume_data['dataset']['column_names'])
    other_metric_df = pd.DataFrame(other_metric_data['dataset']['data'], columns=other_metric_data['dataset']['column_names'])
    # print(trade_volume_df)

    # Merge dataframes on date
    # merged_df = pd.merge(trade_volume_df, transaction_volume_df, on='Date')
    merged_df = pd.merge(trade_volume_vs_Volume_Ratio_df, other_metric_df, on='Date', how='inner')
    print(merged_df)

    # Plot data
    plt.figure(figsize=(10, 5))
    plt.plot(merged_df['Date'], merged_df['Value_x'], label='Bitcoin_Trade_volume_vs_Volume_Ratio')
    plt.plot(merged_df['Date'], merged_df['Value_y'], label='Bitcoin Market Price')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.title('Bitcoin Metrics Over Time(2015 - 2016)')
    plt.legend()

    # Save plot to a string buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plot_url = base64.b64encode(buf.getvalue()).decode('utf8')    #encode the image to base64 string

    return render_template('index.html', 
                           plot_url=plot_url) #render the template with the plot_url

app.run(host='0.0.0.0', port=8080)
