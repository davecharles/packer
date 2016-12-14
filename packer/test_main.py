import pytest

import packer.__main__ as main
import packer.cage as cage

@pytest.fixture(scope='function')
def simple_csv_data():
    return """Product ID,Height (mm),Width (mm),Length (mm),Quantity needed
1,100,100,100,1
2,10,10,10,2"""


@pytest.fixture(scope='function')
def products_csv(tmpdir, simple_csv_data):
    tmpfile = tmpdir.join('cage_products.csv')
    with tmpfile.open('w') as f:
        f.write(simple_csv_data)
    return str(tmpfile)


def test_log_info(capsys):
    main.log_info('foo')
    stdout, _ = capsys.readouterr()
    assert 'INFO: foo' in stdout


def test_log_error(capsys):
    main.log_error('foo')
    stdout, _ = capsys.readouterr()
    assert 'ERROR: foo' in stdout


class TestParseArgs:

    def test_version(self, capsys):
        with pytest.raises(SystemExit):
            main.parse_args(['--version'])
        stdout, _ = capsys.readouterr()
        assert 'packer' in stdout

    def test_file_default(self):
        args = main.parse_args([])
        assert args.products == 'cage_products.csv'

    def test_file_override(self):
        args = main.parse_args(['--file=foo.csv'])
        assert args.products == 'foo.csv'

    def test_verbose(self):
        args = main.parse_args(['--verbose'])
        assert args.verbose is True


def test_get_product():
    row = {'Height (mm)': '57', 'Quantity needed': '1', 'Length (mm)': '300',
           'Product ID': '1', 'Width (mm)': '80'}
    assert main.get_product(row) == (1, 1, 300, 80, 57)


def test_get_product_bad_type():
    row = {'Height (mm)': '57', 'Quantity needed': '1', 'Length (mm)': '300',
           'Product ID': '1', 'Width (mm)': '80.123'}
    with pytest.raises(main.ProcessingError) as e:
        main.get_product(row)
    assert 'Data item invalid type' in str(e)


def test_get_product_missing_data():
    row = {'Height (mm)': '57', 'Quantity needed': '1', 'Length (mm)': '300',
           'Product ID': '1'}
    with pytest.raises(main.ProcessingError) as e:
        main.get_product(row)
    assert 'Missing data item (\'Width (mm)\'' in str(e)


def test_load_products(products_csv):
    data = main.load_products(products_csv)
    assert len(data) == 3
    assert data.pop().volume == 1000
    assert data.pop().volume == 1000
    assert data.pop().volume == 1000000


def test_pack_single_pass(monkeypatch):

    def dummy_pack(_, to_pack):
        return []

    monkeypatch.setattr(cage.Cage, 'pack', dummy_pack)
    cages = main.pack([pytest.Mock(), pytest.Mock(), pytest.Mock()])
    assert len(cages) == 1


def test_pack_multiple_pass(monkeypatch):
    p0 = pytest.Mock()
    p1 = pytest.Mock()
    p2 = pytest.Mock()
    p0.packed = False
    p1.packed = False
    p2.packed = False

    def dummy_pack(_, to_pack):
        to_pack.pop()
        return to_pack

    monkeypatch.setattr(cage.Cage, 'pack', dummy_pack)
    cages = main.pack([p0, p1, p2])
    assert len(cages) == 3
