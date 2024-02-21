import argparse

from FiboService.core import Verbosity
from FiboService.utils import check_positive, mat_mul, str_to_verbosity


def test_check_positive() -> None:
    # Test case 1: Positive integer
    assert check_positive(value="10") == 10

    # Test case 2: Zero should raise an error
    try:
        check_positive(value="0")
        assert False  # This line should not be reached
    except argparse.ArgumentTypeError:
        assert True

    # Test case 3: Negative integer should raise an error
    try:
        check_positive(value="-5")
        assert False  # This line should not be reached
    except argparse.ArgumentTypeError:
        assert True


def test_str_to_verbosity() -> None:
    # Test case 1: Valid verbosity level
    assert str_to_verbosity(s="low") == Verbosity.LOW

    # Test case 2: Invalid verbosity level should raise an error
    try:
        str_to_verbosity(s="invalid")
        assert False  # This line should not be reached
    except ValueError:
        assert True


def test_mat_mul() -> None:
    # Test case 1: Identity matrix multiplication
    assert mat_mul(mat_A=(1, 0, 0, 1), mat_B=(2, 0, 0, 2)) == (2, 0, 0, 2)

    # Test case 2: Non-identity matrix multiplication
    assert mat_mul(mat_A=(1, 2, 3, 4), mat_B=(5, 6, 7, 8)) == (19, 22, 43, 50)
