import json
import argparse
from random import uniform
from functools import partial


def load_data(filepath):
    with open(filepath, 'r', encoding='UTF8') as file_handler:
        return json.load(file_handler)['features']


def get_biggest_bar(bars_data):
    return max(bars_data,
               key=lambda bar: bar['properties']['Attributes']['SeatsCount']
               )


def get_smallest_bar(bars_data):
    return min(bars_data,
               key=lambda bar: bar['properties']['Attributes']['SeatsCount']
               )


def get_closest_bar(bars_data, longtitude, latitude):
    return min(
        bars_data, key=lambda bar:
        (bar['geometry']['coordinates'][0] - longtitude) ** 2 +
        (bar['geometry']['coordinates'][1] - latitude) ** 2
    )


def validate_gps_coord(coordinate, coord_type):
    coordinate = float(coordinate)

    gps_coord_metadata = {
        'Latitude': {'min_val': -90, 'max_val': 90},
        'Longtitude': {'min_val': -180, 'max_val': 180}
    }

    min_val = gps_coord_metadata[coord_type]['min_val']
    max_val = gps_coord_metadata[coord_type]['max_val']
    if coordinate < min_val or coordinate > max_val:
        raise argparse.ArgumentTypeError(
            '{} must be between  {} and {} degrees'.format(
                coord_type, min_val, max_val)
        )
    return coordinate


validate_latitude = partial(validate_gps_coord, coord_type='Latitude')
validate_longtitude = partial(validate_gps_coord, coord_type='Longtitude')


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-f', action='store',
        dest='filepath',
        help='Filepath with data, "bars.json" by default',
        default='bars.json'
    )

    parser.add_argument(
        '-lat', action='store',
        type=validate_latitude,
        dest='latitude',
        help='You latitude. If not set, it will be generated randomly',
        default=uniform(-90, 90)
    )

    parser.add_argument(
        '-long', action='store',
        type=validate_longtitude,
        dest='longtitude',
        help='You longtitude. If not set it will be generated randomly',
        default=uniform(-180, 180)
    )

    return parser.parse_args()


if __name__ == '__main__':
    params = parse_arguments()

    try:
        bars_data = load_data(params.filepath)
    except ValueError:
        exit('Не могу прочитать данные из файла {}'.format(params.filepath))
    except OSError:
        exit('Файл {} не существует '.format(params.filepath))

    print('Наибольший бар: {}'.format(
        get_biggest_bar(bars_data)['properties']['Attributes']['Name'])
    )
    print('Наименьший бар: {}'.format(
        get_smallest_bar(bars_data)['properties']['Attributes']['Name'])
    )
    print('Ближайший бар: {}'.format(
        get_closest_bar(bars_data, params.longtitude, params.latitude
                        )['properties']['Attributes']['Name']
        )
    )
