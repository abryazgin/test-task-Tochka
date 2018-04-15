1. Использовал:
 * Python 3.5.2
 * Фреймворк - Flask
 * ORM - Flask-SQLAlchemy
 * DB - PostgreSQL
 
2. Пункт 7 решен НЕ НА SQL. 
Считаю имеет смысл переиспользовать п.6 и 
избежать логики на SQL. За счет этого осталось неважно 
какая БД используется.  
При необходимости могу все подготовить решение п.7 на уровне SQL 
(прошу дать знать, если будет такая необходимость)

3. Структура БД и скрипт парсинга
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
4. Установка (при необходимости придется изменить URI к БД):
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
