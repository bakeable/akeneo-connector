from setuptools import setup, find_packages

setup(
    name="akeneo_connector",
    version="0.1.28",
    packages=find_packages(),
    install_requires=[
        'requests >= 2.31.0',
        'python-dotenv >= 1.0.1'
    ],
    author="Robin Bakker",
    author_email="robin@bakeable.nl",
    description="Akeneo Connector is a Python package that simplifies interacting with Akeneo's REST API. It provides classes for making HTTP requests to Akeneo endpoints, handling pagination in responses, and managing product data in Akeneo.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/bakeable/akeneo-connector",
    license="MIT",
    classifiers=[
        # Trove classifiers (https://pypi.org/classifiers/)
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',

)