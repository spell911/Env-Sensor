# Server Side
from flask import Flask, Response, render_template
from flask_restful import Api, Resource, abort, reqparse, marshal_with, fields
from flask_sqlalchemy import SQLAlchemy, Model
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from _cons import SQLALCHEMY_DATABASE_URI

import io
import pandas as pd
import json
import matplotlib.pyplot as plt

app = Flask(__name__)

# database
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.debug = True
db = SQLAlchemy(app)
api = Api(app)


@app.route('/temp-humidity-stats', methods=['GET'])
def temp_humidity_stats():
    """
    Calculate simple data stats of tempreture and humidity

    Return:
        (dict), stats data
    """
    df = get_data()
    # filter temp/humidity, by device, for outliers (>1% & <99%)
    df = filter_temp_humidity(df)

    stats = {
        'record_count': '{:,}'.format(df['env_id'].count()),
        'time_range_min': '{:%Y-%m-%d %H:%M:%S %Z}'.format(df.index[1]),
        'time_range_max': '{:%Y-%m-%d %H:%M:%S %Z}'.format(df.index[-1]),
        'temp_min_celsius': '{:.2f}'.format(df['temp'].min()),
        'temp_max_celsius': '{:.2f}'.format(df['temp'].max()),
        'humidity_min_percent': '{:.2f}'.format(df['humidity'].min()),
        'humidity_max_percent': '{:.2f}'.format(df['humidity'].max())
    }

    return stats


@app.route('/temp-humidity-plot.png', methods=['GET'])
def temp_humidity_plot():
    """
    Plot relation of tempreture and humidity graph

    Return:
        png graph
    """
    # create figure in this function
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)

    return Response(output.getvalue(), mimetype='image/png')


def get_data():
    """
    Get iot telemetry data from postgres db

    Return:
        (list), dataframe of iot telemetry data
    """
    result = db.session.query(db.Table('iot_telemetry', db.metadata,
                                       autoload=True, autoload_with=db.engine)).all()
    df = pd.DataFrame(result, columns=[
                      'env_id', 'ts', 'device', 'co', 'humidity', 'light', 'lpg', 'motion', 'smoke', 'temp'])
    # convert ts column to datetime
    df['ts'] = pd.to_datetime(
        df['ts'], infer_datetime_format=True, unit='s', utc=True)
    # set ts column index
    df = df.set_index('ts')
    # sort data by ts column
    df = df.sort_values(by='ts', ascending=True)

    return df


def create_figure():
    """
    Plot graph and figure

    Return:
        (tuple), figure
    """
    df = get_data()
    # filter temp/humidity, by device, for outliers (>1% & <99%)
    df = filter_temp_humidity(df)
    groups = df.groupby('device')
    fig, ax = plt.subplots(1, 1, figsize=(8, 4))

    for device, group in groups:
        ax.plot(group['temp'],
                group['humidity'],
                marker='o',
                linestyle='',
                alpha=.5,
                ms=10,
                label=device)
    ax.grid()
    ax.margins(0.05)
    ax.legend()
    plt.title('Temperature and Humidity')
    plt.xlabel('Temperature (˚c)')
    plt.ylabel('Humidity (%)')

    return fig


def filter_temp_humidity(df):
    """
    Filter temp/humidity, by device, for outliers (>1% & <99%)

    Args:
        df (dataframe): dataframe of iot telemetry.

    Return:
        (dataframe)
    """
    df = df.loc[df['temp'] > df.groupby(
        'device').temp.transform(lambda x: x.quantile(.01))]
    df = df.loc[df['temp'] < df.groupby(
        'device').temp.transform(lambda x: x.quantile(.99))]

    df = df.loc[df['humidity'] > df.groupby(
        'device').humidity.transform(lambda x: x.quantile(.01))]
    df = df.loc[df['humidity'] < df.groupby(
        'device').humidity.transform(lambda x: x.quantile(.99))]

    return df


if __name__ == "__main__":
    app.run()
