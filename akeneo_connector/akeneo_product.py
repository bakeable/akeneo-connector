from typing import TypedDict, Optional

from akeneo_connector.akeneo_connector import AkeneoConnector
from akeneo_connector.akeneo_units import format_value
from akeneo_connector.decorators import validate_parameters

class Value(TypedDict):
     locale: Optional[str]
     scope: Optional[str]
     data: str

class AkeneoProduct:
    """
    A class to represent an Akeneo product.

    Attributes:
        uuid (str): The UUID of the product.
        identifier (str): The identifier of the product.
        enabled (bool): The enabled status of the product.
        family (str): The family of the product.
        categories (list): The categories of the product.
        groups (list): The groups of the product.
        parent (str): The parent of the product.
        values (dict): The values of the product.
        updated_values (dict): The updated values of the product.
        created (str): The created date of the product.
        updated (str): The updated date of the product.
        associations (dict): The associations of the product.
        quantified_associations (dict): The quantified associations of the product.
        metadata (dict): The metadata of the product.
        connector (AkeneoConnector): The Akeneo connector to use.

    """

    def __init__(self, data: dict = {}, connector: AkeneoConnector | None = None):
        # Initialize the AkeneoProduct classs
        self.set(data)

        if connector is None:
            self.connector = AkeneoConnector()
        else:
            self.connector = connector

    def set(self, data: dict):
        """
        Sets the data of the product.

        Args:
            data (dict): The data of the product.
        """
        self.uuid = data.get('uuid')
        self.identifier = data.get('identifier')
        self.enabled = data.get('enabled')
        self.family = data.get('family')
        self.categories = data.get('categories')
        self.groups = data.get('groups')
        self.parent = data.get('parent')
        self.values = data.get('values')
        self.updated_values = {}
        self.created = data.get('created')
        self.updated = data.get('updated')
        self.associations = data.get('associations')
        self.quantified_associations = data.get('quantified_associations')
        self.metadata = data.get('metadata')
    
    def payload(self):
        """Returns a dictionary representation of the product.

        Returns:
            dict: A dictionary representation of the product.
        """
        return {
            'uuid': self.uuid,
            'identifier': self.identifier,
            'values': self.updated_values,
        }
    
    def get_scopes(self, attribute: str | None = None) -> list[str]:
        """
        Gets the scopes for the given attribute.

        Args:
            attribute (str): The attribute to get the scopes for.

        Returns:
            list: The scopes of the attribute.
        """
        scopes = []

        if attribute is not None:
            for value in self.values.get(attribute, []):
                scope = value.get('scope')
                if scope not in scopes:
                    scopes.append(scope)

        if attribute is None:
            for attribute in self.values:
                for value in self.values[attribute]:
                    scope = value.get('scope')
                    if scope not in scopes:
                        scopes.append(scope)

        return scopes
    
    def get_locales(self, attribute: str | None = None) -> list[str]:
        """
        Gets the locales for the given attribute.

        Args:
            attribute (str): The attribute to get the locales for.

        Returns:
            list: The locales of the attribute.
        """
        locales = []
        if attribute is not None:
            for value in self.values.get(attribute, []):
                locale = value.get('locale')
                if locale not in locales:
                    locales.append(locale)

        if attribute is None:
            for attribute in self.values:
                for value in self.values[attribute]:
                    locale = value.get('locale')
                    if locale not in locales:
                        locales.append(locale)

        return locales
    

    def get_locales_by_scopes(self) -> dict[str, list[str]]:
        """
        Gets the locales for each scope.

        Returns:
            dict: The locales for each scope.
        """
        locales_by_scopes = {}
        for attribute in self.values:
            for value in self.values[attribute]:
                locale = value.get('locale')
                scope = value.get('scope')
                if scope not in locales_by_scopes:
                    locales_by_scopes[scope] = []
                if locale not in locales_by_scopes[scope]:
                    locales_by_scopes[scope].append(locale)
        
        return locales_by_scopes
    
    def get_values(self, attribute: str) -> list[Value]:
        """
        Gets the values for the given attribute.

        Args:
            attribute (str): The attribute to get the values for.

        Returns:
            list: The values of the attribute.
        """
        return self.values.get(attribute, [])
    
    def get_value(self, attribute: str, locale: str | None = None, scope: str | None = None, with_fallback = False) -> any:
        """
        Gets the value for the given attribute.

        Args:
            attribute (str): The attribute to get the value for.
            locale (str): The locale of the value.
            scope (str): The scope of the value.

        Returns:
            str: The value of the attribute. None if not found.
        """
        # Failsafe
        if attribute not in self.values:
            return None

        # Try to find the value with locale and scope
        for value in self.values[attribute]:
            if value.get('locale') == locale and value.get('scope') == scope:
                return value.get('data')
        
        # Fallback on locale first, then on scope
        if with_fallback:
            for value in self.values[attribute]:
                if value.get('locale') is locale:
                    return value.get('data')
            
            for value in self.values[attribute]:
                if value.get('scope') is scope:
                    return value.get('data')

        # Return first value if locale is None and scope is None
        if locale is None and scope is None or with_fallback:
            return self.values[attribute][0].get('data')

        # Return None if locale and scope are not found
        return None
    
    def get_linked_data(self, attribute: str, locale: str | None = None, scope: str | None = None, with_fallback = False) -> dict | None:
        """
        Gets the linked data for the given attribute.

        Args:
            attribute (str): The attribute to get the linked data for.
            locale (str): The locale of the value.
            scope (str): The scope of the value.

        Returns:
            dict: The linked data of the attribute. None if not found.
        """
        # Failsafe
        if attribute not in self.values:
            return None

        # Try to find the value with locale and scope
        for value in self.values[attribute]:
            if value.get('locale') == locale and value.get('scope') == scope:
                return value.get('linked_data', None)

        # Return first value if locale is None and scope is None
        if locale is None and scope is None or with_fallback:
            return self.values[attribute][0].get('linked_data', None)
        
        # Return None if locale and scope are not found
        return None
    
    def get_formatted_value(self, attribute: str, locale: str | None = None, scope: str | None = None) -> str:
        """
        Gets the formatted value for the given attribute.

        Args:
            attribute (str): The attribute to get the value for.
            locale (str): The locale of the value.
            scope (str): The scope of the value.

        Returns:
            str: The value of the attribute. "N/A" if not found. Will always return a value.
        """
        # Get value
        value = self.get_value(attribute, locale, scope, with_fallback=True)

        # Get linked data
        linked_data = self.get_linked_data(attribute, locale, scope, with_fallback=True)

        # Return formatted value
        return format_value(value, locale, linked_data)
            
    def get_href(self, attribute: str, locale: str | None = None, scope: str | None = None) -> str | None:
        """
        Gets the link for a downloadable attribute.

        Args:
            attribute (str): The attribute to get the link for.
            locale (str): The locale of the value.
            scope (str): The scope of the value.

        Returns:
            dict: The link of the attribute. None if not found.
        """
        # Failsafe
        if attribute not in self.values:
            return None

        # Try to find the value with locale and scope
        for value in self.values[attribute]:
            if value.get('locale') == locale and value.get('scope') == scope:
                return value.get('_links', {}).get('download', {}).get('href', None)

        # Return first value if locale is None and scope is None
        if locale is None and scope is None:
            return self.values[attribute][0].get('_links', {}).get('download', {}).get('href', None)
        
        # Return None if locale and scope are not found
        return None

    def set_value(self, attribute: str, locale: str | None = None, scope: str | None = None, data: str | None = None):
        """
        Sets a value for the given attribute.

        Args:
            attribute (str): The attribute to set the value for.
            locale (str): The locale of the value.
            scope (str): The scope of the value.
            data (str): The data of the value.

        Returns:
            None
        """
        # Failsafes
        if data is None:
            return
        
        if attribute not in self.values:
            self.values[attribute] = []

        if attribute not in self.updated_values:
            self.updated_values[attribute] = self.values[attribute]

        # Try to find the index of the value existing with locale and scope
        index = None
        for i, value in enumerate(self.updated_values[attribute]):
            if value.get('locale') == locale and value.get('scope') == scope:
                index = i
                break

        # Update the value if it exists
        if index is not None:
            self.updated_values[attribute][index]['data'] = data
        else:
            self.updated_values[attribute].append({
                'locale': locale,
                'scope': scope,
                'data': data
            })

    def get(self, identifier: str | None = None, with_attribute_options: bool = False):
        """
        Retrieves the product data.

        Args:
            identifier (str): The identifier of the product.

        Returns:
            AkeneoProduct: The product with data. None if not found. 
        """
        # Use the identifier if provided
        if identifier is None:
            identifier = self.identifier

        # Failsafe
        if identifier is None:
            return None
        
        # Build the URL
        url = self.connector.product_url.format(identifier=identifier)

        # Add query parameters
        query = ""
        if with_attribute_options:
            query += "with_attribute_options=true&"

        if query:
            url += f"?{query}"

        # Get the product
        data = self.connector.get(url)

        # Return the product if found
        if data is not None:
            # Set the data
            self.set(data)

            # Return the product
            return self
        
        return None

    def update(self):
        """
        Updates the product.

        Returns:
            bool: JSON response if successful, None otherwise.
        """
        # Build the URL
        url = self.connector.product_url.format(identifier=self.identifier)

        # Update the product
        return self.connector.update(url, self.payload())

    def create(self):
        """
        Creates the product.

        Returns:
            bool: JSON response if successful, None otherwise.
        """
        #  Update is same
        return self.update()
    
    def get_media(self, media_attribute: str, locale: str | None = None, scope: str | None = None):
        """
        Downloads the media file for the specified attribute.

        Args:
            image_attribute (str): The name of the attribute containing the image.
            locale (str): The locale of the value.
            scope (str): The scope of the value.

        Returns:
            bytes: The content of the media file, or None if not found
        """
        media_url = self.get_href(media_attribute, locale, scope)
        if media_url:
            return self.connector.get_media_file(media_url)
        return None
    
    @validate_parameters
    def set_media(
            self, 
            attribute: str,
            file_path: str, 
            locale: str, 
            scope: str
        ):
        """
        Sets a media file for the given attribute.
        
        Args:
            attribute (str): The attribute to set the media file for.
            filename (str): The filename of the media file.
            file_type (str): The type of the media file.
            base64_file (str): The base64 encoded media file.
            locale (str): The locale of the value.
            scope (str): The scope of the value.
            
        Returns:
            bool: JSON response if successful, None otherwise.
        """
        
        return self.connector.upload_media({
            'identifier': self.identifier,
            'attribute': attribute,
            'locale': locale,
            'scope': scope  
        }, file_path=file_path)