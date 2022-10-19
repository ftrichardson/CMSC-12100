"""
CS121: Schelling Model of Housing Segregation

  Program for simulating a variant of Schelling's model of
  housing segregation.  This program takes six parameters:

    filename -- name of a file containing a sample city grid

    R - The radius of the neighborhood: a home at Location (k, l) is in
        the neighborhood of the home at Location (i,j) if 0 <= k < N,
        0 <= l < N, and 0 <= |i-k| + |j-l| <= R.

    similarity_satisfaction_range (lower bound and upper bound) -
         acceptable range for ratio of the number of
         homes of a similar color to the number
         of occupied homes in a neighborhood.

   patience - number of satisfactory homes that must be visited before choosing
              the last one visited.

   max_steps - the maximum number of passes to make over the city
               during a simulation.

  Sample: python3 schelling.py --grid_file=tests/a20-sample-writeup.txt --r=1
         --sim_lb=0.40 --sim_ub=0.7 --patience=3 --max_steps=1
  The sample command is shown on two lines, but should be entered on
  a single line in the linux command-line
"""

import click
import utility


def is_satisfied(grid, R, location, sim_sat_range):
    '''
    Determine whether or not the homeowner at a specific location is
    satisfied using an R-neighborhood centered around the location.
    That is, is does their similarity score fall with the specified
    range (inclusive)

    Inputs:
        grid: the grid
        R (int): neighborhood parameter
        location (int, int): a grid location
        sim_sat_range (float, float): lower bound and upper bound on
          the range (inclusive) for when the homeowner is satisfied
          with his similarity score.

    Returns: bool
    '''
    (i, j) = location
    assert grid[i][j] != 'F'

    S = 0
    H = 0

    for k in range(max(0, i - R), min(len(grid), i + R + 1)):
        for l in range(max(0, j - R), min(len(grid), j + R + 1)):
            if abs(i - k) + abs(j - l) <= R:
                if grid[k][l] != 'F':
                    H += 1
                if grid[k][l] == grid[i][j]:
                    S += 1
    
    similarity_score = S / H
    return similarity_score >= min(sim_sat_range) and similarity_score <= max(sim_sat_range)


def swap_homes(grid, open_location, unsatisfied_homeowner):
    '''
    Swaps an unsatisfied homeowner to an unoccupied home

    Inputs:
        open_location: (tuple) an unoccupied location
        unsatisfied_homeowner: (tuple) the location of an unsatisfied homeowner
    '''
    (i, j) = open_location
    assert grid[i][j] == 'F'
    (k, l) = unsatisfied_homeowner

    grid[i][j], grid[k][l] = grid[k][l], grid[i][j]


def is_homeowner_relocated(grid, R, sim_sat_range, unsatisfied_homeowner, homes_for_sale, patience):
    '''
    Tries to relocate an unsatisfied homeowner to a satisfactory home

    Inputs:
        grid (list of lists of strings): the grid
        R (int): neighborhood parameter
        sim_sat_range (float, float): lower bound and upper bound on
          the range (inclusive) for when the homeowner is satisfied
          with his similarity score.
        unsatisfied_homeowner (int, int): location of unsatisfied homeowner
        homes_for_sale (list of tuples): a list of locations with homes for sale
        patience (int): the number of satisfactory homes an unsatisfied homeowner
           will visit before relocating

    Returns: bool
    '''
    assert not is_satisfied(grid, R, unsatisfied_homeowner, sim_sat_range)
    is_relocated = False

    for open_home in homes_for_sale:
        swap_homes(grid, open_home, unsatisfied_homeowner)
        if is_satisfied(grid, R, open_home, sim_sat_range):
            patience -= 1
            if patience == 0:
                homes_for_sale.remove(open_home)
                homes_for_sale.insert(0, unsatisfied_homeowner)
                is_relocated = True
                break
            swap_homes(grid, unsatisfied_homeowner, open_home)
        else:
            swap_homes(grid, unsatisfied_homeowner, open_home)
    
    return is_relocated


