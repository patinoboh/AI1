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

    while q:
        node = hq.heappop(q)

        state = node.state
        real_cost = node.real_cou
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
                    in_q = [n for n in q if n.state == new_state]
                    new_node = Node(heuristic + real_cost + action_cost, real_cost + action_cost, count, new_state, state, a)
                    if in_q:
                        q = [n for n in q if n.state != new_state]
                        q.append(new_node)
                        hq.heapify(q)
                    else:
                        hq.heappush(q, new_node)

                        

                    

                

    return None

