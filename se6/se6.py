from tree import Tree

def sum_cubes(n):
    """
    Recursively calculates the sum of the first n
    positive cubes.

    Input:
        n: positive integer.
    
    Returns: (integer) the value of the sum
        1^3 + 2^3 + ... + n^3
    
    This function may not use any loops or list
    comprehensions.
    """
    if n == 1:
        return 1
    else:
        return n**3 + sum_cubes(n - 1)

def sublists(lst):
    """
    Computes all sublists of the input list.

    Input:
        lst: list of values
    
    Returns: (list of list of values) list of all
        sublists of lst.
    """
    if len(lst) == 0:
        return [[]]
    else:
        sublists_lst = []
        lst_copy = lst.copy()
        elem_to_add = lst_copy[0]
        previous_sublists_lst = sublists(lst_copy[1:])
        sublists_lst.extend(previous_sublists_lst)
        for previous_sublist in previous_sublists_lst:
            sublists_lst.append([elem_to_add] + previous_sublist)
        return sublists_lst

def min_depth_leaf(tree):
    """
    Computes the minimum depth of a leaf in the tree
    (length of shortest path from the root to a leaf).

    Input:
        tree: a Tree instance.
    
    Returns: (integer) the minimum depth of of a leaf
        in tree.
    """
    if tree.num_children() == 0:
        return 0
    else:
        min_depths = set()
        for child in tree.children:
            min_depths.add(1 + min_depth_leaf(child))
        return min(min_depths)

def repeated_value(tree):
    """
    Determines whether there is a node in the input
    tree that has an ancestor with the same value.

    Input:
        tree: a Tree instance.
    
    Returns: a boolean indicating whether there is a 
    node in the tree that has an ancestor with the 
    same value.
    """
    if repeated_value_r(tree, set()):
        return True
    else:
        return False

def repeated_value_r(tree, ancestor_values):
    """
    Helper function for repeated_value. Takes in a tree
    which may be a subtree of the original tree of
    interest, and determines if there is a node in the 
    input tree that has an ancestor in the original tree
    with the same value.

    Inputs:
        tree: a Tree instance, which may be a subtree of
            of the original tree.
        ancestor_values: the set of values of nodes in
            the original tree that are ancestors of the
            input tree.
    
    Returns: a boolean indicating whether there is a node
        in the input tree that has an ancestor in the
        original tree with the same value.
    """
    if tree.num_children() == 0:
        return tree.value in ancestor_values
    else:
        if tree.value in ancestor_values:
            return True
        else:
            ancestor_values.add(tree.value)
        for child in tree.children:
            if repeated_value_r(child, ancestor_values):
                return True
        ancestor_values.remove(tree.value)