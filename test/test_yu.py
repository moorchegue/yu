from unittest import TestCase

import yu


class YandexUslugiTestCase(object):
    def test_url(self):
        version = '13.0'
        u = self.resource('a', 'b', version)
        self.assertEqual(u.url, '%s/%s/%s' % (yu.API_SITE, version, u.resource))


class YandexUslugiBaseTestCase(YandexUslugiTestCase, TestCase):
    resource = yu.YandexUslugiBase


class BankTestCase(YandexUslugiTestCase, TestCase):
    resource = yu.Bank


class BankDepositTestCase(YandexUslugiTestCase, TestCase):
    resource = yu.BankDeposit


class BankCreditTestCase(YandexUslugiTestCase, TestCase):
    resource = yu.BankCredit


class BankAutoCreditTestCase(YandexUslugiTestCase, TestCase):
    resource = yu.BankAutoCredit


class BankMortgageTestCase(YandexUslugiTestCase, TestCase):
    resource = yu.BankMortgage


class YandexUslugiValidationTestCase(object):
    def test_validate(self):
        u = self.resource('a', 'b')
        u._validate(self.required, self.acceptable, self.actual)


class YandexUslugiErrorFactoryTestCase(object):
    def test_error_factory(self):
        error = yu.error_factory(404, None)
        self.assertFalse(isinstance(error, yu.YandexUslugiError))
        self.assertFalse(isinstance(error, yu.YandexUslugiInternalServerError))

    def test_error_factory_500(self):
        error = yu.error_factory(500, None)
        self.assertTrue(isinstance(error, yu.YandexUslugiInternalServerError))
