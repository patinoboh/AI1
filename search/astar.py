#!/usr/bin/env python3
from dataclasses import dataclass
from search_templates import Solution, HeuristicProblem
import heapq as hq


@dataclass
class Node:
    heuristic_cost : float
    path_cost : float
    count : int
    state : object
    old_state : object
    action : object
    def __lt__(self, other):
        return (self.heuristic_cost, self.path_cost, self.count) < (other.heuristic_cost, other.path_cost, other.count)


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

    count = 0
    heuristic = prob.estimate(prob.initial_state())
    q = [Node(heuristic, 0, count, prob.initial_state(), None, None)]

    visited = {}

    while q:
        node = hq.heappop(q)

        path_cost = node.path_cost        
        state = node.state
        old_state = node.old_state
        action = node.action

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
                    new_node = Node(path_cost + action_cost + heuristic, path_cost + action_cost, count, new_state, state, a)
                    hq.heappush(q, new_node)
    return None

