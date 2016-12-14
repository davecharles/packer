import pytest

import packer.product as product


@pytest.fixture(scope='function')
def prod():
    return product.Product(1, 10, 10, 10)


def test_id(prod):
    assert prod.prod_id == 1


def test_volume(prod):
    assert prod.volume == 1000


