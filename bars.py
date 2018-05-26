import os
import json
import argparse
import requests
from random import uniform


def download_bars_json():
    url = 'https://devman.org/fshare/1503831681/4/'
    try:
        bars_data = requests.get(url).json()
        return bars_data['features']
    except ValueError as e:
        print('Не могу скачать или распокавать данные,'
              'попробуйте открыть в браузере '+url)


def load_data(filepath):
    try:
        return json.load(open(filepath, 'r', encoding='UTF8'))['features']
    except ValueError as e:
        print('Не могу прочитать данные из файла {}'
              .format(filepath))
    except OSError  as e:
        print('Файл {} не существует '
              .format(filepath))


def get_biggest_bar(bars_data):
    return max(bars_data,
               key=lambda bar: bar['properties']['Attributes']['SeatsCount'])\
        ['properties']['Attributes']['Name']


def get_smallest_bar(bars_data):
    return min(bars_data,
               key=lambda bar: bar['properties']['Attributes']['SeatsCount'])\
        ['properties']['Attributes']['Name']


def get_closest_bar(bars_data, longtitude, latitude):
    return min(bars_data, key=lambda bar:
    (bar['geometry']['coordinates'][0] - longtitude) ** 2 +
    (bar['geometry']['coordinates'][1] - latitude) ** 2)\
        ['properties']['Attributes']['Name']


def validate_latitude(lat):
    lat = float(lat)
    if lat < -90 or lat > 90:
        raise argparse.ArgumentTypeError("Latitude must be between"
                                         " -90 and 90 degrees")
    return lat


def validate_longtitude(long):
    long = float(long)
    if long < -180 or long > 180:
        raise argparse.ArgumentTypeError("Longtitude must be between"
                                         " -180 and 180 degrees")
    return long


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-d', action='store_true',
                        dest='flag_download',
                        help='If set data will be downloaded'
                             ' from https://devman.org/fshare/1503831681/4/')

    parser.add_argument('-f', action='store',
                        dest='filepath',
                        help='Filepath with data, "bars.json" by default',
                        default='bars.json'
                        )

    parser.add_argument('-lat', action='store',
                        type=validate_latitude,
                        dest='latitude',
                        help='You latitude. '
                             'If not set it will be generated randomly',
                        default=uniform(-180, 180)
                        )

    parser.add_argument('-long', action='store',
                        type=validate_longtitude,
                        dest='longtitude',
                        help='You longtitude. '
                             'If not set it will be generated randomly',
                        default=uniform(0, 360)
                        )
    params = parser.parse_args()

    if params.flag_download:
        bars_data = download_bars_json()
        print('Download from Devman')
    else:
        print('Load from file')
        bars_data = load_data(params.filepath)
    if bars_data:
        print('Наибольший бар: {}'.format(get_biggest_bar(bars_data)))
        print('Наименьший бар: {}'.format(get_smallest_bar(bars_data)))
        print('Ближайший бар: {}'.format(
            get_closest_bar(bars_data, params.latitude, params.longtitude)))
