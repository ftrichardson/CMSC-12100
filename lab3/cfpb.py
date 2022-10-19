'''
Lab #4: dictionary practice
CMSC 121 / CAPP 30121
Fall 2018
'''

import json

CFPB_16 = json.load(open("cfpb16_1000.json"))


# Task 1
def count_complaints_about(complaints, company_name):
    '''
    Count complaints about a specified company

    Inputs:
        complaints (list) A list of complaints, where each complaint is a
            dictionary
        company_name (str): The company name to count complaints for

    Returns: count of complaints (int)
    '''
    complaints_cnt = 0

    for complaint in complaints:
        if complaint['Company'] == company_name:
            complaints_cnt += 1
    
    return complaints_cnt

# Task 2
def find_companies(complaints):
    '''
    Compute a list of companies complained about

    Inputs:
        complaints (list) A list of complaints, where each complaint is a
            dictionary

    Returns: (list or set) of companies
    '''
    companies = set()

    for complaint in complaints:
        companies.add(complaint['Company'])
        
    return companies

# Task 3
def count_by_state(complaints):
    '''
    Compute counts by state of all complaints

    Inputs:
         complaints (list) A list of complaints, where each complaint is a
            dictionary

    Returns: (dict) that relates states to complaint number
    '''
    cnt_by_state = {}

    for complaint in complaints:
        cnt_by_state[complaint['State']] = cnt_by_state.get(complaint['State'], 0) + 1
    
    return cnt_by_state

# Task 4
def state_with_most_complaints(cnt_by_state):
    '''
    Find the state with the most complaints. Can break ties arbitrarily.

    Inputs:
        cnt_by_state (dict) A dictionary relating each state to the
            count of complaints in that state

    Returns: (str) the state with the most complaints
    '''
    max_value = float('-inf')
    most_grumbling_state = None

    for state, cnt in cnt_by_state.items():
        if cnt > max_value:
            max_value = cnt
            most_grumbling_state = state
    
    return most_grumbling_state

# Task 5
def count_by_company_by_state(complaints):
    '''
    Computes a dict of {company: {state: count, state: count}} for all states
        and companies

    Inputs:
        complaints (list) A list of complaints, where each complaint is a
            dictionary

    Returns: (dict) with count per company per state
    '''
    company_to_state_cnts = {}

    for complaint in complaints:
        company = complaint['Company']
        state = complaint['State']
        if company not in company_to_state_cnts:
            company_to_state_cnts[company] = {}
        company_to_state_cnts[company][state] = company_to_state_cnts[company].get(state, 0) + 1
    
    return company_to_state_cnts

# Task 6
def complaints_by_company(complaints):
    '''
    Create a dictionary that maps the name of a company to a list of the
    complaint dictionaries that concern that company.

    Inputs:
        complaints (list) A list of complaints, where each complaint is a
            dictionary

    Returns: (dict) mapping the name of the company to a list of complaints
    '''
    company_to_complaints = {}

    for complaint in complaints:
        if complaint['Company'] not in company_to_complaints:
            company_to_complaints[complaint['Company']] = []
        company_to_complaints[complaint['Company']].append(complaint)
    
    return company_to_complaints