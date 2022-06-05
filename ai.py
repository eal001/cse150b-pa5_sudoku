from __future__ import print_function
from multiprocessing.sharedctypes import Value
from threading import local
from game import sd_peers, sd_spots, sd_domain_num, init_domains, \
    restrict_domain, SD_DIM, SD_SIZE
import random, copy

class AI:
    def __init__(self):
        pass

    def solve(self, problem):
        domains = init_domains()
        restrict_domain(domains, problem) 

        assignments = {}
        decision_stack = []

        # TODO: implement backtracking search. 
        while True:
            assignments[(-1,-1)] = 0
            assignments, domains = self.propagate(domains, assignments)

            # print("look for missing values")
            
            # for i in range( 9):   # all values in the same box
            #     for j in range( 9):
            #         if( not (i,j) in assignments):
            #             print(i,j)

            # print(assignments[(-1, -1)])
            if assignments[(-1,-1)] != -1:      # no conflicts
                if len(list(assignments.keys())) == 82  : # finished! all assigned
                    return domains
                else:                           # not finished, need to make a decision
                    assignments, location = self.make_decision(domains, assignments)
                    decision_stack.append( (assignments, location, domains) )
            else:                               # there is a conflict
                if len(decision_stack) == 0:    # no more 'previous decisions' the initial setup has a conlict
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

    # location should be a 0 indexed (x, y)
    def get_relevant_coords(self, location):
        relevant_coords = []
        for i in range(9):  # all values in the same column
            if i == location[0]: continue
            relevant_coords.append((i, location[1]))

        for j in range(9): # all values in the same row
            if j == location[1]: continue
            relevant_coords.append((location[0], j))

        box_x = int(location[0] / 3)
        box_y = int(location[1] / 3)
        box_x_min = box_x * 3
        box_x_max = (box_x * 3) + 3
        box_y_min = box_y * 3
        box_y_max = (box_y * 3) + 3

        # print('loc + relevant coords')
        # print(location)
        for i in range(box_x_min, box_x_max):   # all values in the same box
            for j in range(box_y_min, box_y_max):
                # print((i,j))
                relevant_coords.append((i,j))

        relevant_coords = list(set(relevant_coords))    # return a set (one of each)
        relevant_coords.remove(location)                # make sure THIS location is not returned
        # print('relevant coords to ' + str(location)+ ' are ' + str(relevant_coords))
        return relevant_coords

    # propogate returns assignment, domain as a tuple ?
    def propagate(self, domains, assignments):
        i = 0
        # print('begin propagate')
        while True:
            # print('iteration '+str(i))
            # do assignments for singletons
            # print('singletons')
            for key in list(domains.keys()): 
                if len(domains[key]) == 1:
                    assignments[key] = domains[key][0]

            # print('reassign this assignments domains')
            # update domain for assigned x's
            for key in list(assignments.keys()):
                # print('updating domains to their assignment')
                if key == (-1,-1): continue
                domains[key] = [assignments[key]]
                # print(key)
                # print(domains[key])

            print('checking for conflicts')
            # check conflicts ?
            for location in list(domains.keys()):
                print(len(domains[key]))
                if domains[key] == []:
                    assignments[(-1,-1)] = -1 # this indicates conflict.
                    return assignments, domains

            print('update other domains')
            conflict_flag = False
            # update OTHER relevant values
            for location in list(assignments.keys()):
                
                if location == (-1,-1): continue
                # print(self.get_relevant_coords(location))
                for coord in self.get_relevant_coords(location):
                    if assignments[location] in domains[coord]:
                        print('before | after')
                        print(domains[coord])
                        conflict_flag = True
                        domains[coord].remove(assignments[location])
                        print(domains[coord])

            if(not conflict_flag):
                return assignments, domains

            # print(str(len(assignments)) + ' ' + str(len(domains)))
            i+=1
        
        
        

    def make_decision(self, domains, assignments):
        # remove all assigned locations from the key
        for key in list(domains.keys()):
            if len(domains[key]) > 1:
                assignments[key] = domains[key][0]
                print('decision made: '+ str(assignments[key]) + ' @ ' + str(key))
                return assignments, key

        # if we reach here there must be a conflict
        # return assignments, key
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
