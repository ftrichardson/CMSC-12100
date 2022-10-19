import numpy as np
import sys

# import linear regression and apply beta from PA #5.
from util import linear_regression, prepend_ones_column

def read_file(filename):
    '''
    Read data from the specified file.  Split the lines and convert
    float strings into floats.  Assumes the first row contains labels
    for the columns.

    Inputs:
      filename: name of the file to be read

    Returns:
      (list of strings, 2D array)
    '''
    with open(filename) as f:
        labels = f.readline().strip().split(',')
        data = np.loadtxt(f, delimiter=',', dtype=np.float64)
        return labels, data

def var(y):
    N = len(y)
    return (1 / N) * np.sum((y - y.mean())**2)

def task2(b):
    print("rows 0, 1, and 2.")
    print(b[0:3, :])
    print()
    print("rows 0, 1, and 5")
    print(b[(0, 1, 5), :])
    print()
    print("columns 0, 1, and 2")
    print(b[:, 0:3])
    print()
    print("columns 0, 1, and 3")
    print(b[:, (0, 1, 3)])
    print()
    print("columns 0, 1, and 2 from rows 2 and 3.")
    print(b[2:4, 0:3])
    print()

def go():
    __, city_data = read_file("city_data.csv")

    graffiti = city_data[:,0]
    garbage = city_data[:,3]

    print("Task 1")
    print("GRAFFITI:", var(graffiti))
    print("GARBAGE:", var(garbage))
    print()
    print()


    print("Task 2")
    b = (np.arange(24)**2).reshape(6,4)
    task2(b)


    print("Task 3")
    print("Rodents, Garbage => Crime", linear_regression(prepend_ones_column(city_data[:, 2:4]), city_data[:, 7]))
    print()
    print()


    # Must do [0] instead of 0. Extracting one column makes a one-dimensional array, but using []
    # makes a two-dimensional array, thereby keeping the dimenions
    print("Task 4")
    print("Graffiti => Crime:", linear_regression(prepend_ones_column(city_data[:, [0]]), city_data[:, 7]))
    print()
    print()

if __name__ == "__main__":
    go()