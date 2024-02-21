import argparse
from enum import Enum


class Verbosity(Enum):
    LOW = 0
    MEDIUM = 1
    HIGH = 2


def check_positive(value: str) -> int:
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("%s is an invalid positive int value" % value)
    return ivalue


def str_to_verbosity(s: str) -> Verbosity:
    try:
        return Verbosity[s.upper()]
    except KeyError:
        raise ValueError(f"Invalid verbosity level: {s}")


Matrix2x2 = tuple[int, int, int, int]


def mat_mul(mat_A: Matrix2x2, mat_B: Matrix2x2) -> Matrix2x2:
    return (
        mat_A[0] * mat_B[0] + mat_A[1] * mat_B[2],
        mat_A[0] * mat_B[1] + mat_A[1] * mat_B[3],
        mat_A[2] * mat_B[0] + mat_A[3] * mat_B[2],
        mat_A[2] * mat_B[1] + mat_A[3] * mat_B[3],
    )
