#!/usr/bin/env python3
from search_templates import Solution, HeuristicProblem
from queue import PriorityQueue


def AStar(prob: HeuristicProblem) -> Solution:
    """Return Solution of the problem solved by AStar search."""
    # Your implementation goes here.

    Q = PriorityQueue()
    count = 0
    heuristic = prob.estimate(prob.initial_state())

    #      f + h,     f, count, state,              actions
    Q.put((heuristic, 0, count, prob.initial_state(), []))
    visited = set()

    while not Q.empty():
        _, path_cost, _, state, actions = Q.get()

        if prob.is_goal(state):
            return Solution(actions, state, path_cost)
        
        if state not in visited:
            visited.add(state)
            for a in prob.actions(state):
                new_state = prob.result(state, a)
                action_cost = prob.cost(state, a)
                if new_state not in visited:
                    count += 1
                    heuristic = prob.estimate(new_state)
                    Q.put( (path_cost + action_cost + heuristic, path_cost + action_cost, count, new_state, actions + [a] ) )
    return None

