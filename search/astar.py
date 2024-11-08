#!/usr/bin/env python3
from search_templates import Solution, HeuristicProblem
from queue import PriorityQueue


def AStar(prob: HeuristicProblem) -> Solution:
    """Return Solution of the problem solved by AStar search."""
    # Your implementation goes here.

    # VRAJ STAČÍ NAKOPČIŤ UCS A PRIDAŤ HEURISTIKU
    # h_value = prob.estimate(state)

    # POZOR že keď používame tuples a chceme ich radiť tak niekedy python nemusí vedieť porovnávač
    # 

    # sekunda je vteřina
    # ale milisekunda je už milisekunda
    Q = PriorityQueue()
    count = 0
    heuristic = prob.estimate(prob.initial_state())
    # real + heuristic, real, count, state, actions
    Q.put((heuristic, 0, count, prob.initial_state(), []))
    visited = set()

    while not Q.empty():
        _, real_cost, _, state, actions = Q.get()

        if prob.is_goal(state):
            return Solution(actions, state, real_cost)
        
        if state not in visited:
            visited.add(state)
            for a in prob.actions(state):
                new_state = prob.result(state, a)
                if new_state not in visited:
                    count += 1
                    cost = prob.cost(state, a)
                    heuristic = prob.estimate(new_state)
                    Q.put( (real_cost + cost + heuristic, real_cost + cost, count, new_state, actions + [a] ) )
    return None



    raise NotImplementedError

    # return Solution([actions leading to goal], goal_state, path_cost)
