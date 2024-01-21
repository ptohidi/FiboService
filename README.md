## Introduction

This is a Python package that I have made for practicing purposes. It calculates Fibonacci numbers using 2x2 matrix multiplication and caches the results for faster calculation.

## Theory

The Fibonacci numbers are defined by the following recurrence relation:

$F_n = F_{n-1} + F_{n-2},$

with seed values $F_0 = 0$ and $F_1 = 1$. 

```math \begin{bmatrix}X\\Y\end{bmatrix}```

It can be shown by mathematical induction that if we define the matrix $A$ as follows:
```math A = \begin{bmatrix}1 & 1 \\ 1 & 0\end{bmatrix}``` , then ```math A^n = \begin{bmatrix}F_{n+1} & F_n \\ F_n & F_{n-1}\end{bmatrix}. ```
In this package, we make use of this property to calculate the Fibonacci numbers:
```math \begin{bmatrix}F_{n+1} & F_n \\ F_n & F_{n-1}\end{bmatrix} = \begin{bmatrix}1 & 1 \\ 1 & 0\end{bmatrix}^n.```

We can calculate $A^n$ using the binary representation of $n$ and the following recursive formula:

```math A^n = \begin{cases} A^{\frac{n}{2}} \times A^{\frac{n}{2}} & \text{if } n \text{ is even} \\ A^{n-1} \times A & \text{if } n \text{ is odd} \end{cases}.```

Using this approach, we can calculate $A^n$ in $O(\log n)$ time.

## License

See the [LICENSE](LICENSE.md) file for license rights and limitations (MIT).