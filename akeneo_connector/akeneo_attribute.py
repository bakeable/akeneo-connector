from akeneo_connector.akeneo_connector import AkeneoConnector
     
class AkeneoAttribute:
    """
    A class to represent an Akeneo attribute.
    
    Attributes:
        code (str): The code of the attribute.
        type (str): The type of the attribute.
        group (str): The group of the attribute.
        labels (dict): The labels of the attribute.
        connector (AkeneoConnector): The Akeneo connector to use.
    """
    
    def __init__(self, code: str | None = None, data: dict = {}, connector: AkeneoConnector | None = None):
        """
        Initializes an instance of the AkeneoAttribute class.
        
        Args:
            data (dict): The data of the attribute.
            connector (AkeneoConnector): The Akeneo connector to use.
        """
        # Initialize the AkeneoAttribute class
        self.set(data)
        
        if connector is None:
            self.connector = AkeneoConnector()
        else:
            self.connector = connector
            
        if code is not None:
            self.get(code)
            
    def get(self, code: str):
        """
        Gets the attribute from Akeneo.
        
        Args:
            code (str): The code of the attribute.
        """
        # Get the attribute
        data = self.connector.get_attribute(code)
        
        self.set(data)
        
    def set(self, data: dict):
        """
        Sets the data of the product.

        Args:
            data (dict): The data of the product.
        """
        self.code = data.get('code')
        self.type = data.get('type')
        self.labels = data.get('labels', {})
            

    def get_label(self, locale: str | None = None):
        """
        Gets the label attribute from Akeneo.

        Args:
            attribute (str): The code of the attribute.
            locale (str): The locale of the value.

        Returns:
            str: The label of the attribute.
        """
        # Get the label
        return self.labels.get(locale, None)