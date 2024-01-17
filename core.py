import argparse
from enum import Enum

Matrix2x2 = tuple[int, int, int, int]
prod_mul_ctr: int = 0
pow_mul_ctr: int = 0


class Verbosity(Enum):
    LOW = 0
    MEDIUM = 1
    HIGH = 2


def str_to_verbosity(s: str) -> Verbosity:
    try:
        return Verbosity[s.upper()]
    except KeyError:
        raise ValueError(f"Invalid verbosity level: {s}")


def mat_mul(A: Matrix2x2, B: Matrix2x2) -> Matrix2x2:
    return (
        A[0] * B[0] + A[1] * B[2],
        A[0] * B[1] + A[1] * B[3],
        A[2] * B[0] + A[3] * B[2],
        A[2] * B[1] + A[3] * B[3],
    )


def fibonacci(
    n: int,
    cache: dict[int, int],
    prod_cache: set[int],
    verbosity: Verbosity = Verbosity.LOW,
    test: bool = False,
    v_len: int = 0,
) -> int | None:
    """calculates the nth fibonacci number

    Args:
        n (int): the index of the fibonacci number to calculate

    Returns:
        int: the nth fibonacci number
    """
    if n in cache:
        return cache[n]
    prod: Matrix2x2 | None = None  # (1, 0, 0, 1)
    A: Matrix2x2 = (1, 1, 1, 0)

    min_mult: int = n.bit_count() + n.bit_length() - 2
    read_ind: int = 1
    mults: int
    num: int
    fib_arg: int = n
    for num, curr_ind in zip([n - 1, n + 1], [3, 0]):
        if (mults := num.bit_count() + num.bit_length() - 2) < min_mult:
            min_mult = mults
            n = num
            read_ind = curr_ind
    num = n
    pow_A: int = 1
    prod_pow: int = 0
    if verbosity in (Verbosity.MEDIUM, Verbosity.HIGH):
        global prod_mul_ctr
        global pow_mul_ctr
    while True:
        if n % 2:
            prod_pow += pow_A
            if prod_pow in prod_cache:
                prod = (
                    cache[prod_pow + 1],
                    cache[prod_pow],
                    cache[prod_pow],
                    cache[prod_pow - 1],
                )
            else:
                if not prod:
                    prod = A
                else:
                    prod = mat_mul(prod, A)
                    if verbosity in (Verbosity.MEDIUM, Verbosity.HIGH):
                        prod_mul_ctr += 1
                        if verbosity == Verbosity.HIGH:
                            print(f"prod_mul {prod_pow}")
                            print(f"prod_cache before mul: {prod_cache}")
                cache[prod_pow + 1], cache[prod_pow], cache[prod_pow - 1] = (
                    prod[0],
                    prod[1],
                    prod[3],
                )
                prod_cache.add(prod_pow)
                if test:
                    try:
                        assert prod[0] == prod[1] + prod[3]
                    except AssertionError:
                        print(
                            f"prod test failure: prod_pow is {prod_pow}, triplet is ({prod[0]}, {prod[1]}, {prod[3]})"
                        )
                        return None

        n >>= 1
        if n == 0:
            break
        pow_A <<= 1
        if pow_A in prod_cache:
            A = (cache[pow_A + 1], cache[pow_A], cache[pow_A], cache[pow_A - 1])
        else:
            A = mat_mul(A, A)
            cache[pow_A + 1], cache[pow_A], cache[pow_A - 1] = A[0], A[1], A[3]
            if test:
                try:
                    assert A[0] == A[1] + A[3]
                except AssertionError:
                    print(
                        "pow test failure: pow_A is {pow_A}, triplet is ({A[0]} = {A[1]} + {A[3]})"
                    )
                    return None
            if verbosity in (Verbosity.MEDIUM, Verbosity.HIGH):
                pow_mul_ctr += 1
                if verbosity == Verbosity.HIGH:
                    print(f"pow_mul {pow_A}")
                    print(f"prod_cache before mul: {prod_cache}")
            prod_cache.add(pow_A)
    if not prod:
        raise ValueError("prod is None")
    if verbosity in (Verbosity.MEDIUM, Verbosity.HIGH):
        print(f"({bin(num)[2:].zfill(v_len)})_2, f({fib_arg}) = {prod[read_ind]}")
    return prod[read_ind]


def main(
    max_fib: int = 8,
    min_fib: int = 1,
    verbosity: Verbosity = Verbosity.LOW,
    test: bool = False,
) -> None:
    global prod_mul_ctr
    global pow_mul_ctr
    prod_mul_ctr = 0
    pow_mul_ctr = 0
    l_bits: int = len(bin(max_fib - 1)[2:])
    cache: dict[int, int] = {0: 0, 1: 1, 2: 1}
    prod_cache: set[int] = set([1])
    fibo_seq: list[int] = []
    curr_fib: int | None
    for i in range(min_fib, max_fib + 1):
        curr_fib = fibonacci(
            n=i,
            cache=cache,
            prod_cache=prod_cache,
            verbosity=verbosity,
            test=test,
            v_len=l_bits,
        )
        if not curr_fib:
            return None
        print(f"f({i}) = {curr_fib}")
        if test:
            fibo_seq.append(curr_fib)
    if args.verbosity in (Verbosity.MEDIUM, Verbosity.HIGH):
        print(f"matmul ops for prod: {prod_mul_ctr}")
        print(f"matmul ops for pow: {pow_mul_ctr}")
    if not test:
        return None
    if max_fib - min_fib < 2:
        print("Too short for triplet test")
        return None
    two_prev: int = fibo_seq[-1]
    prev: int = fibo_seq[-2]
    for ind, num in enumerate(reversed(fibo_seq[:-2])):
        try:
            assert two_prev == prev + num
        except AssertionError:
            print("test failure at {ind}, triplet is ({two_prev} = {prev} + {num})")
            return None
        two_prev, prev = prev, num
    print("All tests passed")
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser("interveiw question on fibonacci series")
    parser.add_argument(
        "-n",
        "--max_fib",
        type=int,
        default=8,
        help="max index of fibonacci number to calculate",
    )
    parser.add_argument(
        "-m",
        "--min_fib",
        type=int,
        default=-1,
        help="min index of fibonacci number to calculate",
    )
    parser.add_argument(
        "-v",
        "--verbosity",
        type=str_to_verbosity,
        choices=list(Verbosity),
        default=Verbosity.LOW,
        help="verbosity level",
    )
    parser.add_argument("-t", "--test", action="store_true", help="run tests")
    args = parser.parse_args()
    if args.verbosity in (Verbosity.MEDIUM, Verbosity.HIGH):
        prod_mul_ctr: int = 0
        pow_mul_ctr: int = 0
    if args.min_fib == -1:
        args.min_fib = args.max_fib
    main(
        max_fib=args.max_fib,
        min_fib=args.min_fib,
        verbosity=args.verbosity,
        test=args.test,
    )
