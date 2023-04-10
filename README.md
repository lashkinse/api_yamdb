# Проект YaMDb (api_yamdb)

[![Python](https://img.shields.io/badge/-Python-464641?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-464646?style=flat-square&logo=django)](https://www.djangoproject.com/)
[![Pytest](https://img.shields.io/badge/Pytest-464646?style=flat-square&logo=pytest)](https://docs.pytest.org/en/6.2.x/)
[![Postman](https://img.shields.io/badge/Postman-464646?style=flat-square&logo=postman)](https://www.postman.com/)

![python version](https://img.shields.io/badge/Python-3.9-green)
![django version](https://img.shields.io/badge/Django-2.2-green)
![pyjwt version](https://img.shields.io/badge/PyJWT-2.1-green)
![pytest version](https://img.shields.io/badge/pytest-6.2-green)
![requests version](https://img.shields.io/badge/requests-2.26-green)

## Описание

Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя
посмотреть фильм или послушать музыку.
Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Например, в категории «Книги» могут быть
произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Жуки» и
вторая сюита Баха. Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство»
или «Ювелирка»).
Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»).
Добавлять произведения, категории и жанры может только администратор.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в
диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения —
рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.
Пользователи могут оставлять комментарии к отзывам.
Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.

## YaMDb API

Доступ к БД проекта осуществляется через Api.
Полный список запросов и эндпоинтов описан в документации ReDoc, доступна после запуска проекта по адресу:

```
http://127.0.0.1:8000/redoc/
```

## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/lashkinse/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source env/scripts/activate
    ```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить первоначальную загрузку справочников:

```
python3 manage.py importcsv
```

Запустить проект:

```
python3 manage.py runserver
```
