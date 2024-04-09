from akeneo_connector.akeneo_connector import AkeneoConnector
from akeneo_connector.akeneo_product import AkeneoProduct



class AkeneoPaginator:
    """
    The AkeneoPaginator class is used to paginate through the Akeneo API.

    Attributes:
        response (dict): The response from the Akeneo API.
        items (list): The items in the response.
        links (dict): The links for the response.
        current_page (int): The current page of the response.
        page_size (int): The page size of the response.
        connector (AkeneoConnector): The Akeneo connector to use.
    """
    def __init__(self, url: str | None = None, page_size: int = 10, version='v1'):
        """
        Initializes an instance of the AkeneoPaginator class.

        Args:
            response (dict): The response from the Akeneo API.
        """
        # Initialize the AkeneoPaginator class
        self.connector = AkeneoConnector(version=version)

        if url is None:
            url = self.connector.products_url

        # Initialize the AkeneoPaginator class
        self.response = None
        self.items: list[AkeneoProduct] | list[dict] = []
        self.initial_url = url
        self.links = {
            'self': url + f'?limit={page_size}',
            'first': None,
            'previous': None,
            'next': None,
            'last': None
        }
        self.page_size = page_size
        self.current_page = 1
        self.page_size = page_size
        
        if url not in [
            self.connector.products_url,
        ]:
            raise ValueError(f'Invalid URL: {url}.')

    def set(self, response):
        """
        Sets the response of the paginator.

        Args:
            response (dict): The response from the Akeneo API.
        """
        # Set the response
        self.response = response

        # Get the items for the response
        self.items = []
        for item in response.get('_embedded').get('items'):
            if 'identifier' in item:
                self.items.append(AkeneoProduct(item, connector=self.connector))
            else:
                self.items.append(item)
        
        # Get the links from the response
        links = response.get('_links')
        self.links = {
            'self': links.get('self').get('href') if 'self' in links else None,
            'first': links.get('first').get('href') if 'first' in links else None,
            'previous': links.get('previous').get('href') if 'previous' in links else None,
            'next': links.get('next').get('href') if 'next' in links else None,
            'last': links.get('last').get('href') if 'last' in links else None
        }

        # Get the current page
        self.current_page = int(response.get('current_page'))

    def init(self):
        """
        Gets the initial page of items

        Returns:
            None
        """
        # Get the next page of items
        response = self.connector.get(self.initial_url)

        # Set the response for the paginator
        self.set(response)

    def next(self):
        """
        Gets the next page of items.

        Returns:
            bool: True if there is a next page, False otherwise.
        """
        # Get the URL for the next page
        if len(self.items) == 0:
            url = self.links["self"]
        else:
            url = self.links["next"]

        # Check if there is a next page
        if url is None:
            return False
        
        # Get the next page of items
        response = self.connector.get(url)

        # Set the response for the paginator
        self.set(response)

        # Return True if there is a next page
        return True

    def __iter__(self):
        """
        Returns an iterator for the items in the response.

        Returns:
            iterator: An iterator for the items in the response.
        """
        if len(self.items) == 0:
            self.init()

        index = 0
        while index < len(self.items):
            yield self.items[index]
            index += 1
            if index == len(self.items) and self.next():
                index = 0
    
    def __len__(self):
        """
        Returns the number of items in the response.

        Returns:
            int: The number of items in the response.
        """
        # Return the number of items
        return len(self.items)