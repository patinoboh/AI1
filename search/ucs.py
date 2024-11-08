#!/usr/bin/env python3
from search_templates import Problem, Solution
from typing import Optional


def ucs(prob: Problem) -> Optional[Solution]:
    """Return Solution of the problem solved by UCS search."""
    # ucs = UniformCostSearch
    
    # graph search = no repeated state
    # tree search = repeated state
    
    Q = [(prob.initial_state(), [])]
    visited = [prob.initial_state()]
    actions = []

    while Q:
        state, actions = Q.pop(0)
        for a in prob.actions(state):
            new_state = prob.result(state, a)            
            if(prob.is_goal(new_state)):
                return Solution(actions.append(a), new_state,len(actions) + 1)
            
            if new_state not in visited:
                Q.append((new_state, actions + [a]))
                visited.append(new_state)
    return None
    # return Solution([actions leading to goal], goal_state, path_cost)
