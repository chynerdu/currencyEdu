from flask import Flask, render_template
import requests
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

#Create a flask app instance named "app"
app = Flask('app')
#my api_key
API_KEY = 'q7Z8KRiyXBBAiaZHyado'


@app.route('/')
def index():
    # define api urls with api key
    trade_volume_vs_ratio_url = f'https://data.nasdaq.com/api/v3/datatables/QDL/BCHAIN.json?code=TVTVR&api_key={API_KEY}'
    other_metric_url = f'https://data.nasdaq.com/api/v3/datatables/QDL/BCHAIN.json?api_key={API_KEY}&code=MKPRU'
#Note I used MKPRU Bitcoin Market Value as my other metric
    
    # Use the request.get() to retrieve the data from the API and stores it in JSON format
    print(f'calling api  {trade_volume_vs_ratio_url}')
    trade_volume_vs_ratio_data = requests.get(trade_volume_vs_ratio_url).json()

    other_metric_data = requests.get(other_metric_url).json()
 

    

    # Convert to DataFrame
    columns = [col['name'] for col in trade_volume_vs_ratio_data['datatable']['columns']]
    trade_volume_vs_Volume_Ratio_df = pd.DataFrame(trade_volume_vs_ratio_data['datatable']['data'], columns=columns)

    other_metric_df = pd.DataFrame(other_metric_data['datatable']['data'], columns=columns)

    
    # Convert date to datetime format
    trade_volume_vs_Volume_Ratio_df['date'] = pd.to_datetime(trade_volume_vs_Volume_Ratio_df['date'])


    other_metric_df['date'] = pd.to_datetime(other_metric_df['date'])
    
    #Filter between 2013 to 2016 (Could'nt find an api for this)
    filtered_trade_volume_vs_Volume_Ratio_df = trade_volume_vs_Volume_Ratio_df[
        (trade_volume_vs_Volume_Ratio_df['date'] >= '2013-01-01') &
        (trade_volume_vs_Volume_Ratio_df['date'] <= '2016-12-31')
    ]

    filtered_other_metric_df = other_metric_df[
        (other_metric_df['date'] >= '2013-01-01') &
        (other_metric_df['date'] <= '2016-12-31')
    ]
    # Merge DataFrames
    merged_df = pd.merge(filtered_trade_volume_vs_Volume_Ratio_df, filtered_other_metric_df, on='date', how='inner')

    # Display result
    print(merged_df)

    # Plot data
    plt.figure(figsize=(10, 5))
    plt.plot(merged_df['date'], merged_df['value_x'], label='Bitcoin_Trade_volume_vs_Volume_Ratio')
    plt.plot(merged_df['date'], merged_df['value_y'], label='Bitcoin Market Price')
    plt.xlabel('date')
    plt.ylabel('Value')
    plt.title('Bitcoin Metrics Over Time(2013 - 2016)')
    plt.legend()

    # Save plot to a string buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plot_url = base64.b64encode(buf.getvalue()).decode('utf8')    #encode the image to base64 string

    return render_template('index.html', 
                           plot_url=plot_url) #render the template with the plot_url

app.run(host='0.0.0.0', port=8080)
