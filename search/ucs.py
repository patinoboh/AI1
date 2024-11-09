#!/usr/bin/env python3
from search_templates import Problem, Solution
from typing import Optional

from dataclasses import dataclass
import heapq as hq


@dataclass
class Node:
    path_cost : float
    count : int
    state : object
    old_state : object
    action : object
    def __lt__(self, other):
        return (self.path_cost, self.count) < (other.path_cost, other.count)


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
    
    count = 0
    q = [Node(0, count, prob.initial_state(), None, None)]
    visited = {}

    while q:
        node = hq.heappop(q)
        # q = [n for n in q if n.state != node.state]
        # hq.heapify(q)

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
                    hq.heappush(q, Node(path_cost + action_cost, count, new_state, state, a ) )
    return None
