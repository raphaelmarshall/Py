def next_greatest_element_slow(arr):
    """
    Function to get Next Greatest Element (NGE) pair for all elements of list
    Maximum element present afterwards the current one which is also greater than current one
    >>> next_greatest_element_slow([11, 13, 21, 3])
    [13, 21, -1, -1]
    """
    result = []
    for i in range(0, len(arr), 1):

        next = -1
        for j in range(i + 1, len(arr), 1):
            if arr[i] < arr[j]:
                next = arr[j]
                break
        result.append(next)
        
    return result

def next_greatest_element(arr):
    """
    Function to get Next Greatest Element (NGE) pair for all elements of list
    Maximum element present afterwards the current one which is also greater than current one
    
    Naive way to solve this is to take two loops and check for the next bigger number but that will make the
    time complexity as O(n^2). The better way to solve this would be to use a stack to keep track of maximum
    number givig a linear time complex solution.
    
    >>> next_greatest_element([11, 13, 21, 3])
    [13, 21, -1, -1]
    """
    stack = []              
    result = [-1]*len(arr)

    for index in reversed(range(len(arr))):
        if len(stack):
            while stack[-1] <= arr[index]:
                stack.pop()
                if len(stack) == 0:
                    break

        if len(stack) != 0:
            result[index] = stack[-1]

        stack.append(arr[index])
        
    return result


if __name__ == "__main__":
    from timeit import timeit

    arr = [11, 13, 21, 3]
    print(next_greatest_element_slow(arr))
    print(next_greatest_element(arr))

    setup = ("from __main__ import arr, next_greatest_element_slow, "
             "next_greatest_element")
    print("next_greatest_element_slow():",
          timeit("next_greatest_element_slow(arr)", setup=setup))
    print("     next_greatest_element():",
          timeit("next_greatest_element(arr)", setup=setup))
