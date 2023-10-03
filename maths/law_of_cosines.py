# url: https://en.wikipedia.org/wiki/Law_of_cosines


import math


def law_of_cosines(a, b, angle_c):
    """
    Calculate the length of the third side of a triangle using the Law of Cosines.

    :param a: Length of side 'a'
    :param b: Length of side 'b'
    :param angle_c: Measure of angle 'C' in degrees
    :return: Length of side 'c'
    """
    # Convert the angle from degrees to radians
    angle_c_radians = math.radians(angle_c)

    # Use the Law of Cosines formula
    c_squared = a**2 + b**2 - 2 * a * b * math.cos(angle_c_radians)

    # Take the square root to find the length of side 'c'
    c = math.sqrt(c_squared)

    return c


if __name__ == "__main__":
    # Input values from the user or other sources
    a = float(input("Enter the length of side 'a': "))
    b = float(input("Enter the length of side 'b': "))
    angle_C_degrees = float(input("Enter the measure of angle 'C' in degrees: "))

    # Calculate the length of side 'c'
    c = law_of_cosines(a, b, angle_C_degrees)
    print(f"The length of side 'c' is {c:.2f}")
