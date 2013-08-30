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
[{'company': 'ОАО «Газпромбанк»',
  'id': '61',
  'link': [{'href': 'http://api.uslugi.yandex.ru/1.0/banks/61', 'rel': 'self'},
   {'href': 'http://www.gazprombank.ru/', 'rel': 'www'},
   {'href': 'http://www.cbr.ru/credit/coinfo.asp?id=450000661',
    'rel': 'cbrf'}],
  'name': 'Газпромбанк',
  'rating': {'stars': '5.0', 'value': 'Aaa'}},
…
]
```

### Get more detailed info by ID

```python
>>> b.get(123, region="Москва")
{'company': 'ЗАО «АКБ «Век»',
 'deposits': {'deposit': {'id': '305427',
   'link': [{'href': 'http://api.uslugi.yandex.ru/1.0/banks/deposits/305427',
     'rel': 'self'},
    {'href': 'http://www.vek.ru/index.php?view=78', 'rel': 'www'}],
   'name': 'Сберегательный'}},
 'id': '102306',
 'link': [{'href': 'http://api.uslugi.yandex.ru/1.0/banks/102306',
   'rel': 'self'},
  {'href': 'http://www.vek.ru/', 'rel': 'www'},
  {'href': 'http://www.cbr.ru/credit/coinfo.asp?id=450000366', 'rel': 'cbrf'}],
 'name': 'Век',
 'phone': '(495) 411-55-30',
 'rating': {'stars': None, 'value': None}}
```

### Search for credits

```python
>>> c = yu.BankCredit('YOURKEY', 'http://your.referer')
>>> c.find(region="Москва", currency='RUB', sum=1000, period='1 years')
[{'additional-info': {'credit-delivery': {'mode': 'FLAT_PAYMENT'}},
  'advanced-repayment': {'scheme': 'PARTIAL_AND_WHOLE'},
  'bank': {'company': 'ООО ИКБ «Совкомбанк»',
   'id': '17241',
   'link': [{'href': 'http://api.uslugi.yandex.ru/1.0/banks/17241',
     'rel': 'self'},
    {'href': 'http://www.sovcombank.ru/', 'rel': 'www'},
    {'href': 'http://cbr.ru/credit/coinfo.asp?id=340000004', 'rel': 'cbrf'}],
   'name': 'Совкомбанк',
   'rating': {'stars': None, 'value': None}},
  'credit-security': {'guarantee-need': 'NOT_REQUIRED',
   'pledge-need': 'NOT_REQUIRED'},
  'debtor-requirements': {'citizenship': None,
   'debtor': [{'gender': 'MALE', 'max-repayment-age': '70', 'min-age': '20'},
    {'gender': 'FEMALE', 'max-repayment-age': '70', 'min-age': '20'}],
   'home-phone': None,
   'job-phone': None,
   'last-work-experience': 'Не менее 4 месяцев.',
   'registration': 'PERMANENT_REGION'},
  'id': '267405',
  'link': [{'href': 'http://api.uslugi.yandex.ru/1.0/banks/credits/267405',
    'rel': 'self'},
   {'href': 'http://credit.sovcombank.ru/tovarnyj_kredit', 'rel': 'www'}],
  'locus-contractus': 'BANK_OFFICE',
  'name': 'Товарный кредит',
  'other-provided-documents': {'comment': 'Один документ из следующего списка: свидетельство о постановке на учет в налоговом органе, страховой медицинский полис, водительское удостоверение, удостоверение личности офицера, военный билет, заграничный паспорт, страховое пенсионное свидетельство, пенсионное удостоверение.',
   'documents': {'document': [{'required': 'OBLIGATORY', 'value': 'PASSPORT'},
     {'required': 'CHOOSINGLY', 'value': 'MILITARY_ID'},
     {'required': 'CHOOSINGLY', 'value': 'INN'},
     {'required': 'CHOOSINGLY', 'value': 'PENSION_INSURANCE_CERTIFICATE'},
     {'required': 'CHOOSINGLY', 'value': 'INTERNATIONAL_PASSPORT'},
     {'required': 'CHOOSINGLY', 'value': 'DRIVING_LICENSE'},
     {'required': 'CHOOSINGLY', 'value': 'OTHER_DOCUMENTS'}]}},
  'payment': {'methods': {'method': ['CLEARING_BASIS_PAYMENT',
     'RUSSIAN_POST',
     'BANK_OFFICE']},
   'scheme': 'ANNUITY'},
  'purpose': 'GOODS',
  'short': {'first-payment': '169.89',
   'min-initial-instalment': '0.0',
   'month-payment': '86.56',
   'overpayment': '38.71',
   'rate': {'max-value': '45.0', 'min-value': '7.07'}}},
…
]
```

Using `get` method you'd get JSON-like object. You can access fields by both `__getitem__` and `__getattr__` methods (var['item'] and var.attr syntax). In case of `all` and `find` that'd be list of such objects.

References
----------

1. Check out [Ruby implementation](https://github.com/sld/yandex_uslugi_wrapper)
