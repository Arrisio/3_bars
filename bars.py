import os
import json
import argparse

def enter_filepath():
    default_file_path = os.path.join(os.getcwd(), 'bars.json')
    print('Введите путь к файлу (по умолчанию {})'.format(default_file_path))
    # return input() or default_file_path
    return default_file_path


def load_data(filepath):
    return json.load(open(filepath, 'r', encoding='UTF8')).get('features')


def get_biggest_bar(bars_data):
    return max(bars_data,
               key=lambda bar: bar['properties']['Attributes']['SeatsCount'])\
        ['properties']['Attributes']['Name']


def get_smallest_bar(bars_data):
    return min(bars_data,
               key=lambda bar: bar['properties']['Attributes']['SeatsCount'])\
        ['properties']['Attributes']['Name']


def get_closest_bar(bars_data, longtitude, latitude ):
    return min(bars_data, key=lambda bar:
        (bar['geometry']['coordinates'][0] - longtitude) ** 2 +
        (bar['geometry']['coordinates'][1] - latitude) ** 2)\
        ['properties']['Attributes']['Name']


if __name__ == '__main__':
    filepath = enter_filepath()
    bars_data = load_data(filepath)

    print('Наибольший бар: {}'.format(get_biggest_bar(bars_data)))
    print('Наименьший бар: {}'.format(get_smallest_bar(bars_data)))

    default_latitude = 55.748861154831935
    default_longtitude = 37.594104911195
    print('Введите вашу широту (по умолчанию {})'.format(default_latitude))
    # latitude = float(input() or default_latitude)

    print('Введите вашу долготу (по умолчанию {})'.format(default_longtitude))
    # longtitude = float(input() or default_longtitude)

    print('Ближайший бар: {}'.format(get_closest_bar(bars_data,
                                                     default_longtitude, default_latitude)))
