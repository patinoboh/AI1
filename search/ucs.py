#!/usr/bin/env python3
from search_templates import Problem, Solution
from typing import Optional

from queue import PriorityQueue


def ucs(prob: Problem) -> Optional[Solution]:
    """Return Solution of the problem solved by UCS search."""
    # ucs = UniformCostSearch
    
    # graph search = no repeated state
    # tree search = repeated state
    
    Q = PriorityQueue()
    Q.put((0, (prob.initial_state(), []) ))
    visited = []

    while not Q.empty():
        total_cost, (state, actions) = Q.get()
        visited.append(state)        
        for a in prob.actions(state):
            new_state = prob.result(state, a)
            cost = prob.cost(state, a)
            if prob.is_goal(new_state):
                return Solution(actions.append(a), new_state, total_cost + cost)
            
            elif state not in visited:
                Q.put((total_cost + cost, (new_state, actions+[a]) ))
                visited.append(new_state)
    return None
    # return Solution([actions leading to goal], goal_state, path_cost)
