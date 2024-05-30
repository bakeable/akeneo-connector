
# Akeneo Connector and Paginator

This repository contains two Python classes designed to facilitate interacting with Akeneo's REST API: `AkeneoConnector` for making HTTP requests to Akeneo endpoints, and `AkeneoPaginator` for handling paginated responses from Akeneo.

## AkeneoConnector

The `AkeneoConnector` class simplifies authentication and requests to the Akeneo API. It supports GET, PATCH, and POST requests, handling token-based authentication and request headers internally.

### Features

- Supports token-based authentication with Akeneo.
- Simplifies GET, PATCH, and POST requests to Akeneo.
- Automatically handles request headers.


## Usage
To use 'AkeneoConnector', you need to provide your Akeneo credentials and the base URL for your Akeneo API:

```python
from akeneo_connector import AkeneoConnector

# Initialize the connector
connector = AkeneoConnector(username='your_username', password='your_password', auth_token='your_auth_token', auth_url='your_auth_url')

# Use the connector to make API requests
products = connector.get(connector.products_url)
print(products)
```


## AkeneoPaginator
`AkeneoPaginator` handles pagination in responses from the Akeneo API. It's designed to work seamlessly with `AkeneoConnector`, providing an easy way to iterate through pages of API responses.

### Features
Easy iteration over paginated responses.
Supports navigating to next, previous, first, and last pages.
Automatically integrates with `AkeneoConnector` for API requests.

## Usage
Here's how to use `AkeneoPaginator` to iterate through products:

```python
from akeneo_connector import AkeneoConnector
from akeneo_paginator import AkeneoPaginator

# Initialize the paginator
paginator = AkeneoPaginator(AkeneoPaginator.products_url)

# Fetch and print all products
while paginator.next():
    for product in paginator.items:
        print(product)

# Or iterate over all products directly
for product in paginator:
    print(i, product.identifer)
```


## AkeneoProduct
`AkeneoProduct` holds the product data from Akeneo to easily get and/or update a certain product in Akeneo. Along with some methods to make it easy to set values with a certain locale or scope.

### Features
Easy retrieval of product data
Automatically integrates with `AkeneoConnector`
Several methods for retrieving locales, scopes and setting attribute values

#### Usage
Here's an example of how to use `AkeneoProduct`:


```python
from akeneo.akeneo_product import AkeneoProduct

# Assume `product_data` is a dictionary containing product information
product = AkeneoProduct(product_data)

# Or retrieve the product by identifier
product = AkeneoProduct().get('1234')
```

Retrieving Product Attributes
You can retrieve locales, scopes, and values of a product attribute:

```python

# Get locales for an attribute
locales = product.get_locales('description')
print(locales)

# Get scopes for an attribute
scopes = product.get_scopes('price')
print(scopes)

# Get values for an attribute
values = product.get_values('size')
print(values)

```

Setting Product Attributes
To update or set the value of a product attribute for a specific locale and scope:

```python
# Set a new value for an attribute
product.set_value('description', locale='en_US', scope='ecommerce', data='New product description')
```

Fetching a Product
To fetch a product by its identifier:
```python
# Fetch a product
fetched_product = product.get('product_identifier')
if fetched_product:
    print("Product fetched successfully.")
else:
    print("Product not found.")
```

You can get images or other media files associated with a specific attribute from Akeneo products using the get_media method. This method allows you to specify the attribute name, locale, and scope to retrieve the correct media file. To get a media file attribute:
```python
# Get a image attribute for locale en_US and scope ecommerce
product.get_media('thumbnail', locale='en_US', scope='ecommerce')
```
