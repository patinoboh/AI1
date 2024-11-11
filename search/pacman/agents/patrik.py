#!/usr/bin/env python3
from game.controllers import PacManControllerBase
from game.pacman import Game, DM, Direction
from typing import List
import sys
from os.path import dirname

# hack for importing from parent package
sys.path.append(dirname(dirname(dirname(dirname(__file__))))) # TODO change back to 3 dirnames

from search_templates import *
from ucs import ucs


class PacProblem(Problem):
    def __init__(self, game: Game) -> None:
        self.game: Game = game

    def initial_state(self) -> int:
        return self.game

    def actions(self, state: int) -> List[int]:
        return self.game.get_possible_pacman_dirs(True)

    def result(self, state: int, action: int) -> int:
        return 0

    def is_goal(self, state: int) -> bool:
        return True

    def cost(self, state: int, action: int) -> float:
        return 1


class Patrik(PacManControllerBase):

    def tick(self, game: Game) -> None:
        fruit = self.game.fruit_loc
        pacman = self.game.pac_loc
        # eating_time = self.game.eating_time()
        ghost_locs = self.game.ghost_locs
        # ghost_dirs = self.game.ghost_dirs()
        # edible_times = self.game.edible_times()

        print(f"fruit {fruit}")
        print(f"pacman {pacman}")
        print("ghosts : ", " , ".join(str(x) for x in ghost_locs))

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
