def add_one_and_multiply(a, x):
    """ Add 1 to a, and multiply by x"""
    return (a + 1) * x


def within_range(x, lb, ub):
    """ Is x strictly between lb and ub?"""
    return x > lb and x < ub


def number_string(x):
    """
    Given a number x, produce a string: "POSITIVE", "NEGATIVE", "ZERO"
    (depending on whether the number is positive, negative, or zero)
    """
    if x > 0:
        return 'POSITIVE'
    elif x < 0:
        return 'NEGATIVE'
    else:
        return 'ZERO'
        

def num_divisible(lb, ub, p, q):
    """
    How many numbers between lb and ub (inclusive)
    are divisible by both p and q?
    """
    p_q_divisible_cnt = 0

    for num in range(lb, ub + 1):
        if num % p == 0 and num % q == 0:
            p_q_divisible_cnt += 1

    return p_q_divisible_cnt

    
def count_negative(lst):
    """
    Count the number of negative numbers in the list
    """
    negative_cnt = 0

    for num in lst:
        if num < 0:
            negative_cnt += 1

    return negative_cnt


def negate_list(lst):
    """
    Produce a *new* list with its values negated
    """
    # Format of list comprehension...
    # [(expression with item) for (item) in (list) if (item meets a condition)]]
    return [-x for x in lst]