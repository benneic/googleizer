from setuptools import setup, find_packages

import googleizer

version = str(googleizer.__version__)

setup(
    name='googleizer',
    version=version,
    author='Benn Eichhorn',
    url='http://github.com/beichhor/googleizer',
    description='google api tool',
    download_url='http://github.com/beichhor/googleizer/tarball/master',
    packages=find_packages(),
    install_requires=[
        'httplib2',
        'poster'
    ],
    keywords='google api maps places',
    include_package_data=True,
    zip_safe=True,
)
