from setuptools import setup, find_packages

v = '0.5.8'

setup(
    name='lp_api_wrapper',
    version=v,
    description='Unofficial LivePerson API Python Wrapper',
    author='Anthony Jones',
    author_email='anthonybjones@me.com',
    url='https://github.com/ajoneslp/liveperson-api-python-wrapper',
    download_url='https://github.com/ajoneslp/liveperson-api-python-wrapper/archive/{}.tar.gz'.format(v),
    packages=find_packages(),
    install_requires=['requests', 'requests_oauthlib'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
)
