"""
Approximates the area under the curve using many different 
methods of numerical integration. For more information on 
numerical integration see here:

https://en.wikipedia.org/wiki/Numerical_integration

The methods used are described in order from most 
accurate to least accurate:
1. Right endpoint rule
2. Left endpoint rule
3. Midpoint rule
4. Trapezoidal rule
5. Simpson's rule

"""
from __future__ import annotations

from typing import Callable

def right_endpt_rule(
    fnc: Callable[[int | float], int | float],
    x_start: int | float,
    x_end: int | float,
    steps: int = 100,
) -> float:
    
    """
    Construct a rectangle on each subinterval, the height of 
    the rectangle is determined by the function value at the 
    right endpoint of the subinterval. The rectangle width 
    is the length of the function (x_end-x_start)/steps. By 
    summing the area of each of these rectangles, we are 
    approximating the area underneath the curve
    """
    area = 0.0
    dx = (x_end - x_start) / steps

    # For the RIGHT endpoint rule, we start at the 
    # right-hand side of each reactangle 
    # so our starting point must be x_start+dx
    i = x_start + dx

    # Looping through each subinterval 
    # till the end of the interval
    while i < x_end:
        # Calculate the height of rectangle
        height = fnc(i)
        # Calculate the area of rectangle and 
        # add it to our total area
        area += (height*dx)

        # Increment to the next subinterval
        i += dx

    return area

def left_endpt_rule(
    fnc: Callable[[int | float], int | float],
    x_start: int | float,
    x_end: int | float,
    steps: int = 100,
) -> float:

    """
    Construct a rectangle on each subinterval, the height of 
    the rectangle is determined by the function value at the 
    left endpoint of the subinterval. The rectangle width 
    is the length of the function (x_end-x_start)/steps. By 
    summing the area of each of these rectangles, we are 
    approximating the area underneath the curve
    """
    area = 0.0
    dx = (x_end - x_start) / steps

    # For the LEFT endpoint rule, we start at the 
    # left-hand side of each reactangle 
    # so our starting point must be x_start
    i = x_start

    # Looping through each subinterval 
    # till the end of the interval
    while i <= x_end-dx:
        # Calculate the height of rectangle
        height = fnc(i)
        # Calculate the area of rectangle and 
        # add it to our total area
        area += (height*dx)

        # Increment to the next subinterval
        i += dx

    return area

def midpoint_rule(
    fnc: Callable[[int | float], int | float],
    x_start: int | float,
    x_end: int | float,
    steps: int = 100,
) -> float:

    """
    Construct a rectangle on each subinterval, the height of 
    the rectangle is determined by the function value at the 
    midpoint of the subinterval. The rectangle width 
    is the length of the function (x_end-x_start)/steps. By 
    summing the area of each of these rectangles, we are 
    approximating the area underneath the curve
    """
    area = 0.0
    dx = (x_end - x_start) / steps

    # For the midpoint rule, we start at the 
    # middle of each sub-interval 
    # so our starting point must be (x_start + (x_start+dx))/2
    # i.e. the average of the left point and the right point
    i = (x_start + (x_start+dx))/2

    # Looping through each subinterval 
    # till the end of the interval
    while i <= x_end:
        # Calculate the height of rectangle
        height = fnc(i)
        # Calculate the area of rectangle and 
        # add it to our total area
        area += (height*dx)

        # Increment to the next subinterval
        i += dx

    return area

def trapezoidal_area(
    fnc: Callable[[int | float], int | float],
    x_start: int | float,
    x_end: int | float,
    steps: int = 100,
) -> float:

    """
    Treats curve as a collection of linear lines and sums the area of the
    trapezium shape they form
    :param fnc: a function which defines a curve
    :param x_start: left end point to indicate the start of line segment
    :param x_end: right end point to indicate end of line segment
    :param steps: an accuracy gauge; more steps increases the accuracy
    :return: a float representing the length of the curve

    >>> def f(x):
    ...    return 5
    >>> '%.3f' % trapezoidal_area(f, 12.0, 14.0, 1000)
    '10.000'

    >>> def f(x):
    ...    return 9*x**2
    >>> '%.4f' % trapezoidal_area(f, -4.0, 0, 10000)
    '192.0000'

    >>> '%.4f' % trapezoidal_area(f, -4.0, 4.0, 10000)
    '384.0000'
    """
    x1 = x_start
    fx1 = fnc(x_start)
    area = 0.0

    for i in range(steps):

        # Approximates small segments of curve as linear and solve
        # for trapezoidal area
        x2 = (x_end - x_start) / steps + x1
        fx2 = fnc(x2)
        area += abs(fx2 + fx1) * (x2 - x1) / 2

        # Increment step
        x1 = x2
        fx1 = fx2
    return area

def simpsons_rule(
    fnc: Callable[[int | float], int | float],
    x_start: int | float,
    x_end: int | float,
    steps: int = 100,
) -> float:

    pass

if __name__ == "__main__":

    def f(x):
        return x ** 3

    print("f(x) = x^3")
    print("The area between the curve, x = 0, x = 5 and the x axis is:")
    i = 10
    while i <= 100000:
        r_area = right_endpt_rule(f, 0, 5, i)
        l_area = left_endpt_rule (f, 0, 5, i)
        m_area = midpoint_rule   (f, 0, 5, i)
        t_area = trapezoidal_area(f, 0, 5, i)
        print(f"Right endpoint rule ({i} steps): \t {r_area}")
        print(f"Left endpoint rule ({i} steps):  \t {l_area}")
        print(f"Midpoint rule ({i} steps):       \t {m_area}")
        print(f"Trapezoidal rule ({i} steps):    \t {t_area}\n")
        i *= 10