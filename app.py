from flask import Flask
import yfinance as yf
import os
import pandas as pd

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/stock/history/<ticker>')
def stock_info(ticker):
    if os.path.isfile(ticker + '.csv'):
        return pd.read_csv(ticker + '.csv').to_json()

    data_df = yf.download(ticker, start='2017-04-01', end='2021-04-01')
    data_df.to_csv(ticker + '.csv')
    return data_df.to_json()


@app.route('/stock/history/<ticker>/start/<start_date>/end/<end_date>')
def stock_info_custom(ticker, start_date, end_date):
    if os.path.isfile(ticker + '.csv'):
        return pd.read_csv(ticker + '.csv').to_json()

    data_df = yf.download(ticker, start=start_date, end=end_date)
    data_df.to_csv(ticker + '.csv')
    return data_df.to_json()


@app.route('/covid/daily/usa')
def daily_covid_data_usa():
    if os.path.isfile('daily_covid_usa.json'):
        return pd.read_json('daily_covid_usa.json').to_json()

    data = pd.read_json('https://api.covidtracking.com/v1/us/daily.json')
    data.to_json('daily_covid_usa.json')
    return data.to_json()


@app.route('/indicators/unemployment/rates/usa')
def twitter_recent_tweets():

    df = pd.read_csv('UnemploymentStatistics.csv')
    print(df.shape)
    return pd.read_csv('UnemploymentStatistics.csv').to_json()


if __name__ == '__main__':
    app.run(port=5000)
