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
    EATING = 2


class Patrik(PacManControllerBase):
    def ghosts_to_eat(self):
        return [self.game.get_ghost_loc(i) for i in range(4) if self.game.is_edible(i)]
    
    def get_opposite_dir(self, direction):
        if direction == Direction.UP:
            return Direction.DOWN
        elif direction == Direction.DOWN:
            return Direction.UP
        elif direction == Direction.LEFT:
            return Direction.RIGHT
        elif direction == Direction.RIGHT:
            return Direction.LEFT
        

    def tick(self, game: Game) -> None:
        pacman = self.game.pac_loc        
        
        active_pills = game.get_active_pills_nodes()
        nearest_pill = game.get_target(pacman, active_pills, True, DM.PATH)
        active_power_pills = game.get_active_power_pills_nodes()
        nearest_active_power = game.get_target(pacman, active_power_pills, True, DM.PATH)
        
        fruit = self.game.fruit_loc
        
        ghost_locs = self.game.ghost_locs
        ghost_distances = [self.game.get_path_distance(pacman, ghost_locs[i]) for i in range(4)]
        ghost_distances = [d if d != -1 else 10000 for d in ghost_distances]
        # print(ghost_distances)
        nearest_ghost = ghost_locs[ghost_distances.index(min(ghost_distances))]

        ghost_dirs = self.game.ghost_dirs
        
        eating_time = self.game.eating_time
        edible_times = self.game.edible_times

        
        # if active_power_pills
        # print("TOTO")
        # # print(self.game.get_path_distance(pacman, nearest_active_power))
        # # print(self.game.get_path_distance(pacman, nearest_ghost))

        self.pacman.set(Direction.NONE)
        ghosts_to_eat = self.ghosts_to_eat()
        # print(f"ghost to eat {ghosts_to_eat}")
        
        status = PacManStatus.DEFAULT
        if not ghosts_to_eat and not active_power_pills:
            status = PacManStatus.DEFAULT
        elif not ghosts_to_eat and self.game.get_path_distance(pacman, nearest_active_power) > 3:
            status = PacManStatus.DEFAULT
        elif not ghosts_to_eat and self.game.get_path_distance(pacman, nearest_active_power) <= 2:
            status = PacManStatus.BAITING
        elif ghosts_to_eat:
            status = PacManStatus.EATING

        # print(status)

        if status == PacManStatus.DEFAULT:
            # chod cim blizsie k cukriku a baiti
            self.pacman.set(ucs(ProblemOdDo(self.game, pacman, nearest_active_power)).actions[0])
        elif status == PacManStatus.BAITING:
            # print(f"\n nearest ghost \n {self.game.get_path_distance(pacman, nearest_ghost)} \n")
            dir_to_power = ucs(ProblemOdDo(self.game, pacman, nearest_active_power)).actions[0]
            opposite_dir = self.get_opposite_dir(dir_to_power)
            if self.game.get_path_distance(pacman, nearest_ghost) <= 5:
                self.pacman.set(dir_to_power)
            else:
                self.pacman.set(opposite_dir)
        elif status == PacManStatus.EATING:
            self.pacman.set(ucs(ProblemOdDo(self.game, pacman, ghosts_to_eat[0])).actions[0])
        return

            
        targets = active_pills + active_power_pills


        # print("ghosts : ", " , ".join(str(x) for x in ghost_locs))

        kam = active_power_pills[0] if active_power_pills else ghost_locs[0]

        mojproblem = ProblemOdDo(self.game, pacman, kam)
        sol = ucs(mojproblem)
        if sol is not None and sol.actions:
            # print(f"JO : {sol.actions[0]}")
            self.pacman.set(sol.actions[0])

        # # print(f"Chod takto : \n {ucs(mojproblem).actions}")

        # # print(f"eating_time {eating_time}")
        # # print(f"ghost_locs {ghost_locs}")
        # # print(f"ghost_dirs {ghost_dirs}")
        # # print(f"edible_times {edible_times}")




        # ghost_locs = self.game.ghost_locs()
        prob = PacProblem(game)
        sol = ucs(prob)
                
        if sol is None or not sol.actions:
            pass
            # if self.verbose:
            #     # print("No path found.", file=sys.stderr)
        else:
            self.pacman.set(sol.actions[0])
