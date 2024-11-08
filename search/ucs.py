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
    count = 0
    Q.put((0, count, prob.initial_state(), []))
    visited = set()

    while not Q.empty():
        total_cost, _, state, actions = Q.get()

        if prob.is_goal(state):
            return Solution(actions, state, total_cost)
        
        if state not in visited:
            visited.add(state)
            for a in prob.actions(state):
                new_state = prob.result(state, a)
                if new_state not in visited:
                    count += 1
                    cost = prob.cost(state, a)
                    Q.put( (total_cost + cost, count, new_state, actions + [a] ) )
    return None
    # return Solution([actions leading to goal], goal_state, path_cost)
