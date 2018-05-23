import json
import os
import pickle
import requests
import numpy as np
import scipy.spatial as spatial  # Query the kd-tree for nearest neighbors https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.KDTree.query.html#scipy.spatial.KDTree.query

def load_data(filepath):
    print ("Введите свой токен для сайта apidata.mos.ru")
    token = input()
    url = 'https://apidata.mos.ru/v1/features/1796?api_key='+token
    try:
        request_response = requests.get(url)
        data = json.loads(request_response.content.decode('utf-8'))
        geopos_KDTree = spatial.KDTree([i.get('geometry').get('coordinates') for i in data.get('features')])
        bars_names = [i.get('properties').get('Attributes').get('Name') for i in data.get('features')]
        bars_seat_counts = np.array([i.get('properties').get('Attributes').get('SeatsCount') for i in data.get('features')])

        with open(filepath, 'wb') as file:
            pickle.dump(file=file, obj=(bars_names, bars_seat_counts, geopos_KDTree))
            print ('Данные о барах и их геокоординаты записаны в файл {}'.format(filepath))

    except Exception as e:
        print("Не могу скачать или рапокавать данные. Попробуйте проверить в браузере сформированный URL {}".format(url))

def get_biggest_bar(filepath):
    with open(filepath, 'rb') as file:
        (bars_names, bars_seat_counts, _) = pickle.load(file)
        idx = np.argmax(bars_seat_counts)
        print ("Наибольшый бар: {} , кол-во мест: {}".format(bars_names[idx],bars_seat_counts[idx]))

def get_smallest_bar(filepath):
    with open(filepath, 'rb') as file:
        (bars_names, bars_seat_counts, _) = pickle.load(file)
    idx = np.argmin(bars_seat_counts)
    print("Наименьший бар: {} , кол-во мест: {}".format(bars_names[idx], bars_seat_counts[idx]))

def get_closest_bar(filepath):
    with open(filepath, 'rb') as file:
        (bars_names, bars_seat_counts, geopos_KDTree) = pickle.load(file)
    default_latitude = geopos_KDTree.data[0][1]
    default_longtitude = geopos_KDTree.data[0][0]
    print("Введите вашу широту (по умолчанию {})".format(default_latitude))
    latitude = float(input() or default_latitude)
    print("Введите вашу долготу (по умолчанию {})".format(default_longtitude))
    longitude = float(input() or default_longtitude)
    (distance, idx) = geopos_KDTree.query((longitude, latitude), k=1)
    print (" Ближайший бар {}, расстояние до него {:.0f} метров".format(bars_names[idx], distance * 111e3))

def enter_filepath():
    default_file_path = os.path.join(os.getcwd(),'bars_geodata.pkl')
    print ("Введите путь к файлу (по умолчанию {}) ".format(default_file_path ))
    file = input()
    return file or default_file_path

if __name__ == '__main__':
    default_ms= """Введите одну из комманд: 
        load_data        : Загрузка данных с apidata.mos.ru/ 
        get_biggest_bar  : возвращает наибольший бар и его геокоордлинаты 
        get_smallest_bar : возвращает наименьший бар и его геокоордлинаты
        get_closest_bar  : возвращает ближайший бар и его геокоордлинаты"""
    print(default_ms)
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