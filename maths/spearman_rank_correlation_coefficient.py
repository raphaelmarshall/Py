def assign_ranks(data: list[float]) -> list[int]:
    """
    Assigns ranks to elements in the array.

    :param data: List of floats.
    :return: List of ints representing the ranks.

    Example:
    >>> assign_ranks([3.2, 1.5, 4.0, 2.7, 5.1])
    [3, 1, 4, 2, 5]

    >>> assign_ranks([10.5, 8.1, 12.4, 9.3, 11.0])
    [3, 1, 5, 2, 4]
    """
    ranked_data = sorted((value, index) for index, value in enumerate(data))
    ranks = [0] * len(data)

    for position, (_, index) in enumerate(ranked_data):
        ranks[index] = position + 1

    return ranks


def calculate_spearman_rank_correlation(variable_1: list[float], variable_2: list[float]) -> float:
    """
    Calculates Spearman's rank correlation coefficient.

    :param variable_1: List of floats representing the first variable.
    :param variable_2: List of floats representing the second variable.
    :return: Spearman's rank correlation coefficient.

    Example Usage:

    >>> x = [1, 2, 3, 4, 5]
    >>> y = [5, 4, 3, 2, 1]
    >>> calculate_spearman_rank_correlation(x, y)
    -1.0

    >>> x = [1, 2, 3, 4, 5]
    >>> y = [2, 4, 6, 8, 10]
    >>> calculate_spearman_rank_correlation(x, y)
    1.0

    >>> x = [1, 2, 3, 4, 5]
    >>> y = [5, 1, 2, 9, 5]
    >>> calculate_spearman_rank_correlation(x, y)
    0.6
    """
    n = len(variable_1)
    rank_var1 = assign_ranks(variable_1)
    rank_var2 = assign_ranks(variable_2)

    # Calculate differences of ranks
    d = [rx - ry for rx, ry in zip(rank_var1, rank_var2)]

    # Calculate the sum of squared differences
    d_squared = sum(di ** 2 for di in d)

    # Calculate the Spearman's rank correlation coefficient
    rho = 1 - (6 * d_squared) / (n * (n**2 - 1))

    return rho


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    # Example usage:
    x1 = [1, 2, 3, 4, 5]
    y1 = [2, 4, 6, 8, 10]
    rho1 = calculate_spearman_rank_correlation(x1, y1)
    print(f"Spearman's rank correlation coefficient (Example 1): {rho1}")

    x2 = [1, 2, 3, 4, 5]
    y2 = [5, 4, 3, 2, 1]
    rho2 = calculate_spearman_rank_correlation(x2, y2)
    print(f"Spearman's rank correlation coefficient (Example 2): {rho2}")

    x3 = [1, 2, 3, 4, 5]
    y3 = [5, 1, 2, 9, 5]
    rho3 = calculate_spearman_rank_correlation(x3, y3)
    print(f"Spearman's rank correlation coefficient (Example 3): {rho3}")
