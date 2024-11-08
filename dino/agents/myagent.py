#!/usr/bin/env python3
from game.dino import *
from game.agent import Agent


class MyAgent(Agent):
    """Reflex agent static class for Dino game."""

    @staticmethod
    def get_move(game: Game) -> DinoMove:
        """
        Note: Remember you are creating simple-reflex agent, that should not
        store or access any information except provided.
        """
        # # for visual debugging intellisense you can use
        # from game.debug_game import DebugGame
        # game: DebugGame = game
        # if not hasattr(MyAgent, "debug_txt"):
        #     _ = game.add_text(Coords(10, 10), "red", "Hello World.")
        #     MyAgent.debug_txt = game.add_text(Coords(10, 30), "red", "0")
        # else:
        #     MyAgent.debug_txt.text = str(game.score)
        # game.add_dino_rect(Coords(-10, -10), 150, 150, "yellow")
        # l = game.add_dino_line(Coords(0, 0), Coords(100, 0), "black")
        # l.dxdy.update(50, 30)
        # l.dxdy.x += 50
        # game.add_moving_line(Coords(1000, 100), Coords(1000, 500), "purple")

        # YOUR CODE GOES HERE

        return DinoMove.NO_MOVE

class MiddleAgent(Agent):
    
    @staticmethod
    def get_move(game: Game) -> DinoMove:
        print(f"POSITION x ; {game.dino.x} y : {game.dino.y}")
        
        print(f"BODY H,W w : {game.dino.body.width} h : {game.dino.body.height}")
        print(f"BODY POSITION : x : {game.dino.body.x} y : {game.dino.body.y}")
        
        print(f"HEAD H,W w : {game.dino.head.width} h : {game.dino.head.height}")
        print(f"HEAD POSITION : x : {game.dino.head.x} y : {game.dino.head.y}")

        print(f"game w : {game.WIDTH} h : {game.HEIGHT}")
        
        return DinoMove.NO_MOVE