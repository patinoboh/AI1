#!/usr/bin/env python3
from search_templates import Problem, Solution
from typing import Optional

from queue import PriorityQueue

def retrieve_actions(actions, state):
    result = []
    action = None
    while state is not None and state in actions:
        state, action = actions[state]
        result.append(action)
    return result[:-1][::-1]

def ucs(prob: Problem) -> Optional[Solution]:
    """Return Solution of the problem solved by UCS search."""
    # ucs = UniformCostSearch
    
    # graph search = no repeated state
    # tree search = repeated state
    
    Q = PriorityQueue()
    count = 0
    #   path, count,    state,    previous_state,  action
    Q.put((0, count, prob.initial_state(), None, None))
    
    visited = {}

    while not Q.empty():
        path_cost, _, state, old_state, action = Q.get()

        if prob.is_goal(state):
            visited[state] = (old_state, action)
            return Solution(retrieve_actions(visited, state), state, path_cost)

        if state not in visited:
            visited[state] = (old_state, action)
            for a in prob.actions(state):
                new_state = prob.result(state, a)
                action_cost = prob.cost(state, a)
                if new_state not in visited:
                    count += 1
                    Q.put( (path_cost + action_cost, count, new_state, state, a ) )
    return None
