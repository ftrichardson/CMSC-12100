from math import sin
from tree import Tree

def is_power_of_two(n):
    '''
    Checks if input is a power of two

    Inputs:
        n: an integer
    
    Returns: bool
    '''
    if n == 1:
        return True
    else:
        if n % 2 == 1:
            return False
        return is_power_of_two(n / 2)

# Memoization is very useful and efficient for recursion problems where 
# one recomputes values already computed
def fib(n, memo):
    '''
    Calculates the n-th fibonacci number using memoization

    Inputs:
        n: a positive integer
        memo: a dictionary to store results from previous recursive calculations
            in order to increase runtime efficiency

    Returns: the n-th fibonacci number 
    '''
    if n == 1:
        return 0
    elif n == 2:
        return 1
    else:
        if n in memo:
            return memo[n]
        else:
            memo[n] = fib(n - 2, memo) + fib(n - 1, memo)
            return memo[n]

def find_root_sqrt2(epsilon, a, b):
    '''
    Finds the closely estimated square root of an input

    Inputs:
        epsilon: the accepted level of deviation the estimate can be from the
            actual square root
        a: a float
        b: a float
    
    Returns: the estimated square root (a float)
    '''
    c = (a + b) / 2
    if abs(c**2 - 2) < epsilon:
        return c
    else:
        if (c**2 - 2) * (a**2 - 2) < 0:
            return find_root_sqrt2(epsilon, a, c)
        else:
            return find_root_sqrt2(epsilon, c, b)


t0 = Tree("node0", 27)

t1 = Tree("node0", 1)
child1 = Tree("node1", 2)
child1.add_child(Tree("node2", 3))
t1.add_child(child1)
t1.add_child(Tree("node3", 4))
t1.add_child(Tree("node4", 5))


def count_leaves(t):
    '''
    Count the number of leaves in the tree rooted at t
    
    Inputs: (Tree) a tree
    
    Returns: (integer) number of leaves in t
    '''
    assert t is not None

    if t.num_children() == 0:
        return 1

    num_leaves = 0
    for kid in t.children:
        num_leaves += count_leaves(kid)

    return num_leaves


def add_values(t):
    '''
    Returns the sum of all the values in a tree

    Inputs:
        t: a Tree instance
    
    Returns: int
    '''
    if t.num_children() == 0:
        return t.value
    else:
        total_value = t.value
        for child in t.children:
            total_value += add_values(child)
        return total_value