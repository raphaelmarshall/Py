"""
Implementation of an auto-balanced binary tree!
For doctests run following command:
python3 -m doctest -v avl_tree.py
For testing run:
python avl_tree.py
"""
import math
import random


class my_queue:
    def __init__(self):
        self.data = []
        self.head = 0
        self.tail = 0

    def isEmpty(self):
        return self.head == self.tail

    def push(self, data):
        self.data.append(data)
        self.tail = self.tail + 1

    def pop(self):
        ret = self.data[self.head]
        self.head = self.head + 1
        return ret

    def count(self):
        return self.tail - self.head

    def print(self):
        print(self.data)
        print("**************")
        print(self.data[self.head : self.tail])


class my_node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
        self.height = 1

    def getdata(self):
        return self.data

    def getleft(self):
        return self.left

    def getright(self):
        return self.right

    def getheight(self):
        return self.height

    def setdata(self, data):
        self.data = data
        return

    def setleft(self, node):
        self.left = node
        return

    def setright(self, node):
        self.right = node
        return

    def setheight(self, height):
        self.height = height
        return


def getheight(node):
    if node is None:
        return 0
    return node.getheight()


def my_max(a, b):
    if a > b:
        return a
    return b


def right_rotation(node):
    r"""
            A                      B
           / \                    / \
          B   C                  Bl  A
         / \       -->          /   / \
        Bl  Br                 UB Br  C
       /
     UB
    UB = unbalanced node
    """
    print("left rotation node:", node.getdata())
    ret = node.getleft()
    node.setleft(ret.getright())
    ret.setright(node)
    h1 = my_max(getheight(node.getright()), getheight(node.getleft())) + 1
    node.setheight(h1)
    h2 = my_max(getheight(ret.getright()), getheight(ret.getleft())) + 1
    ret.setheight(h2)
    return ret


def leftrotation(node):
    """
        a mirror symmetry rotation of the leftrotation
    """
    print("right rotation node:", node.getdata())
    ret = node.getright()
    node.setright(ret.getleft())
    ret.setleft(node)
    h1 = my_max(getheight(node.getright()), getheight(node.getleft())) + 1
    node.setheight(h1)
    h2 = my_max(getheight(ret.getright()), getheight(ret.getleft())) + 1
    ret.setheight(h2)
    return ret


def lrrotation(node):
    r"""
            A              A                    Br
           / \            / \                  /  \
          B   C    LR    Br  C       RR       B    A
         / \       -->  /  \         -->    /     / \
        Bl  Br         B   UB              Bl    UB  C
             \        /
             UB     Bl
    RR = rightrotation   LR = leftrotation
    """
    node.setleft(leftrotation(node.getleft()))
    return rightrotation(node)


def rlrotation(node):
    node.setright(rightrotation(node.getright()))
    return leftrotation(node)


def insert_node(node, data):
    if node is None:
        return my_node(data)
    if data < node.getdata():
        node.setleft(insert_node(node.getleft(), data))
        if (
            getheight(node.getleft()) - getheight(node.getright()) == 2
        ):  # an unbalance detected
            if (
                data < node.getleft().getdata()
            ):  # new node is the left child of the left child
                node = rightrotation(node)
            else:
                node = lrrotation(node)  # new node is the right child of the left child
    else:
        node.setright(insert_node(node.getright(), data))
        if getheight(node.getright()) - getheight(node.getleft()) == 2:
            if data < node.getright().getdata():
                node = rlrotation(node)
            else:
                node = leftrotation(node)
    h1 = my_max(getheight(node.getright()), getheight(node.getleft())) + 1
    node.setheight(h1)
    return node


def getRightMost(root):
    while root.getright() is not None:
        root = root.getright()
    return root.getdata()


def getLeftMost(root):
    while root.getleft() is not None:
        root = root.getleft()
    return root.getdata()


def del_node(root, data):
    if root.getdata() == data:
        if root.getleft() is not None and root.getright() is not None:
            temp_data = getLeftMost(root.getright())
            root.setdata(temp_data)
            root.setright(del_node(root.getright(), temp_data))
        elif root.getleft() is not None:
            root = root.getleft()
        else:
            root = root.getright()
    elif root.getdata() > data:
        if root.getleft() is None:
            print("No such data")
            return root
        else:
            root.setleft(del_node(root.getleft(), data))
    elif root.getdata() < data:
        if root.getright() is None:
            return root
        else:
            root.setright(del_node(root.getright(), data))
    if root is None:
        return root
    if getheight(root.getright()) - getheight(root.getleft()) == 2:
        if getheight(root.getright().getright()) > getheight(root.getright().getleft()):
            root = leftrotation(root)
        else:
            root = rlrotation(root)
    elif getheight(root.getright()) - getheight(root.getleft()) == -2:
        if getheight(root.getleft().getleft()) > getheight(root.getleft().getright()):
            root = rightrotation(root)
        else:
            root = lrrotation(root)
    height = my_max(getheight(root.getright()), getheight(root.getleft())) + 1
    root.setheight(height)
    return root


class AVLtree:
    """
    An AVL tree doctest
    Examples:
    >>> t = AVLtree()
    >>> t.insert(4)
    insert:4
    >>> t.traversale()
     4
    *************************************
    >>> t.insert(2)
    insert:2
    >>> t.traversale()
      4
     2  *
    *************************************
    >>> t.insert(3)
    insert:3
    right rotation node: 2
    left rotation node: 4
    >>> t.traversale()
      3
     2  4
    *************************************
    >>> t.getheight()
    2
    >>> t.del_node(3)
    delete:3
    >>> t.traversale()
      4
     2  *
    *************************************
    """
    def __init__(self):
        self.root = None

    def getheight(self):
        #        print("yyy")
        return getheight(self.root)

    def insert(self, data):
        print("insert:" + str(data))
        self.root = insert_node(self.root, data)

    def del_node(self, data):
        print("delete:" + str(data))
        if self.root is None:
            print("Tree is empty!")
            return
        self.root = del_node(self.root, data)

    def traversale(self):  # a level traversale, gives a more intuitive look on the tree
        q = my_queue()
        q.push(self.root)
        layer = self.getheight()
        if layer == 0:
            return
        cnt = 0
        while not q.isEmpty():
            node = q.pop()
            space = " " * int(math.pow(2, layer - 1))
            print(space, end="")
            if node is None:
                print("*", end="")
                q.push(None)
                q.push(None)
            else:
                print(node.getdata(), end="")
                q.push(node.getleft())
                q.push(node.getright())
            print(space, end="")
            cnt = cnt + 1
            for i in range(100):
                if cnt == math.pow(2, i) - 1:
                    layer = layer - 1
                    if layer == 0:
                        print()
                        print("*************************************")
                        return
                    print()
                    break
        print()
        print("*************************************")
        return

    def test(self):
        getheight(None)
        print("****")
        self.getheight()


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    t = AVLtree()
    t.traversale()
    lst = list(range(10))
    random.shuffle(lst)
    for i in lst:
        t.insert(i)
        t.traversale()
    random.shuffle(lst)
    for i in lst:
        t.del_node(i)
        t.traversale()
