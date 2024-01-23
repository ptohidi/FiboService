import argparse

from FiboService.core import FibMachine
from FiboService.utils import Verbosity, check_positive, str_to_verbosity


def main(
    max_fib: int = 8,
    min_fib: int = 1,
    verbosity: Verbosity = Verbosity.LOW,
    test: bool = False,
) -> None:
    fibo_seq: list[int] = []
    curr_fib: int | None
    l_bits: int = (max_fib + 1).bit_length()
    machine: FibMachine
    if verbosity == Verbosity.LOW:
        machine = FibMachine()
    else:
        machine = FibMachine()
    for i in range(min_fib, max_fib + 1):
        curr_fib = machine.fibonacci(
            n=i,
            test=test,
            verbosity=verbosity,
            l_bits=l_bits,
        )
        if not curr_fib:
            return None
        if verbosity == Verbosity.LOW:
            print(f"f({i}) = {curr_fib}")
        if test:
            fibo_seq.append(curr_fib)
    if args.verbosity in (Verbosity.MEDIUM, Verbosity.HIGH):
        machine.print_counters()
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
            print(f"test failure at {ind}, triplet is ({two_prev} = {prev} + {num})")
            return None
        two_prev, prev = prev, num
    print("All tests passed")
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser("interveiw question on fibonacci series")
    parser.add_argument(
        "-n",
        "--max_fib",
        default=8,
        type=check_positive,
        required=True,
        help="max index of fibonacci number to calculate",
    )
    parser.add_argument(
        "-m",
        "--min_fib",
        type=check_positive,
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
    if args.min_fib == -1:
        args.min_fib = args.max_fib
    main(
        max_fib=args.max_fib,
        min_fib=args.min_fib,
        verbosity=args.verbosity,
        test=args.test,
    )
