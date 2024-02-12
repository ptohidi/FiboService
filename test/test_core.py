from FiboService.core import FibMachine, Verbosity


def test_fibonacci() -> None:
    fib_machine = FibMachine()

    # Test case 1: Fibonacci number at index 0
    assert fib_machine.fibonacci(0) == 0

    # Test case 2: Fibonacci number at index 1
    assert fib_machine.fibonacci(1) == 1

    # Test case 3: Fibonacci number at index 5
    assert fib_machine.fibonacci(5) == 5

    # Test case 4: Fibonacci number at index 10
    assert fib_machine.fibonacci(10) == 55

    # Test case 5: Fibonacci number at index 20 with high verbosity
    assert fib_machine.fibonacci(20, verbosity=Verbosity.HIGH) == 6765


def test_find_read_ind() -> None:
    fib_machine = FibMachine()

    # Test case 1: Index 3 should return exponent 2 and read index 3
    assert fib_machine.find_read_ind(3) == (2, 0)

    # Test case 2: Index 4 should return exponent 3 and read index 3
    assert fib_machine.find_read_ind(4) == (3, 0)


def test_reset_counters() -> None:
    fib_machine = FibMachine()
    fib_machine.reset_counters()
    assert fib_machine.prod_mul_ctr == 0
    assert fib_machine.pow_mul_ctr == 0


def test_reset_caches() -> None:
    fib_machine = FibMachine()
    fib_machine.reset_caches()
    assert fib_machine.cache == {0: 0, 1: 1, 2: 1}
    assert fib_machine.prod_cache == {1}
