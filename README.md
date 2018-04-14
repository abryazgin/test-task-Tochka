1. Структура БД и скрипт парсинга
    1. Структура БД [тут](https://github.com/bryazginnn/test-task-Tochka/blob/master/src/database/models.py)
    1. Скрипт парсинга данных по акциям с сайта [тут](https://github.com/bryazginnn/test-task-Tochka/blob/master/bin/parse_using_file.py). Пример использования:
    
    ```bash
    (venv) abryazgin@abryazgin:~/my/git/test-task-Tochka$ python ./bin/parse_using_file.py symbol_list.txt 20
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
1. 