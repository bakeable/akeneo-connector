import base64
import json
import os
import requests as req



class AkeneoConnector:
    """
    The AkeneoConnector class is used to connect to the Akeneo API.

    Attributes:
        products_url (str): The URL to get the products from.
        username (str): The username to authenticate with.
        password (str): The password to authenticate with.
        auth_token (str): The authentication token to use.
        auth_url (str): The URL to authenticate with.
        access_token (str): The access token to use.
        headers (dict): The headers to use for the request.
        version (str): The version of the API to use.
    """

    # Constants
    PRODUCT_URL = 'https://{origin}/api/rest/{version}/products/{identifier}'
    PRODUCTS_URL = 'https://{origin}/api/rest/{version}/products'
    ATTRIBUTE_URL = 'https://{origin}/api/rest/{version}/attributes/{code}'

    def __init__(self, origin: str | None = None, username = None, password = None, auth_token = None, auth_url = None, version='v1'):
        """
        Initializes an instance of the AkeneoConnector class.

        Args:
            username (str): The username to authenticate with.
            password (str): The password to authenticate with.
            auth_token (str): The authentication token to use.
            auth_url (str): The URL to authenticate with.
        """
        # Initialize the AkeneoConnector class
        # Initialize the AkeneoConnector class
        auth_token = os.getenv('AKENEO_AUTH_TOKEN') if auth_token is None else auth_token
        if auth_token is None:
            raise ValueError("auth_token is required")
        
        self.origin = os.getenv('AKENEO_ORIGIN') if origin is None else origin
        self.username = os.getenv('AKENEO_USERNAME') if username is None else username
        self.password = os.getenv('AKENEO_PASSWORD') if password is None else password
        self.auth_token = base64.b64encode(auth_token.encode()).decode()
        self.auth_url = os.getenv('AKENEO_AUTH_URL') if auth_url is None else auth_url
        self.access_token = self.get_access_token()
        self.headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-type': 'application/vnd.akeneo.collection+json'
        }
        self.version = version
        self.product_url = self.PRODUCT_URL.format(origin=self.origin, version=self.version, identifier='{identifier}')
        self.products_url = self.PRODUCTS_URL.format(origin=self.origin, version=self.version)

    def get_access_token(self):
        """
        Gets the access token from Akeneo.

        Returns:
            str: The access token.
        """
        # Method to get the authentication token from Akeneo
        body = {
            'grant_type': 'password',
            'username': self.username,
            'password': self.password
        }

        # Create the headers for the request
        headers = {
            'Authorization': 'Basic ' + self.auth_token
        }

        # Send the request to the Akeneo API
        response = req.post(self.auth_url, headers=headers, data=body)

        try:
            # Get the JSON response from the request
            data = response.json()

            # Get the access_token from the response data
            self.access_token = data.get('access_token')  

            # Return the access_token
            return self.access_token  
        except:
            print(f"Error: {response.status_code} - {response.text}")
            raise ValueError("Error getting access token")
        
    def get(self, url: str):
        """
        Retrieves data from a given Akeneo API endpoint URL.

        Returns:
            dict: The JSON response.
        """
        # Method to get the products from Akeneo
        print(f"GET {url}")
        response = req.get(url, headers=self.headers)

        # Check if the request was successful
        if response.status_code < 200 or response.status_code >= 300:
            print(f"Request error: {response.status_code} - {response.text}")
            return None
        
        # Try to parse the response as JSON
        try:
            data = response.json()
        except:
            data = response.text

        return data
    
    def update(self, url: str, payload: list | dict):
        """
        Updates an item in Akeneo.

        Args:
            payload (list | dict): The payload to send in the request.
        """   
        if isinstance(payload, dict):
            payloads = [payload]
        else:
            payloads = payload

        # Convert to JSON-strings
        batch_strings = [json.dumps(p) for p in payloads]

        # Join the JSON-strings into a single string
        data_str = "\n".join(batch_strings)

        # Set the payload to the joined JSON-strings
        print(f"PATCH {url}")
        response = req.patch(url, headers=self.headers, data=data_str)

        # Check if the request was successful
        if response.status_code < 200 or response.status_code >= 300:
            print(f"Request error: {response.status_code} - {response.text}")
            return None
        
        # Try to parse the response as JSON
        try:
            data = response.json()
        except:
            data = response.text

        return data

    def get_media_file(self, media_url):
        """
        Gets the media file from Akeneo.

        Args:
            media_url (str): The URL of the media file.

        Returns:
            response: The response object containing the media file.
        """
        response = req.get(media_url, headers=self.headers)
        if response.status_code == 200:
            return response.content
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
    
    def get_attribute(self, attributecode: str):
        """
        Gets the attribute from Akeneo.

        Args:
            code (str): The code of the attribute.

        Returns:
            dict: The JSON response.
        """
        response = req.get(self.ATTRIBUTE_URL.format(origin=self.origin, version=self.version, code=attributecode), headers=self.headers)
        
        # Check if the request was successful
        if response.status_code < 200 or response.status_code >= 300:
            print(f"Request error: {response.status_code} - {response.text}")
            return None
        
        # Try to parse the response as JSON
        try:
            data = response.json()
        except:
            data = response.text
            
        return data