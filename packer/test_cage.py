import pytest

import packer.product as product
import packer.cage as cage


@pytest.fixture(scope='function')
def empty_cage():
    return cage.Cage(0)


@pytest.fixture(scope='function')
def filled_cage():
    c = cage.Cage(0)
    p0 = product.Product(0, 600, 400, 520)
    p1 = product.Product(1, 600, 100, 400)
    p2 = product.Product(2, 600, 100, 400)
    c.placed_products = [p0, p1, p2]
    return c


def test_cage_initial(empty_cage):
    assert empty_cage.cage_id == 0
    assert empty_cage.total_volume == (cage.Cage.height * cage.Cage.length *
                                       cage.Cage.width)
    assert empty_cage.volume_used == 0
    assert empty_cage.percentage_used == 0.0


def test_cage_volume_used(filled_cage):
    assert filled_cage.volume_used == 172800000
    pct = filled_cage.volume_used/filled_cage.total_volume * 100.0
    assert filled_cage.percentage_used == pct
