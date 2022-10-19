def is_pythagorean_triple(a, b, c):
    """
    Do a, b, and c form a Pythagorean Triple?

    a, b, c: ints

    Returns: bool
    """
    return a**2 + b**2 == c**2

def characterize_nums(lst):
    """
    Characterize a list by counting the number of negative
    numbers, zeros, and positive numbers.

    lst: list of ints

    Returns: (int, int, int)
    """
    negative_cnt = 0
    zero_cnt = 0
    positive_cnt = 0

    for num in lst:
        if num < 0:
            negative_cnt += 1
        elif num > 0:
            positive_cnt += 1
        else:
            zero_cnt += 1
    
    return (negative_cnt, zero_cnt, positive_cnt)

def compute_matching(lst1, lst2):
    """
    Given two lists of equal length, compute a list
    that where the ith element is True if the lists
    match at index i.

    lst1, lst2: lists

    Returns: list of bools
    """
    ### Leave this assertion
    assert len(lst1) == len(lst2)

    new_lst = []

    for i, __ in enumerate(lst1):
        new_lst.append(lst1[i] == lst2[i])
    
    return new_lst

def compute_matching_indices(lst1, lst2):
    """
    Given two lists of equal length, compute a list that of the
    indices where the two lists have the same value.

    lst1, lst2: lists

    Returns: list of integer indices
    """
    ### Leave this assertion
    assert len(lst1) == len(lst2)

    new_lst = []

    for i, __ in enumerate(lst1):
        if lst1[i] == lst2[i]:
            new_lst.append(i)
    
    return new_lst


def destructive_negate(lst):
    """
    Negate the value of each element in the list *in place*.

    lst: list of ints
    """
    for i, __ in enumerate(lst):
        lst[i] *= -1

def win_lose_or_draw(board, row, col):
    """
    Returns "Win", "Lose", or "Draw" depending on whether sum of the 
    values in the row is larger, smaller, or the same as the sum
    of the values in the column

    board: list of lists of ints
    row: int
    col: int

    Returns: string: "Win", "Lose", or "Draw"
    """
    # A column of a list of lists is simply...
    # [lst[row_index][col (fixed)] for row_index, __ in enumerate(lst)]
    column_sum = 0
    for i, __ in enumerate(board):
        column_sum += board[i][col]

    row_sum = sum(board[row])

    if row_sum > column_sum:
        return 'Win'
    elif column_sum > row_sum:
        return 'Lose'
    else:
        return 'Draw'