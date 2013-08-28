import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

install_requires = [
    'requests==1.2.3',
    'xmltodict==0.7.0',
]

setup(
    name='yu',
    version='0.0.1',
    description='Yandex Uslugi API Python client implementation',
    long_description=README,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    author='murchik',
    author_email='mixturchik@gmail.com',
    url='https://github.com/moorchegue/yu',
    keywords='yandex uslugi',
    packages=find_packages(),
    py_modules=['yu'],
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    test_suite="yu",
)
