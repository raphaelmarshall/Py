class CircularQueueLinkedList:
    def __init__(self):
        self.elem = None

    def is_empty(self) -> bool:
        """
        >>> cq = CircularQueueLinkedList()
        >>> cq.is_empty()
        True
        >>> cq.enqueue('a')
        >>> cq.is_empty()
        False
        >>> cq.dequeue()
        'a'
        >>> cq.is_empty()
        True
        """
        return self.elem is None

    def first(self):
        """
        >>> cq = CircularQueueLinkedList()
        >>> cq.first()
        Traceback (most recent call last):
           ...
        Exception: Empty Queue
        >>> cq.enqueue('a')
        >>> cq.first()
        'a'
        >>> cq.dequeue()
        'a'
        >>> cq.first()
        Traceback (most recent call last):
           ...
        Exception: Empty Queue
        """
        self.check_can_perform_operation()
        return self.elem

    def enqueue(self, data):
        self.elem = data

    def dequeue(self):
        """
        >>> cq = CircularQueueLinkedList()
        >>> cq.dequeue()
        Traceback (most recent call last):
           ...
        Exception: Empty Queue
        >>> cq.enqueue('a')
        >>> cq.dequeue()
        'a'
        >>> cq.dequeue()
        Traceback (most recent call last):
           ...
        Exception: Empty Queue
        """
        self.check_can_perform_operation()
        elem = self.elem
        self.elem = None
        return elem

    def check_can_perform_operation(self):
        if self.elem is None:
            raise Exception("Empty Queue")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
