#!/usr/bin/env python3
from game.controllers import PacManControllerBase
from game.pacman import Game, DM, Direction
from typing import List
import sys
from os.path import dirname
from enum import Enum

# hack for importing from parent package
sys.path.append(dirname(dirname(dirname(dirname(__file__))))) # TODO change back to 3 dirnames

from search_templates import *
from ucs import ucs


# i do not use this one
class PacProblem(Problem):
    def __init__(self, game: Game) -> None:
        self.game: Game = game

    def initial_state(self) -> int:
        return self.game

    def actions(self, state: int) -> List[int]:
        # return self.game.get_possible_pacman_dirs(True)a
        return self.game.get_possible_dirs(state)

    def result(self, state: int, action: int) -> int:
        return self.game.get_neighbor(state, action)

    def is_goal(self, state: int) -> bool:
        return True

    def cost(self, state: int, action: int) -> float:
        return 1


# this is the shit
class ProblemOdDo(Problem):
    def __init__(self, game, start_pos, end_pos):
        self.game = game
        self.start = start_pos
        self.end = end_pos

    def initial_state(self):
        return self.start
    
    def actions(self, state):
        return self.game.get_possible_dirs(state)
    
    def result(self, state, action):
        return self.game.get_neighbor(state, action)
    
    def is_goal(self, state):
        return state == self.end
    
    def cost(self, state, action):
        return 1




class PacManStatus(Enum):
    DEFAULT = 0
    BAITING = 1
    EATING = 0


class Patrik(PacManControllerBase):

    def tick(self, game: Game) -> None:
        pacman = self.game.pac_loc        
        
        active_pills = game.get_active_pills_nodes()
        nearest_pill = game.get_target(pacman, active_pills, True, DM.PATH)
        active_power_pills = game.get_active_power_pills_nodes()
        nearest_active_power = game.get_target(pacman, active_power_pills, True, DM.PATH)
        
        fruit = self.game.fruit_loc
        
        ghost_locs = self.game.ghost_locs
        ghost_dirs = self.game.ghost_dirs
        
        eating_time = self.game.eating_time
        edible_times = self.game.edible_times

        print(f"fruit {fruit}")
        print(f"hore : {self.game.get_neighbor(pacman, Direction.UP)}")
        print(f"active pills {active_power_pills}")
        # print(f"dole : {self.game.get_neighbor(pacman, Direction.DOWN)}")
        # print(f"dolava : {self.game.get_neighbor(pacman, Direction.LEFT)}")
        # print(f"doprava : {self.game.get_neighbor(pacman, Direction.RIGHT)}")

        status = PacManStatus.DEFAULT

        if status == PacManStatus.DEFAULT:
            print("DEFAULT STATUS")
            # chod cim blizsie k cukriku a baiti

            
        elif status == PacManStatus.BAITING:
            print("BAITING STATUS")


        elif status == PacManStatus.EATING:
            return

        
        targets = active_pills + active_power_pills


        print("ghosts : ", " , ".join(str(x) for x in ghost_locs))

        kam = active_power_pills[0] if active_power_pills else ghost_locs[0]

        mojproblem = ProblemOdDo(self.game, pacman, kam)
        sol = ucs(mojproblem)
        if sol is not None and sol.actions:
            print(f"JO : {sol.actions[0]}")
            self.pacman.set(sol.actions[0])

        # print(f"Chod takto : \n {ucs(mojproblem).actions}")

        # print(f"eating_time {eating_time}")
        # print(f"ghost_locs {ghost_locs}")
        # print(f"ghost_dirs {ghost_dirs}")
        # print(f"edible_times {edible_times}")




        # ghost_locs = self.game.ghost_locs()
        prob = PacProblem(game)
        sol = ucs(prob)
                
        if sol is None or not sol.actions:
            pass
            # if self.verbose:
            #     print("No path found.", file=sys.stderr)
        else:
            self.pacman.set(sol.actions[0])
