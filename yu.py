from functools import reduce

import requests
from xmltodict import parse


API_SITE = "http://api.uslugi.yandex.ru"
API_VERSION = "1.0"


class YandexUslugiBase(object):
    """ Yandex Uslugi base class.
    """

    headers = {}
    resource = ''
    url = ''

    _required_get = ()
    _acceptable_get = ('key', )
    _get_path = []

    def __init__(self, key, referer, version=API_VERSION):
        self.headers = {
            'Authorization': key,
            'Referer': referer,
        }
        self.url = '%s/%s/%s' % (API_SITE, version, self.resource)

    def get(self, id_, *args, **kwargs):
        self._validate(self._required_get, self._acceptable_get, kwargs)
        url = '%s/%s' % (self.url, id_)
        data = self._get_response(url, kwargs)
        return reduce(dict.get, self._get_path, data)

    def _get_response(self, url, params):
        response = requests.get(url, params=params, headers=self.headers)
        data = parse(response.content, dict_constructor=AttrDict, attr_prefix='', cdata_key='value')

        if response.status_code is not 200:
            raise error_factory(response.status_code, data.error.message, data.error.comment)

        return data

    def _validate(self, required, acceptable, actual):
        """ Check actual request fields to be necessary and sufficient.
        """
        for field in required:
            if field not in actual:
                raise AttributeError('%s field is required' % field)

        for field in actual:
            if field not in required + acceptable:
                raise AttributeError('%s field is not accepted' % field)


class YandexUslugiSearcheable(object):
    _required_search = ('region', )
    _acceptable_search = ('key')
    _list_path = []

    def find(self, *args, **kwargs):
        self._validate(self._required_search, self._acceptable_search, kwargs)
        url = '%s/%s' % (self.url, 'search')
        data = self._get_response(url, kwargs)
        return reduce(dict.get, self._list_path, data)


class YandexUslugiListable(object):
    _required_all = ('region', )
    _acceptable_all = ('key', )
    _list_path = []

    def all(self, *args, **kwargs):
        self._validate(self._required_all, self._acceptable_all, kwargs)
        data = self._get_response(self.url, kwargs)
        return reduce(dict.get, self._list_path, data)


class Bank(YandexUslugiBase, YandexUslugiListable):
    resource = 'banks'
    _get_path = ['bank']
    _list_path = ['banks', 'bank']
    _required_get = ('region', )


class BankDeposit(YandexUslugiBase, YandexUslugiSearcheable):
    resource = 'banks/deposits'
    _get_path = ['deposit']
    _list_path = ['deposits', 'deposit']
    _required_search = ('region', 'currency', 'sum', 'period')
    _acceptable_search = (
        'key',
        'currency',
        'sum',
        'period',
        'restrictions',
        'banks',
        'start',
        'limit',
        'order',
        'replenishment',
        'capitalization',
        'partial-withdrawal',
        'min-balance',
        'auto-prolongation',
        'multicurrency',
        'pensionary',
        'payment-of-interest',
    )


class BankCredit(YandexUslugiBase, YandexUslugiSearcheable):
    resource = 'banks/credits'
    _get_path = ['credit']
    _list_path = ['credits', 'credit']
    _required_search = (
        'region',
        'currency',
        'sum',
        'period',
    )
    _acceptable_search = (
        'key',
        'restrictions',
        'banks',
        'start',
        'limit',
        'order',
        'advanced-repayment',
        'without-penalty',
        'without-moratorium',
        'without-guarantee',
        'without-additional-fee',
        'without-life-insurance',
        'no-citizenship',
        'proof-of-income',
        'proof-docs',
        'payment-scheme',
        'decision-period',
        'purpose',
        'without-pledge',
        'cash',
    )


class BankAutoCredit(YandexUslugiBase, YandexUslugiSearcheable):
    resource = 'banks/autocredits'
    _get_path = ['autocredit']
    _list_path = ['autocredits', 'autocredit']
    _required_search = (
        'region',
        'currency',
        'sum',
        'period',
        'restrictions',
        'banks',
        'start',
        'limit',
        'order',
        'advanced-repayment',
        'without-penalty',
        'without-moratorium',
        'without-guarantee',
        'without-additional-fee',
        'without-life-insurance',
        'no-citizenship',
        'proof-of-income',
        'proof-docs',
        'payment-scheme',
        'decision-period',
    )
    _acceptable_search = (
        'key',
        'min-initial-instalment',
        'instalment-in-percents',
        'vehicle-type',
        'vendor-type',
        'age-type',
        'without-kasko',
        'seller',
        'state-program',
        'refinancing',
    )


class BankMortgage(YandexUslugiBase, YandexUslugiSearcheable):
    resource = 'banks/mortage'
    _get_path = ['mortages']
    _list_path = ['mortages', 'mortage']
    _required_search = (
        'region',
        'currency',
        'sum',
        'period',
        'restrictions',
        'banks',
        'start',
        'limit',
        'order',
        'advanced-repayment',
        'without-penalty',
        'without-moratorium',
        'without-guarantee',
        'without-additional-fee',
        'without-life-insurance',
        'no-citizenship',
        'proof-of-income',
        'proof-docs',
        'payment-scheme',
        'decision-period',
        'min-initial-instalment',
        'instalment-in-percents',
    )
    _acceptable_search = (
        'key',
        'dwelling',
        'dwelling-readiness',
        'without-mortgage-insurance',
        'without-title-insurance',
        'all-purpose-dwelling-pledge-credit',
        'refinancing',
    )


def error_factory(code, message, comment):
    """ There are two major kinds of errors: 500 and anything else.

        500 means it's services bad, any other means you are the stupid one.
        So you have a chance to handle those more wisely.
    """
    if code == 500:
        return YandexUslugiInternalServerError(code, message, comment)

    return YandexUslugiError(code, message, comment)


class YandexUslugiError(Exception):
    def __init__(self, code, message, comment):
        self.code = code
        self.message = message
        self.comment = comment

    def __str__(self):
        return '%s: %s (%s).' % (self.code, self.message, self.comment)


class YandexUslugiInternalServerError(YandexUslugiError):
    pass


class AttrDict(dict):
    """ To access dict fields as object attributes.
    """
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self
