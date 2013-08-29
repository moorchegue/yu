圄 aka Yandex Uslugi
====================

`圄` is a tiny client on [Yandex Uslugi API](http://api.yandex.ru/uslugi/doc/banks-dg/concepts/about.xml)

Installation
------------

```sh
$ git clone https://github.com/moorchegue/yu.git
$ python setup.py develop
```

Usage
-----

First check out Yandex docs to figure out what are key and referer.

There are five user classes available:

1. `Bank`
2. `BankDeposit`
3. `BankCredit`
4. `BankAutoCredit`
5. `BankMortgage`

All of those supports `get` method. `Bank` supports `all`, and other four supports `find`.

For long boring lists of required and acceptable arguments of each check out the code.

So:

```python
>>> import yu
```

### Get all banks

```python
>>> b = yu.Bank('YOURKEY', 'http://your.referer')
>>> b.all(region="Москва")
b'<?xml version="1.0" encoding="UTF-8"?>\n<banks>…'
```

### Get more detailed info by ID

```python
>>> b.get(123, region="Москва")
b'<?xml version="1.0" encoding="UTF-8"?>\n<bank>…'
```

### Search for deposits

```python
>>> c = yu.BankCredit('YOURKEY', 'http://your.referer')
>>> c.find(region="Москва", currency='RUB', sum=1000, period='1 years')
b'<?xml version="1.0" encoding="UTF-8"?>\n<credits>…'
```

In every case you'll get a string of ugly raw `XML`. So you can use any XML library to work with it or e.g. [xmltodict](https://github.com/martinblech/xmltodict) or something like that.

References
----------

1. Check out [Ruby implementation](https://github.com/sld/yandex_uslugi_wrapper)
