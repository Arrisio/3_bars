# Ближайшие бары

Скрипт выполняет следующие функции
1) Возвращает бар с наибольшим кол-вом посадочных мест
2) Возвращает бар с наименьшим кол-вом посадочных мест
3) Возвращает  бар, ближайшей к точке , координаты которой будут указаны при запуске скрипты.

Для работы требуются данные о барах, файл с которыми находится в текущей директории.
Если необходимо, данные можно скачать с сайта [devman](https://devman.org/) или https://apidata.mos.ru/v1/features/1796?api_key={place_your_API_key_here} (нужен выданый при регистрации токен)

# Как запустить

Скрипт требует для своей работы установленного интерпретатора Python версии 3.5

Запуск на Linux:

```bash
$ python bars.py # possibly requires call of python3 executive instead of just python
usage: bars.py [-h] [-d] [-f FILEPATH] [-lat LATITUDE] [-long LONGTITUDE]

optional arguments:
  -h, --help        show this help message and exit
  -f FILEPATH       Filepath with data, "bars.json" by default
  -lat LATITUDE     You latitude. If not set it will be generated randomly
  -long LONGTITUDE  You longtitude. If not set it will be generated randomly

```

```bash
$ python bars.py -f bars.json -lat 55.56 -long 37.643
Наибольший бар: Спорт бар «Красная машина»
Наименьший бар: БАР. СОКИ
Ближайший бар: БАР «ПИВНОЙ ПОГРЕБОК»

Process finished with exit code 0
```

Запуск на Windows происходит аналогично.

# Цели проекта

Код создан в учебных целях. В рамках учебного курса по веб-разработке - [DEVMAN.org](https://devman.org)
