"""Product module."""


class Product:
    """Class that encapsulates a product to be packed into a cage.
    """
    def __init__(self, prod_id, length, width, height):
        self.prod_id = prod_id
        self.length = length
        self.width = width
        self.height = height
        self.location = None

    @property
    def volume(self):
        """Volume of the product."""
        return self.length * self.width * self.height
