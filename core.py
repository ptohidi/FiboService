from utils import Matrix2x2, Verbosity, mat_mul


class FibMachine:
    """calculates fibonacci numbers using matrix multiplication and caches the results"""

    def __init__(self) -> None:
        self.cache: dict[int, int]
        self.prod_cache: set[int]
        self.reset_caches()
        self.prod_mul_ctr: int
        self.pow_mul_ctr: int
        self.reset_counters()
        return None

    def fibonacci(
        self,
        n: int,
        test: bool = False,
        verbosity: Verbosity = Verbosity.LOW,
        l_bits: int = 0,
    ) -> int | None:
        """calculates the nth fibonacci number

        Args:
            n (int): the index of the fibonacci number to calculate

        Returns:
            f(n) (int): the n-th fibonacci number
        """

        if verbosity == Verbosity.HIGH:
            print("*" * 40)
            print(f"f({n}):")

        if n in self.cache:
            if verbosity == Verbosity.HIGH:
                print(f"cache hit: {n}")
            return self.cache[n]
        prod: Matrix2x2 | None = None  # (1, 0, 0, 1)
        A: Matrix2x2 = (1, 1, 1, 0)

        n, read_ind = self.find_read_ind(n)

        if verbosity == Verbosity.HIGH:
            print(f"exponent used: ({bin(n)[2:].zfill(l_bits)})_2")

        pow_A: int = 1
        prod_pow: int = 0
        while True:
            if n % 2:
                prod_pow += pow_A
                if prod_pow in self.prod_cache:
                    prod = (
                        self.cache[prod_pow + 1],
                        self.cache[prod_pow],
                        self.cache[prod_pow],
                        self.cache[prod_pow - 1],
                    )
                else:
                    if not prod:
                        prod = A
                    else:
                        prod = mat_mul(prod, A)
                        if verbosity in (Verbosity.MEDIUM, Verbosity.HIGH):
                            self.prod_mul_ctr += 1
                            if verbosity == Verbosity.HIGH:
                                print(f"prod_mul {prod_pow}")
                                print(f"prod_cache before mul: {self.prod_cache}")
                    (
                        self.cache[prod_pow + 1],
                        self.cache[prod_pow],
                        self.cache[prod_pow - 1],
                    ) = (
                        prod[0],
                        prod[1],
                        prod[3],
                    )
                    self.prod_cache.add(prod_pow)
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
            if pow_A in self.prod_cache:
                A = (
                    self.cache[pow_A + 1],
                    self.cache[pow_A],
                    self.cache[pow_A],
                    self.cache[pow_A - 1],
                )
            else:
                A = mat_mul(A, A)
                self.cache[pow_A + 1], self.cache[pow_A], self.cache[pow_A - 1] = (
                    A[0],
                    A[1],
                    A[3],
                )
                if test:
                    try:
                        assert A[0] == A[1] + A[3]
                    except AssertionError:
                        print(
                            "pow test failure: pow_A is {pow_A}, triplet is ({A[0]} = {A[1]} + {A[3]})"
                        )
                        return None
                if verbosity in (Verbosity.MEDIUM, Verbosity.HIGH):
                    self.pow_mul_ctr += 1
                    if verbosity == Verbosity.HIGH:
                        print(f"pow_mul {pow_A}")
                        print(f"prod_cache before mul: {self.prod_cache}")
                self.prod_cache.add(pow_A)
        if not prod:
            raise ValueError("prod is None")
        return prod[read_ind]

    @staticmethod
    def find_read_ind(n: int) -> tuple[int, int]:
        """finds the index of the fibonacci number to read from the matrix multiplication result

        Args:
            n (int): the index of the fibonacci number to calculate

        Returns:
            n (int): the exponent of the matrix to calculate
            read_ind (int): the index of the result matrix to read the fibonacci number from
        """
        read_ind: int
        n, read_ind = min(
            zip([n - 1, n, n + 1], [0, 1, 3]),
            key=lambda x: x[0].bit_count() + x[0].bit_length() - 2,
        )
        return n, read_ind

    def reset_counters(self) -> None:
        self.prod_mul_ctr = 0
        self.pow_mul_ctr = 0
        return None

    def print_counters(self) -> None:
        """prints the number of matrix multiplications used to calculate the fibonacci numbers."""
        print(f"matmul ops for prod: {self.prod_mul_ctr}")
        print(f"matmul ops for pow: {self.pow_mul_ctr}")
        return None

    def reset_caches(self) -> None:
        """resets the caches used to calculate the fibonacci numbers."""
        self.cache = {0: 0, 1: 1, 2: 1}
        self.prod_cache = set([1])
        return None

    def print_caches(self) -> None:
        """prints the caches used to calculate the fibonacci numbers."""
        print(f"cache: {self.cache}")
        print(f"prod_cache: {self.prod_cache}")
        return None
