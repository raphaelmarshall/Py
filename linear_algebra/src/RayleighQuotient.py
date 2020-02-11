'''
https://en.wikipedia.org/wiki/Rayleigh_quotient
'''
import numpy as np


def isHermitian(matrix) -> bool:
    '''
    Checks if a matrix is Hermitian.

    >>> import numpy as np
    >>> A = np.matrix([
    ... [2,    2+1j, 4],
    ... [2-1j,  3,  1j],
    ... [4,    -1j,  1]])
    >>> isHermitian(A)
    True
    '''
    return np.array_equal(matrix, matrix.H)

def rayleigh_quotient(A, v) -> float:
    '''
    Returns the Rayleigh quotient of a Hermitian matrix A and
    vector v.
    >>> import numpy as np
    >>> A = np.matrix([
    ... [1,  2, 4],
    ... [2,  3,  -1],
    ... [4, -1,  1]
    ... ])
    >>> v = np.matrix([
    ... [1],
    ... [2],
    ... [3]
    ... ])
    >>> rayleigh_quotient(A, v)
    matrix([[3.]])
    '''
    v_star = v.H
    return (v_star*A*v)/(v_star*v)


def tests() -> None:
    A = np.matrix([
    [2,    2+1j, 4],
    [2-1j,  3,  1j],
    [4,    -1j,  1]
    ])

    v = np.matrix([
    [1],
    [2],
    [3]
    ])

    assert isHermitian(A) == True
    print( rayleigh_quotient(A, v))

    A = np.matrix([
    [1,  2, 4],
    [2,  3,  -1],
    [4, -1,  1]
    ])
    assert isHermitian(A) == True
    assert rayleigh_quotient(A, v) == float(3)

if __name__=='__main__':
    import doctest
    doctest.testmod()
    tests()
