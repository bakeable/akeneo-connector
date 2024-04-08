import sys
sys.path.append('..')

from akeneo import AkeneoProduct, AkeneoConnector

# Create an instance of the AkeneoConnector class
connector = AkeneoConnector()

# Create an instance of the AkeneoProduct class
product = AkeneoProduct(data={}, connector=connector)

# Retrieve the product
product.get('0031')

# Set the product name
product.set_value(attribute='name', locale='en_US', data='Test Name')

# Print the product payload
print(product.payload())

# Save the product
product.update()