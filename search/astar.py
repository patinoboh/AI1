#!/usr/bin/env python3
from dataclasses import dataclass
from search_templates import Solution, HeuristicProblem
import heapq as hq


@dataclass
class Node:
    f_n : float
    g_n : float
    tie_break : int
    state : object
    old_state : object
    action : object
    def __lt__(self, other):
        # return (self.f_n, self.g_n, self.tie_break) < (other.f_n, other.g_n, other.tie_break)
        return (self.f_n, self.tie_break) < (other.f_n, other.tie_break)


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

    tie_break = 0 # tie breaker
    #                            f_n                     , g_n,   _    , state               , previous, action
    q = [Node(0 + 0 + prob.estimate(prob.initial_state()), 0, tie_break, prob.initial_state(), None, None)]

    visited = {} # not exapanded nodes, but all nodes that have been in queue so far
    # in_queue = {q[0].state : 0} # nodes that are in queue

    max_q_size = 0
    max_visited_size = 0
    while q:
        max_q_size, max_visited_size = max(max_q_size, len(q)), max(max_visited_size, len(visited))
        node = hq.heappop(q)
        # del in_queue[node.state]

        state = node.state
        g_n = node.g_n

        if prob.is_goal(state):
            visited[state] = node
            print("Max queue size : ", max_q_size)
            print("Max visited size : ", max_visited_size)
            return Solution(retrieve_actions(visited, state), state, g_n)
        
        if state not in visited:
            visited[state] = node
            for a in prob.actions(state):
                new_state = prob.result(state, a)
                action_cost = prob.cost(state, a)
                h_n = prob.estimate(new_state)
                tie_break += 1
                if new_state not in visited:
                    new_node = Node(h_n + g_n + action_cost, g_n + action_cost, tie_break, new_state, state, a)
                    hq.heappush(q, new_node)

                    
                    # if new_state in in_queue and in_queue[new_state] > new_node.g_n + action_cost:
                    #     in_queue[new_state] = new_node.g_n + action_cost
                    #     q = [n for n in q if n.state != new_state]
                    #     q.append(new_node)
                    #     hq.heapify(q)
                    # elif new_state not in in_queue:
                    #     hq.heappush(q, new_node)
                    #     in_queue[new_state] = new_node.g_n + action_cost
            

    print("Max queue size:", max_q_size)
    print("Max visited size:", max_visited_size)
    return None
