import os
import pickle
import requests

# Query the kd-tree for nearest neighbors
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.KDTree.query.html
import scipy.spatial as spatial


def load_data(filepath):
    print("Введите свой токен для сайта apidata.mos.ru")
    url = 'https://apidata.mos.ru/v1/features/1796'
    rest_params = {'api_key': input()}
    try:
        request_response = requests.get(url, params=rest_params)
        request_data = request_response.json()
        points_tree = spatial.KDTree(
            [bar.get('geometry').get('coordinates')
             for bar in request_data.get('features')]
        )
        bars_names =\
            [bar.get('properties').get('Attributes').get('Name')
             for bar in request_data.get('features')]
        bars_seat_counts = \
            [bar.get('properties').get('Attributes').get('SeatsCount')
             for bar in request_data.get('features')]

        pickle.dump(file=open(filepath, 'wb'),
                    obj=(bars_names, bars_seat_counts, points_tree))
        print('Данные о барах и их геокоординаты записаны в файл {}'
              .format(filepath))

    except ValueError as e:
        print("Не могу скачать или рапокавать данные."
              " Проверте в браузере сформированный URL {}".format(url))


def get_biggest_bar(filepath):
    (bars_names, bars_seat_counts, _) = pickle.load(open(filepath, 'rb'))
    max_seats = max(bars_seat_counts)
    print("Наибольшый бар: {} , кол-во мест: {}"
              .format(bars_names[bars_seat_counts.index(max_seats)], max_seats)
              )


def get_smallest_bar(filepath):
    (bars_names, bars_seat_counts, _) = pickle.load(open(filepath, 'rb'))
    min_seats = min(bars_seat_counts)
    print("Наименьший бар: {} , кол-во мест: {}"
          .format(bars_names[bars_seat_counts.index(min_seats)], min_seats))


def get_closest_bar(filepath):
    (bars_names, bars_seat_counts, points_tree) =\
        pickle.load(open(filepath, 'rb'))
    (default_longtitude, default_latitude) = points_tree.data.mean(axis=0)
    print("Введите вашу широту (по умолчанию {})".format(default_latitude))
    latitude = float(input() or default_latitude)
    print("Введите вашу долготу (по умолчанию {})".format(default_longtitude))
    longitude = float(input() or default_longtitude)
    (distance, idx) = points_tree.query((longitude, latitude), k=1)
    # distance * 111e3  , т.к. в одном градусе 111 км.
    print(" Ближайший бар {}, расстояние до него {:.0f} метров"
          .format(bars_names[idx], distance * 111e3)
          )


def enter_filepath():
    default_file_path = os.path.join(os.getcwd(), 'bars_geodata.pkl')
    print("Введите путь к файлу (по умолчанию {})".format(default_file_path))
    return input() or default_file_path


if __name__ == '__main__':
    start_ms = """Введите одну из комманд:
        load_data        : Загрузка данных с apidata.mos.ru/
        get_biggest_bar  : Возвращает бар с наибольшим кол-вом посадочных мест
        get_smallest_bar : Возвращает бар с наименьшим кол-вом посадочных мест
        get_closest_bar  : возвращает ближайший бар и расстояние до него"""
    print(start_ms)
    mission = input()
    if mission == 'load_data':
        data_file = enter_filepath()
        load_data(data_file)
    elif mission == 'get_biggest_bar':
        data_file = enter_filepath()
        get_biggest_bar(data_file)
    elif mission == 'get_smallest_bar':
        data_file = enter_filepath()
        get_smallest_bar(data_file)
    elif mission == 'get_closest_bar':
        data_file = enter_filepath()
        get_closest_bar(data_file)
    else:
        print('неправильная комманда')
