"""Cage module."""


class Cage:
    """Class that encapsulates a cage for products to be packed into."""
    width = 697  # x axis
    height = 1603  # y axis
    length = 846  # z axis

    def __init__(self, cage_id):
        self.cage_id = cage_id
        self.placed_products = []
        self.x = 0
        self.y = 0
        self.z = 0

    def fill(self, products):
        """Fill cage with products to maximum width.

        Fill cage for the current y and z until placed products exceed the x
        bounds.  Returns all unplaced products.
        """
        unplaced = []
        self.x = 0
        for p in products:
            if self.x + p.width < Cage.width:
                p.location = self.x, self.y, self.z
                self.placed_products.append(p)
                self.x += p.width
            else:
                unplaced.append(p)
        return unplaced

    def pack(self, products):
        """Pack cage layers.

        Calls ``fill`` for the current y and z.  For any unplaced products
        we increment z and repeat until the cage layer space is exhausted.
        Increment the layer height until the cage capacity it utilised.
        Returns unplaced products for allocation to the next cage.
        """
        unplaced = products
        while True:
            unplaced = self.fill(unplaced)
            if len(unplaced):  # Work to do?
                # Is there still room in the cage layer?
                new_z = self.z + max(p.length for p in unplaced)
                new_y = self.y + max(p.height for p in unplaced)
                if new_z < self.length:
                    self.z = new_z
                else:
                    self.z = 0
                if new_y < self.height:
                    # Layer full, move to next layer
                    self.y = new_y
                else:
                    break
            else:
                break
        return unplaced

    @property
    def total_volume(self):
        """Total volume of the cage."""
        return self.length * self.width * self.height

    @property
    def volume_used(self):
        """Volume filled by products."""
        return sum(product.volume
                   for product in self.placed_products)

    @property
    def percentage_used(self):
        """Percentage of the cage volume used."""
        return self.volume_used/self.total_volume * 100.0
