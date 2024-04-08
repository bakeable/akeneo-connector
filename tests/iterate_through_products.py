import sys
sys.path.append('../akeneo')
sys.path.append('..')

from akeneo import AkeneoPaginator

# Create an instance of the AkeneoPaginator class
paginator = AkeneoPaginator()

# Loop through all products
for product in paginator:
    print(f'{product.identifier}')