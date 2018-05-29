import json
import argparse
from random import uniform
from functools import partial


def load_data(filepath):
    with open(filepath, 'r', encoding='UTF8') as file_handler:
        return json.load(file_handler)['features']


def get_biggest_bar(bars_data):
    return max(
        bars_data,
        key=lambda bar: bar['properties']['Attributes']['SeatsCount']
    )


def get_smallest_bar(bars_data):
    return min(
        bars_data,
        key=lambda bar: bar['properties']['Attributes']['SeatsCount']
    )


def get_closest_bar(bars_data, longtitude, latitude):
    return min(
        bars_data, key=lambda bar:
        (bar['geometry']['coordinates'][0] - longtitude) ** 2 +
        (bar['geometry']['coordinates'][1] - latitude) ** 2
    )


def validate_gps_coord(coordinate, gps_coord_metadata):
    try:
        coordinate = float(coordinate)
    except ValueError:
        raise argparse.ArgumentTypeError('Coordinate is not numeric')

    if (
            coordinate < gps_coord_metadata['min_val'] or
            coordinate > gps_coord_metadata['max_val']
    ):
        raise argparse.ArgumentTypeError(
            '{} must be between  {} and {} degrees'.format(
                gps_coord_metadata['name'],
                gps_coord_metadata['min_val'],
                gps_coord_metadata['max_val'])
        )
    return coordinate


def parse_arguments():
    latitude_metadata = {
        'name': 'Latitude', 'min_val': -90, 'max_val': 90
    }
    longtitude_metadata = {
        'name': 'Longtitude', 'min_val': -180, 'max_val': 180
    }

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-f', action='store',
        dest='filepath',
        help='Filepath with data, "bars.json" by default',
        default='bars.json'
    )

    parser.add_argument(
        '-lat', action='store',
        type=partial(
            validate_gps_coord,
            gps_coord_metadata=latitude_metadata
        ),
        dest='latitude',
        help='You latitude. If not set, it will be generated randomly',
        default=uniform(
            latitude_metadata['min_val'],
            latitude_metadata['max_val'],
        )
    )

    parser.add_argument(
        '-long', action='store',
        type=partial(
            validate_gps_coord,
            gps_coord_metadata=longtitude_metadata
        ),
        dest='longtitude',
        help='You longtitude. If not set it will be generated randomly',
        default=uniform(
            longtitude_metadata['min_val'],
            longtitude_metadata['max_val']
        )

    )

    return parser.parse_args()


if __name__ == '__main__':
    params = parse_arguments()

    try:
        bars_data = load_data(params.filepath)
    except ValueError:
        exit('can not read file {}'.format(params.filepath))
    except OSError:
        exit('File {} not exists '.format(params.filepath))

    print('Bigger ber: {}'.format(
        get_biggest_bar(bars_data)['properties']['Attributes']['Name'])
    )
    print('Smallest bar: {}'.format(
        get_smallest_bar(bars_data)['properties']['Attributes']['Name'])
    )
    print('Closest bar: {}'.format(
        get_closest_bar(bars_data, params.longtitude, params.latitude
                        )['properties']['Attributes']['Name']
        )
    )
