"""Packer.

Packer application that solves a cage filling problem.  In essence this
program performs a 'first fit decreasing' packing algorithm.  It loads a CSV
file containing product information (dimensions and quantities) to be packed
into standard sized cages.  It sorts the items by volume then sequentially
places them in a cage at position (x,y,z).

On completion the program outputs the number of cages required to
accommodate the products given, the volume utilisation percentage of each
cage and the product not packed, if any.
"""


import argparse
import csv
import operator
import sys
import time

from packer import product
from packer import cage


class ProcessingError(Exception):
    pass


def log_error(message):
    now = time.strftime('%Y-%m-%d %H:%M:%S')
    print('{} ERROR: {}'.format(now, message))


def log_info(message):
    now = time.strftime('%Y-%m-%d %H:%M:%S')
    print('{} INFO: {}'.format(now, message))


def parse_args(argv=None):
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(prog='packer')
    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version='%(prog)s 0.1',
    )
    parser.add_argument(
        '--file',
        help='Path of the products CSV file',
        default='cage_products.csv',
        dest='products',
    )
    parser.add_argument(
        '--verbose',
        help='Verbose output of cage packing results',
        action='store_true',
        dest='verbose',
    )

    return parser.parse_args(argv)


def get_product(row):
    """Extract and validate the acquired csv data.

    Raises ProcessingError if row data is missing or invalid.
    """
    try:
        qty = int(row['Quantity needed'])
        prod_id = int(row['Product ID'])
        length = int(row['Length (mm)'])
        width = int(row['Width (mm)'])
        height = int(row['Height (mm)'])
    except KeyError as e:
        raise ProcessingError('Missing data item ({})'.format(e))
    except ValueError as e:
        raise ProcessingError('Data item invalid type ({})'.format(e))
    return qty, prod_id, length, width, height


def load_products(f):
    """Load and sort product data.

    Load product data CSV and normalise into a list of Product objects
    sorted by their volume.
    """
    data = []
    with open(f) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                qty, prod_id, length, width, height = get_product(row)
            except ProcessingError as e:
                log_error(e)
            else:
                for i in range(qty):
                    prod = product.Product(prod_id=prod_id,
                                           length=length,
                                           width=width,
                                           height=height)
                    data.append(prod)
    return sorted(data, key=operator.attrgetter('volume'), reverse=True)


def pack(products):
    """Pack products into cages.

    This is the main entry point to the packing algorithm.  While there are
    products to pack we create a cage and attempt to pack all the products
    in it.  ``cage.pack`` returns when no more products can fit in it,
    or all the products have been all been packed.  If the former, and there
    are still products to pack, we create the next cage and repeat.
    """
    cages = []
    while len(products):
        current_cage = cage.Cage(len(cages))
        products = current_cage.pack(products)
        cages.append(current_cage)
    return cages


def main(argv=None):
    """Program entry point.

    Parses any arguments, invokes ``load_products`` to load and normalise
    product data then calls ``pack`` to populate cages with product.
    Finally, outputs cage information.
    """
    args = parse_args(argv)
    products = load_products(args.products)
    cages = pack(products)
    log_info('{} cage(s) packed:'.format(len(cages)))
    for c in cages:
        log_info('Cage {}: {:3.3f}% utilised'.format(c.cage_id,
                                                     c.percentage_used))
        if args.verbose:
            log_info('== Cage {} details ===='.format(c.cage_id))
            for item in c.placed_products:
                log_info('Product {} placed at {}'.format(item.prod_id,
                                                          item.location))
                log_info('p.width={} p.height={} p.length={}'.format(
                    item.width, item.height, item.length))
            log_info('======================='.format(c.cage_id))


if __name__ == '__main__':  # pragma: no cover
    sys.exit(main())
