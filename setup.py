from distutils.core import setup


setup(
    name='lp_api_wrapper',
    version='0.1',
    description='Unofficial LivePerson API Python Wrapper',
    author='Anthony Jones',
    author_email='ajones@liveperson.com',
    url='https://github.com/ajoneslp/liveperson-api-python-wrapper',
    packages=['lp_api_wrapper'],
    install_requires=['requests', 'requests_oauthlib'],
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'Programming Language :: Python :: 3.5',
    ],
    zip_safe=False
)
