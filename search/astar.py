#!/usr/bin/env python3
from dataclasses import dataclass
from search_templates import Solution, HeuristicProblem
import heapq as hq


@dataclass
class Node:
    heuristic_cost : float
    real_cost : float
    count : int
    state : object
    old_state : object
    action : object
    def __lt__(self, other):
        return (self.heuristic_cost, self.real_cost, self.count) < (other.heuristic_cost, other.real_cost, other.count)


def retrieve_actions(actions, state):
    node = None
    result = []
    while state is not None and state in actions:
        node = actions[state]
        state = node.old_state
        result.append(node.action)
    return result[:-1][::-1]

def AStar(prob: HeuristicProblem) -> Solution:
    """Return Solution of the problem solved by AStar search."""

    count = 0 # tie breaker
    q = [Node(0 + 0 + prob.estimate(prob.initial_state()), 0, count, prob.initial_state(), None, None)]

    visited = {} # not exapanded nodes, but all nodes that have been in queue so far
    in_queue = {q[0].state : q[0].heuristic_cost}

    while q:
        node = hq.heappop(q)
        del in_queue[node.state]

        state = node.state
        real_cost = node.real_cost

        if prob.is_goal(state):
            visited[state] = node
            return Solution(retrieve_actions(visited, state), state, real_cost)
        
        if state not in visited:
            visited[state] = node
            for a in prob.actions(state):
                new_state = prob.result(state, a)
                action_cost = prob.cost(state, a)
                heuristic = prob.estimate(new_state)
                count += 1
                if new_state not in visited:

                    if new_state not in in_queue:
                        new_node = Node(real_cost + action_cost + heuristic, real_cost + action_cost, count, new_state, state, a)
                        hq.heappush(q, new_node)
                        in_queue[new_state] = real_cost + action_cost + heuristic

                    elif new_state in in_queue and in_queue[new_state] > real_cost + action_cost + heuristic:
                        new_node = Node(real_cost + action_cost + heuristic, real_cost + action_cost, count, new_state, state, a)
                        q = [n for n in q if n != new_node]
                        hq.heapify(q)
                        hq.heappush(q, new_node)
                        in_queue[new_state] = real_cost + action_cost + heuristic

                

    return None

