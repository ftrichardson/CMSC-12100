# CS121 Lab 3: Function


def are_any_true(lst):
    assert all(isinstance(x, bool) for x in lst)

    for boolean in lst:
        if boolean:
            return True
    
    return False

def add_lists(lst1, lst2):
    assert len(lst1) == len(lst2)
    new_lst = []

    for index, __ in enumerate(lst1):
        new_lst.append(lst1[index] + lst2[index])
    
    return new_lst

def add_one(lst):
    for index, __ in enumerate(lst):
        lst[index] += 1


def go():
    '''
    Write code to verify that your functions work as expected here.
    Try to think of a few good examples to test your work.
    '''

    a = [1, 2, 3, 4, 5]
    add_one(a)
    print(a)


if __name__ == "__main__":
    go()

