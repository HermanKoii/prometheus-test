from setuptools import setup, find_packages

setup(
    name='coingecko-api-client',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'python-dotenv',
    ],
    extras_require={
        'dev': [
            'pytest',
        ],
    },
)