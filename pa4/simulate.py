'''
Polling places

FLYNN RICHARDSON

Main file for polling place simulation
'''

from os import wait
import sys
import random
import queue
import click
import util

HOURS_TO_MINUTES = 60


class Voter(object):
    def __init__(self, arrival_time, voting_duration):
        '''
        Constructor

        Inputs:
            arrival_time: the time a voter arrives at the polls
            voting_duration: the time a voter takes to vote
        '''
        self.arrival_time = arrival_time
        self.voting_duration = voting_duration
        self.start_time = None
        self.departure_time = None


class Precinct(object):
    def __init__(self, name, hours_open, max_num_voters,
                 num_booths, arrival_rate, voting_duration_rate):
        '''
        Constructor for the Precinct class

        Input:
            name: (str) Name of the precinct
            hours_open: (int) Hours the precinct will remain open
            max_num_voters: (int) Number of voters in the precinct
            num_booths: (int) Number of voting booths in the precinct
            arrival_rate: (float) Rate at which voters arrive
            voting_duration_rate: (float) Lambda for voting duration
        '''
        self.name = name
        self.hours_open = hours_open
        self.max_num_voters = max_num_voters
        self.num_booths = num_booths
        self.arrival_rate = arrival_rate
        self.voting_duration_rate = voting_duration_rate


    def simulate(self, percent_straight_ticket, straight_ticket_duration, seed):
        '''
        Simulate a day of voting

        Input:
            percent_straight_ticket: (float) Percentage of straight-ticket
              voters as a decimal between 0 and 1 (inclusive)
            straight_ticket_duration: (float) Voting duration for
              straight-ticket voters
            seed: (int) Random seed to use in the simulation

        Output:
            List of voters who voted in the precinct
        '''
        voters = []
        random.seed(seed)
        time_elapsed = 0.0
        voting_booth = VotingBooths(self.num_booths)

        for __ in range(self.max_num_voters):
            gap, voting_duration = util.gen_voter_parameters(self.arrival_rate, self.voting_duration_rate, \
                                                             percent_straight_ticket, straight_ticket_duration)
            if gap + time_elapsed > self.hours_open * HOURS_TO_MINUTES:
                break
            else:
                voter = Voter(gap + time_elapsed, voting_duration)
                voting_booth.update_voting_booth(voter)
                voters.append(voter)
                time_elapsed += gap
        
        return voters


class VotingBooths(object):
    def __init__(self, num_booths):
        '''
        Constructor

        Inputs:
            num_booths: the size of a VotingBooths instance
        '''
        self.__voting_booth = queue.PriorityQueue(maxsize=num_booths)
    

    def update_voting_booth(self, voter):
        '''
        Updates the voting booth *in-place* with voter

        Inputs:
            voter: a Voter instance 
        '''
        voter.start_time = voter.arrival_time

        if self.__voting_booth.full():
            previous_departure_time = self.__voting_booth.get()
            if previous_departure_time > voter.arrival_time:
                voter.start_time = previous_departure_time
        
        voter.departure_time = voter.start_time + voter.voting_duration
        self.__voting_booth.put(voter.departure_time)


