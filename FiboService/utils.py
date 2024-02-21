import argparse
from enum import Enum
from typing import Any


class Verbosity(Enum):
    LOW = 0
    MEDIUM = 1
    HIGH = 2


def check_positive(value: Any) -> int:
    try:
        ivalue = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("%s is an invalid positive int value" % value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("%s is an invalid positive int value" % value)
    return ivalue


def str_to_verbosity(s: str) -> Verbosity:
    try:
        return Verbosity[s.upper()]
    except KeyError:
        raise ValueError(f"Invalid verbosity level: {s}")


Matrix2x2 = tuple[int, int, int, int]


def mat_mul(A: Matrix2x2, B: Matrix2x2) -> Matrix2x2:
    return (
        A[0] * B[0] + A[1] * B[2],
        A[0] * B[1] + A[1] * B[3],
        A[2] * B[0] + A[3] * B[2],
        A[2] * B[1] + A[3] * B[3],
    )
