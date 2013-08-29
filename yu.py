import requests
import xmltodict


API_SITE = "http://api.uslugi.yandex.ru"
API_VERSION = "1.0"


class YandexUslugiBase(object):
    """ Yandex Uslugi base class.
    """

    headers = {}
    resource = ''
    url = ''

    _required_get = ('region', )
    _acceptable_get = ('key', )

    def __init__(self, key, referer, version=API_VERSION):
        self.headers = {
            'Authorization': key,
            'Referer': referer,
        }
        self.url = '%s/%s/%s' % (API_SITE, version, self.resource)

    def get(self, id_, *args, **kwargs):
        self._validate(self._required_get, self._acceptable_get, kwargs)
        url = '%s/%s' % (self.url, id_)
        return self._get_response(url, kwargs)

    def _get_response(self, url, params):
        response = requests.get(url, params=params, headers=self.headers)
        data = xmltodict.parse(response.content)

        if response.status_code is not 200:
            raise error_factory(response.status_code, data['error'])

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

    def find(self, *args, **kwargs):
        self._validate(self._required_search, self._acceptable_search, kwargs)
        url = '%s/%s' % (self.url, 'search')
        return self._get_response(url, kwargs)


class YandexUslugiListable(object):
    _required_all = ('region', )
    _acceptable_all = ('key', )

    def all(self, *args, **kwargs):
        self._validate(self._required_all, self._acceptable_all, kwargs)
        return self._get_response(self.url, kwargs)


class Bank(YandexUslugiBase, YandexUslugiListable):
    resource = 'banks'


class BankDeposit(YandexUslugiBase, YandexUslugiSearcheable):
    resource = 'banks/deposits'
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


def error_factory(code, error):
    """ There are two major kinds of errors: 500 and anything else.

        500 means it's services bad, any other means you are the stupid one.
        So you have a chance to handle those more wisely.
    """
    if code == 500:
        return YandexUslugiInternalServerError(error)

    return YandexUslugiError(error)


class YandexUslugiError(Exception):
    def __init__(self, error):
        self.error = error

    def __str__(self):
        return '%s: %s' % (self.error['@code'], self.error['@message'])


class YandexUslugiInternalServerError(YandexUslugiError):
    pass