def find_avg_wait_time(precinct, percent_straight_ticket, ntrials, initial_seed=0):
    '''
    Simulates a precinct multiple times with a given percentage of
    straight-ticket voters. For each simulation, computes the average
    waiting time of the voters, and returns the median of those average
    waiting times.

    Input:
        precinct: (dictionary) A precinct dictionary
        percent_straight_ticket: (float) Percentage straight-ticket voters
        ntrials: (int) The number of trials to run
        initial_seed: (int) Initial seed for random number generator

    Output:
        The median of the average waiting times returned by simulating
        the precinct 'ntrials' times.
    '''
    wait_times = []
    precinct_to_simulate = Precinct(precinct['name'], precinct['hours_open'], precinct['num_voters'], \
                                    precinct['num_booths'], precinct['arrival_rate'], precinct['voting_duration_rate'])
    
    for __ in range(ntrials):
        total_wait_time = 0
        voters = precinct_to_simulate.simulate(percent_straight_ticket, precinct['straight_ticket_duration'], \
                                               initial_seed)
        for voter in voters:
            total_wait_time += voter.start_time - voter.arrival_time
        
        avg_wait_time = total_wait_time / len(voters)
        wait_times.append(avg_wait_time)
        initial_seed += 1
    
    return sorted(wait_times)[ntrials // 2]
  
    
def find_percent_split_ticket(precinct, target_wait_time, ntrials, seed=0):
    '''
    Finds the percentage of split-ticket voters needed to bound
    the (average) waiting time.

    Input:
        precinct: (dictionary) A precinct dictionary
        target_wait_time: (float) The minimum waiting time
        ntrials: (int) The number of trials to run when computing
                 the average waiting time
        seed: (int) A random seed

    Output:
        A tuple (percent_split_ticket, waiting_time) where:
        - percent_split_ticket: (float) The percentage of split-ticket
                                voters that ensures the average waiting time
                                is above target_waiting_time
        - waiting_time: (float) The actual average waiting time with that
                        percentage of split-ticket voters

        If the target waiting time is infeasible, returns (0, None)
    '''
    for percent_straight in range(10, -1, -1):
        avg_wait_time = find_avg_wait_time(precinct, percent_straight / 10, ntrials, seed)
        if avg_wait_time > target_wait_time:
            percent_split = 1 - (percent_straight / 10)
            return (percent_split, avg_wait_time)
    
    return (1, None)


# DO NOT REMOVE THESE LINES OF CODE
# pylint: disable-msg= invalid-name, len-as-condition, too-many-locals
# pylint: disable-msg= missing-docstring, too-many-branches
# pylint: disable-msg= line-too-long
@click.command(name="simulate")
@click.argument('precincts_file', type=click.Path(exists=True))
@click.option('--target-wait-time', type=float)
@click.option('--print-voters', is_flag=True)
def cmd(precincts_file, target_wait_time, print_voters):
    precincts, seed = util.load_precincts(precincts_file)

    if target_wait_time is None:
        voters = {}
        for p in precincts:
            precinct = Precinct(p["name"],
                                p["hours_open"],
                                p["num_voters"],
                                p["num_booths"],
                                p["arrival_rate"],
                                p["voting_duration_rate"])
            voters[p["name"]] = precinct.simulate(p["percent_straight_ticket"], p["straight_ticket_duration"], seed)
        print()
        if print_voters:
            for p in voters:
                print("PRECINCT '{}'".format(p))
                util.print_voters(voters[p])
                print()
        else:
            for p in precincts:
                pname = p["name"]
                if pname not in voters:
                    print("ERROR: Precinct file specified a '{}' precinct".format(pname))
                    print("       But simulate_election_day returned no such precinct")
                    print()
                    sys.exit(-1)
                pvoters = voters[pname]
                if len(pvoters) == 0:
                    print("Precinct '{}': No voters voted.".format(pname))
                else:
                    pl = "s" if len(pvoters) > 1 else ""
                    closing = p["hours_open"]*60.
                    last_depart = pvoters[-1].departure_time
                    avg_wt = sum([v.start_time - v.arrival_time for v in pvoters]) / len(pvoters)
                    print("PRECINCT '{}'".format(pname))
                    print("- {} voter{} voted.".format(len(pvoters), pl))
                    msg = "- Polls closed at {} and last voter departed at {:.2f}."
                    print(msg.format(closing, last_depart))
                    print("- Avg wait time: {:.2f}".format(avg_wt))
                    print()
    else:
        precinct = precincts[0]

        percent, avg_wt = find_percent_split_ticket(precinct, target_wait_time, 20, seed)

        if percent == 0:
            msg = "Waiting times are always below {:.2f}"
            msg += " in precinct '{}'"
            print(msg.format(target_wait_time, precinct["name"]))
        else:
            msg = "Precinct '{}' exceeds average waiting time"
            msg += " of {:.2f} with {} percent split-ticket voters"
            print(msg.format(precinct["name"], avg_wt, percent*100))


if __name__ == "__main__":
    cmd() # pylint: disable=no-value-for-parameter