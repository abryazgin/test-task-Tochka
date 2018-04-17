# [Задача](https://github.com/Life1over/test-task/blob/master/python.md):

## Само задание: 
- [http://www.nasdaq.com/symbol/cvx/historical](http://www.nasdaq.com/symbol/cvx/historical)
- [http://www.nasdaq.com/symbol/cvx/insider-trades](http://www.nasdaq.com/symbol/cvx/insider-trades)

### Вводная.
 Это страницы с финансовыми данными компании Chevron Corporation(CVX). CVX - название акции, которая торгуется. Если заменить на AAPL  - получим данные об Apple Inc.

Дано:
- **файл tickers.txt, в котором в каждой строке записана акция(CVX, AAPL, GOOG, etc...)**
1. Спроектировать архитектуру БД для хранения данных о ценах акций и торговых операциях совладельцев компании.
    * Для перечисленных в файле акций спарсить данные цен акции за 3 месяца и сохранить в БД. Парсер должен принимать аргумент N - количество потоков, в которых он должен выполнять работу.
    * Для перечисленных акций спарсить insider-trades и сохранить в БД. Это данные о торговле совладельцев компании. Данные insider-trades разделены на страницы. Необходимо спарсить с 1 по 10 страницы. Если страниц меньше - все, что есть.
2. Создать веб-интерфейс, который на / будет отдавать веб-страницу со ссылками на акции, доступные в базе данных.
3. создать веб-интерфейс, который на /%TICKER% будет отдавать веб-страницу с таблицей цен на акцию за 3 месяца
4. Создать веб-интерфейс, который на /%TICKER%/insider будет отдавать веб-страницу с данными торговли владельцев компании. На эту страницу попадать по ссыле со страницы /%TICKER%/
5. Создать веб-интерфейс, который на /%TICKER%/insider/%NAME% будет отдавать веб-страницу с данными о торговле данного владельца компании. На эту страницу попадать по ссылке со страницы /%TICKER%/insider
6. Создать веб-интерфейс, который на /%TICKER%/analytics?date_from=..&date_to=... будет отдавать веб-страницу с данными о разнице цен в текущих датах(нужна разница всех цен - открытия, закрытия, максимума, минимума)
7. Создать веб-интерфейс, который на /%TICKER/delta?value=N&type=(open/high/low/close) будет отдавать веб-страницу с данными о минимальных периодах (дата начала-дата конца), когда указанная цена изменилась более чем на N
Например, с первого по пятое число месяца цена акции прирастала на 2 доллара в день, затем два дня падала на 1 доллар(до 7 числа), и затем выросла на 3 доллара(к 8 числу). 9 числа цена упала на 5 долларов.
Задана разница - 11 долларов. Необходимо показать интервал 1 - 8 число.
Если бы 9 числа цена не упала, а приросла на 5 долларов - минимальный интервал все равно останется с 1 по 8 число.
8.  Для задач 2-3-4-5-6-7 сделать вызовы с префиксом /api/... , которые отдадут те же данные, но в формате JSON

## **P.S.**
-	К верстке претензий нет - лишь бы было функционально
-	Использовать PostgreSQL
-	ORM любая на выбор
- Задачу 7 желательно решать средствами SQL, так интереснее



# Краткое описание решения:

1. Использовал:
 * Python 3.5.2
 * Фреймворк - Flask
 * ORM - Flask-SQLAlchemy
 * DB - PostgreSQL
 
2. Структура БД и скрипт парсинга
    1. Структура БД [тут](https://github.com/bryazginnn/test-task-Tochka/blob/master/src/database/models.py)
    1. Скрипт парсинга данных по акциям с сайта [тут](https://github.com/bryazginnn/test-task-Tochka/blob/master/bin/parse_using_file.py). Пример использования:
    
    ```bash
    (venv) abryazgin@abryazgin:~/my/git/test-task-Tochka$ python ./bin/parse_using_file.py symbol_list.txt 3
    DOWNLOADING: https://www.nasdaq.com/symbol/cvx/historical
    DOWNLOADING: https://www.nasdaq.com/symbol/cvx/insider-trades?page=1
    DOWNLOADING: https://www.nasdaq.com/symbol/aapl/historical
    DOWNLOADING: https://www.nasdaq.com/symbol/aapl/insider-trades?page=1
    DOWNLOADING: https://www.nasdaq.com/symbol/goog/historical
    DOWNLOADING: https://www.nasdaq.com/symbol/goog/insider-trades?page=1
    DOWNLOADING: https://www.nasdaq.com/symbol/cvx/insider-trades?page=2
    DOWNLOADING: https://www.nasdaq.com/symbol/cvx/insider-trades?page=3
    DOWNLOADING: https://www.nasdaq.com/symbol/cvx/insider-trades?page=4
    DOWNLOADING: https://www.nasdaq.com/symbol/cvx/insider-trades?page=7
    DOWNLOADING: https://www.nasdaq.com/symbol/cvx/insider-trades?page=6
    DOWNLOADING: https://www.nasdaq.com/symbol/cvx/insider-trades?page=5
    DOWNLOADING: https://www.nasdaq.com/symbol/aapl/insider-trades?page=2
    DOWNLOADING: https://www.nasdaq.com/symbol/aapl/insider-trades?page=3
    DOWNLOADING: https://www.nasdaq.com/symbol/aapl/insider-trades?page=5
    DOWNLOADING: https://www.nasdaq.com/symbol/aapl/insider-trades?page=7
    DOWNLOADING: https://www.nasdaq.com/symbol/aapl/insider-trades?page=9
    DOWNLOADING: https://www.nasdaq.com/symbol/aapl/insider-trades?page=4
    DOWNLOADING: https://www.nasdaq.com/symbol/aapl/insider-trades?page=6
    DOWNLOADING: https://www.nasdaq.com/symbol/aapl/insider-trades?page=10
    DOWNLOADING: https://www.nasdaq.com/symbol/aapl/insider-trades?page=8
    DOWNLOADING: https://www.nasdaq.com/symbol/goog/insider-trades?page=2
    DOWNLOADING: https://www.nasdaq.com/symbol/goog/insider-trades?page=3
    DOWNLOADING: https://www.nasdaq.com/symbol/goog/insider-trades?page=5
    DOWNLOADING: https://www.nasdaq.com/symbol/goog/insider-trades?page=7
    DOWNLOADING: https://www.nasdaq.com/symbol/goog/insider-trades?page=6
    DOWNLOADING: https://www.nasdaq.com/symbol/goog/insider-trades?page=4
    DOWNLOADING: https://www.nasdaq.com/symbol/goog/insider-trades?page=8
    DOWNLOADING: https://www.nasdaq.com/symbol/goog/insider-trades?page=9
    DOWNLOADING: https://www.nasdaq.com/symbol/goog/insider-trades?page=10
    ```
3. Установка:
```bash
# качаем
git clone git@github.com:bryazginnn/test-task-Tochka.git test_task
# ставим
cd test_task
virtualenv venv -p python3
source venv/bin/activate
pip install -r requirements.txt
# создаем БД
python ./db/create_db.py
# парсим
python ./bin/parse_using_file.py symbol_list.txt 3
# запускаем
FLASK_APP='src/main.py' flask run
# заходим на http://127.0.0.1:5000/
``` 
