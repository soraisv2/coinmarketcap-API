# Coinmarketcap API basic usage

[![Python 3.9.6](https://img.shields.io/badge/python-3.9-blueviolet)](https://www.python.org/)

---

You just have to put your api key and execute like :

    ./api.py 5 55

---
```python
    def getDataApi():
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        parameters = {
            'start':'1',
            'limit':'55',
            'convert':'USD'
        }
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': '[YOUR API KEY]', # <==================
        }

        session = Session()
        session.headers.update(headers)

        try:
            response = session.get(url, params=parameters)
            return(response.text)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)
```
