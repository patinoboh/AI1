#!/usr/bin/env python3
from search_templates import Solution, HeuristicProblem
from queue import PriorityQueue


def retrieve_actions(actions, state):
    result = []
    action = None
    while state is not None and state in actions:
        state, action = actions[state]
        result.append(action)
    return result[:-1][::-1]

def AStar(prob: HeuristicProblem) -> Solution:
    """Return Solution of the problem solved by AStar search."""
    # Your implementation goes here.

    Q = PriorityQueue()
    count = 0
    heuristic = prob.estimate(prob.initial_state())

    #      g + h,     g, count, state,     previouse_state, action
    Q.put((heuristic, 0, count, prob.initial_state(), None, None))
    visited = {}

    while not Q.empty():
        _, path_cost, _, state, old_state, action = Q.get()

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
                    heuristic = prob.estimate(new_state)
                    Q.put( (path_cost + action_cost + heuristic, path_cost + action_cost, count, new_state, state, a ) )
    return None

