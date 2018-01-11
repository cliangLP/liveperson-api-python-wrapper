from setuptools import setup, find_packages


setup(
    name='lp_api_wrapper',
    version='0.3',
    description='Unofficial LivePerson API Python Wrapper',
    author='Anthony Jones',
    author_email='ajones@liveperson.com',
    url='https://github.com/ajoneslp/liveperson-api-python-wrapper',
    download_url='https://github.com/ajoneslp/liveperson-api-python-wrapper/archive/0.3.tar.gz',
    packages=find_packages(exclude=['examples']),
    install_requires=['requests', 'requests_oauthlib'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
)
