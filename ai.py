from __future__ import print_function
from game import sd_peers, sd_spots, sd_domain_num, init_domains, \
    restrict_domain, SD_DIM, SD_SIZE
import random, copy

class AI:
    def __init__(self):
        pass

    def solve(self, problem):
        domains = init_domains()
        restrict_domain(domains, problem) 

        assignments = {(-1, -1): 0}
        decision_stack = []

        # TODO: implement backtracking search. 
        while True:
            assignments, domains = self.propagate(domains, assignments)
            
            if assignments[(-1,-1)] != -1:      # no conflicts
                if len(assignments.keys) == 82  : # finished! all assigned
                    return domains
                else:                           # not finished, need to make a decision
                    assignments, location = self.make_decision(domains, assignments)
                    decision_stack.append( (assignments, location, domains) )
            else:                               # there is a conflict
                if len(decision_stack) == 0:    # no more 'previous decisions' the initial setup has a conlict
                    print('\n##################\nno solution.\n#################\n')
                    return None
                else:                           # more previous decisions
                    assignments, domains = self.backtrack(decision_stack)
        
        

        # TODO: delete this block ->
        # Note that the display and test functions in the main file take domains as inputs. 
        #   So when returning the final solution, make sure to take your assignment function 
        #   and turn the value into a single element list and return them as a domain map. 
        for spot in sd_spots:
            domains[spot] = [1]
        return domains
        # <- TODO: delete this block

    # TODO: add any supporting function you need

    # propogate returns assignment, domain as a tuple ?
    def propagate(self, domains, assignments):
        
        while True:
            there_are_singletons = False
            # do assignments for singletons
            for key in list(domains.keys()):   
                if len(domains[key]) == 1:
                    assignments[key] = domains[key][1]
                    there_are_singletons = True

            if not there_are_singletons:
                return assignments, domains

            # update domain for assigned x's
            for key in list(assignments.keys()):
                domains[key].remove(assignments[key])

            # check conflicts ?
            for domain in list(domain.values()):
                if len(domain) <= 0:
                    assignments[(-1,-1)] = -1 # this indicates conflict.
                    return assignments, domain

    def make_decision(self, domains, assignments):
        # remove all assigned locations from the key
        for key in list(domains.keys()):
            if len(domains[key]) != 1:
                assignments[key] = domains[key][0]
                return assignments, key
        # NOTE: we cant make a decision if all domains are length 1 (or 0)

    def backtrack(self, decision_stack):
        assignments, location, domains = decision_stack.pop()
        assigned_value = assignments[location];
        assignments.pop(location, None)
        domains[location].remove(assigned_value)
        return assignments, domains

    #### The following templates are only useful for the EC part #####

    # EC: parses "problem" into a SAT problem
    # of input form to the program 'picoSAT';
    # returns a string usable as input to picoSAT
    # (do not write to file)
    def sat_encode(self, problem):
        text = ""

        # TODO: write CNF specifications to 'text'

        return text

    # EC: takes as input the dictionary mapping 
    # from variables to T/F assignments solved for by picoSAT;
    # returns a domain dictionary of the same form 
    # as returned by solve()
    def sat_decode(self, assignments):
        # TODO: decode 'assignments' into domains
        
        # TODO: delete this ->
        domains = {}
        for spot in sd_spots:
            domains[spot] = [1]
        return domains
        # <- TODO: delete this
