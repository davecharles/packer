# packer
Packer is a simple Python program that solves a 3-D Cage filling problem.
It was developed for an off-line python coding test.

In essence the program performs a 'first fit decreasing' packing algorithm.
It loads a CSV file containing product information (dimensions and quantities)
to be packed into a standard sized cage.  It sorts the items by volume then
sequentially places them in a cage at position (x,y,z).  On completion the
program outputs the number of cages required to accommodate the products
given, the volume utilisation percentage of each cage and the product not
packed, if any.

# Usage
Clone the repo and navigate to packer/.  There product data is in
``cage_product.csv``.  Execute as follows to show usage:

```
$ python -m packer --help
usage: packer [-h] [-v] [--file PRODUCTS] [--verbose]

optional arguments:
  -h, --help       show this help message and exit
  -v, --version    show program's version number and exit
  --file PRODUCTS  Path of the products CSV file
  --verbose        Verbose output of cage packing results
```

## Examples
```
$ python -m packer 
2016-12-19 10:16:02 INFO: 2 cage(s) packed:
2016-12-19 10:16:02 INFO: Cage 0: 57.289% utilised
2016-12-19 10:16:02 INFO: Cage 1: 35.344% utilised
```

```
$ python -m packer --verbose
2016-12-19 10:16:47 INFO: 2 cage(s) packed:
2016-12-19 10:16:47 INFO: Cage 0: 57.289% utilised
2016-12-19 10:16:47 INFO: == Cage 0 details ====
2016-12-19 10:16:47 INFO: Product 13 placed at (0, 0, 0)
2016-12-19 10:16:47 INFO: p.width=400 p.height=520 p.length=600
...
2016-12-19 10:16:47 INFO: p.width=100 p.height=100 p.length=100
2016-12-19 10:16:47 INFO: =======================
2016-12-19 10:16:47 INFO: Cage 1: 35.344% utilised
2016-12-19 10:16:47 INFO: == Cage 1 details ====
2016-12-19 10:16:47 INFO: Product 21 placed at (0, 0, 0)
2016-12-19 10:16:47 INFO: p.width=400 p.height=400 p.length=600
...
2016-12-19 10:16:47 INFO: p.width=325 p.height=112 p.length=157
2016-12-19 10:16:47 INFO: =======================
```

## Testing
```
py.test packer/
...
packer/test_cage.py ..
packer/test_main.py ............
packer/test_product.py ..
-- coverage: platform linux, python 3.4.3-final-0 --
Name                  Stmts   Miss  Cover
-----------------------------------------
packer/__init__           0      0   100%
packer/__main__          66     14    79%
packer/cage              41     23    44%
packer/conftest           4      0   100%
packer/product            9      0   100%
packer/test_cage         21      0   100%
packer/test_main         71      0   100%
packer/test_product       8      0   100%
-----------------------------------------
TOTAL                   220     37    83%

```
Coverage needs work ;)

## Things to-do
Packing an arbitrary three-dimensional space with arbitrary sized cuboids
is an _NP-HARD_ problem, as such ``packer`` takes a heuristic approach.

The current solution consumes 2 cages to pack products the sum of whose
volumes equates to ~92% of a singles cage's capacity.  Pareto principle
might suggest our work is done, however testing on larger data sets
needs to be done.  Optimisations one could try out are as follows:

- Box rotation: Currently the boxes are placed as presented from the
data file (``(x,y,x) == (0,0,0)``) however given a "no-fit" one could
rotate the box through each of its 6 orientations to get a better fit.
- Multiple passes: Randomly selecting a starting point to see if a better
solution can be achieved.
- Better test coverage

## Additional information
- Requires Python 3.4
- Tested using pytest 2.8.2 (with unittest.mock 1.0)
- Pep8 using Pylint 1.5.4
