### Парсер, который асинхронно скачивает бюллетень по итогам торгов с сайта [биржи](https://spimex.com/markets/oil_products/trades/results/) и записывает данные в базу данных

### Запуск проекта

Для запуска проекта в корневой директории необходимо создать файл *.env*, пример в файле [**env.example**](https://github.com/Harukakuraharu/4_Asyncio/blob/main/env.example)

Далее нужно локально инициализировать базу данных, *если **postgresql** неустановлен локально*:
```
docker compose up --build -d
```

Для создания виртуального окружения:
```
python -m venv .venv
```
Активация виртуальной среды для OC Linux:
```
source .venv/bin/activate
```
Активация виртуальной среды для OC Windows:
```
venv\Scripts\activate
```
Установка зависимостей:
```
pip install poetry
poetry install
```

### Запуск приложения
```
python main.py
```

Eсли нужно открыть контейнер c базой данных в консоли:
```
docker compose exec имя_контейнера psql -U имя_пользователя имя_бд
```
Или посмотреть данные можно через pgAdmin по ссылке **localhost:80**, логин и пароль указаны в файле [**docker-compose.yaml**](https://github.com/Harukakuraharu/4_Asyncio/blob/main/docker-compose.yaml) в *PGADMIN_DEFAULT_EMAIL* и *PGADMIN_DEFAULT_PASSWORD*. Данные для подключения к БД в [**env.example**](https://github.com/Harukakuraharu/4_Asyncio/blob/main/env.example)

*Удалять файлы не нужно, после прочтения файла и записи в БД, файлы удаляются автоматически*


### Сравнение асинхронного и синхронного парсера

1. [Асинхронный парсер](https://github.com/Harukakuraharu/4_Asyncio/blob/main/async_parser.jpg)
2. [Синхронный парсер](https://github.com/Harukakuraharu/4_Asyncio/blob/main/sync_parser.jpg)