from setuptools import setup, find_packages


setup(
    name='dorksint',
    version='1.0.6',
    packages=find_packages(),
    py_modules=['dorksint'],
    install_requires=[
        'requests',
        'beautifulsoup4',
        'termcolor'
    ],
    entry_points={
        'console_scripts': [
            'dorksint=dorksint:main',
        ],
    },
)