def simulation_wave(grid, R, sim_sat_range, homes_for_sale, patience, homeowner_color):
    '''
    Performs a wave (based on homeowner color) of the simulation

    Inputs:
        grid (list of lists of strings): the grid
        R (int): neighborhood parameter
        sim_sat_range (float, float): lower bound and upper bound on
          the range (inclusive) for when the homeowner is satisfied
          with his similarity score.
        homes_for_sale (list of tuples): a list of locations with homes for sale
        patience (int): the number of satisfactory homes an unsatisfied homeowner
          is willing to visit before making a decision
        homeowner_color (string): the color of a homeowner
        
    Returns: (int) number of relocations
    '''
    num_relocations = 0

    for i, __ in enumerate(grid):
        for j, __ in enumerate(grid):
            if grid[i][j] == homeowner_color and not is_satisfied(grid, R, (i, j), sim_sat_range):
                if is_homeowner_relocated(grid, R, sim_sat_range, (i, j), homes_for_sale, patience):
                    num_relocations += 1
    
    return num_relocations


def simulation_step(grid, R, sim_sat_range, homes_for_sale, patience):
    '''
    Performs a step of the simulation

    Inputs:
        grid (list of lists of strings): the grid
        R (int): neighborhood parameter
        sim_sat_range (float, float): lower bound and upper bound on
          the range (inclusive) for when the homeowner is satisfied
          with his similarity score.
        homes_for_sale (list of tuples): a list of locations with homes for sale
        patience (int): the number of satisfactory homes an unsatisfied homeowner
          is willing to visit before making a decision

    Returns: (int) number of relocations
    '''
    num_relocations = 0
    num_relocations += simulation_wave(grid, R, sim_sat_range, homes_for_sale, patience, 'M')
    num_relocations += simulation_wave(grid, R, sim_sat_range, homes_for_sale, patience, 'B')
    return num_relocations


def do_simulation(grid, R, sim_sat_range, patience, max_steps, homes_for_sale):
    '''
    Do a full simulation.

    Inputs:
        grid (list of lists of strings): the grid
        R (int): neighborhood parameter
        sim_sat_range (float, float): lower bound and upper bound on
          the range (inclusive) for when the homeowner is satisfied
          with his similarity score.
        max_steps (int): maximum number of steps to do
        for_sale (list of tuples): a list of locations with homes for sale

    Returns: (int) The number of relocations completed.
    '''
    total_relocations = 0

    for __ in range(max_steps):
        num_relocations = simulation_step(grid, R, sim_sat_range, homes_for_sale, patience)
        if num_relocations == 0:
            break
        else:
            total_relocations += num_relocations
    
    return total_relocations


@click.command(name="schelling")
@click.option('--grid_file', type=click.Path(exists=True))
@click.option('--r', type=int, default=1,
              help="neighborhood radius")
@click.option('--sim_lb', type=float, default=0.40,
              help="Lower bound of similarity range")
@click.option('--sim_ub', type=float, default=0.70,
              help="Upper bound of similarity range")
@click.option('--patience', type=int, default=1, help="patience level")
@click.option('--max_steps', type=int, default=1)
def cmd(grid_file, r, sim_lb, sim_ub, patience, max_steps):
    '''
    Put it all together: do the simulation and process the results.
    '''

    if grid_file is None:
        print("No parameters specified...just loading the code")
        return

    grid = utility.read_grid(grid_file)
    for_sale = utility.find_homes_for_sale(grid)
    sim_sat_range = (sim_lb, sim_ub)


    if len(grid) < 20:
        print("Initial state of city:")
        for row in grid:
            print(row)
        print()

    num_relocations = do_simulation(grid, r, sim_sat_range, patience,
                                    max_steps, for_sale)

    if len(grid) < 20:
        print("Final state of the city:")
        for row in grid:
            print(row)
        print()

    print("Total number of relocations done: " + str(num_relocations))


if __name__ == "__main__":
    cmd() # pylint: disable=no-value-for-parameter