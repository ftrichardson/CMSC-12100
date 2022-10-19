def f(x):
    '''
    Real valued square function  f(x) == x^2
    '''

    return x*x

def integrate():
    ''' Integrate the function f using the rectangle method '''
    N = 10000
    width = 1 / N
    total_area = 0

    for i in range(N):
        # Good opportuity to use descriptive variable names (e.g. abstracting
        # f(i * width) to height)
        height = f(i * width)
        total_area += height * width
    
    return total_area