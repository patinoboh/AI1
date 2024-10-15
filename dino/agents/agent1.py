#!/usr/bin/env python3

from game.dino import *
from game.agent import Agent
from itertools import accumulate
from math import ceil, floor

class Agent1(Agent):
    def write_object(o, name=None):
        name = name if name else o.type
        # print(f"{name} (x,y)=({o.rect.x},{o.rect.y}) (w,h)=({o.rect.width},{o.rect.height}) speed={o.speed}")
        
    
    def write_dino(game):
        dino = game.dino
        # print(f"POSIITON    DINO ({dino.x},{dino.y})    BODY ({dino.body.x},{dino.body.y})    HEAD ({dino.head.x},{dino.head.y})")
        # print(f"HW    BODY ({dino.body.height},{dino.body.width})    HEAD ({dino.head.height},{dino.head.width})    GAME ({HEIGHT},{WIDTH})")
        # print(f"state {dino.state}")

    def write_obstacles(game):
        obstacles = sorted(game.obstacles, key=lambda obs: obs.rect.x)

        # print(f"obstacles count : {len(obstacles)}")
        # print(f"game speed : {game.speed}")
        # print(f"dino (x,y)=({game.dino.x},{game.dino.y})")
        for i,o in enumerate(obstacles):
            Agent1.write_object(o)

    def overlapse2(d_l, d_r, o_l, o_r):
        #    ____    DINO
        #      ____  OBJ
        #  ____      OBJ
        #  ________  OBJ
        return (d_l <= o_l <= d_r) or (d_l <= o_r <= d_r) or (o_l <= d_l <= o_r)


    def overlapse(dino, o):
        d_l = dino.x                  # dino left
        d_r = dino.x + 77             # dino right
        o_l = o.rect.x                # object left
        o_r = o.rect.x + o.type.width # object right
        return Agent1.overlapse2(d_l, d_r, o_l, o_r)

    def can_reverse(game: Game):
        can_he = True
        for o in game.obstacles:
            o_moving_speed = game.speed + o.speed
            o_x_next = o.rect.x - (o_moving_speed)
            can_he &= Agent1.overlapse2(game.dino.x - 20, game.dino.x + 77 - 20, o_x_next, o_x_next + o.type.width)
        return can_he


    @staticmethod
    def get_move(game: Game) -> DinoMove:
        # print()
        
        dino = game.dino
        # [390, 370, 351, 333, 316, 300, 285, 271, 258, 246, 235, 225, 216, 208, 201, 195, 190, 186, 183, 181, 180, 180]        
        obstacles = sorted(game.obstacles, key=lambda obs: obs.rect.x) # TODO sort by which one will be first when they'll get to me

        d_w = 77 # head + offset of the head
        d_h = 80 # body + offset of the head
        d_w_duck = 101
        # d_h_duck = 
        dino_ground_y = 310
        ground_level = 310 + d_h
        birds = [ObstacleType.BIRD1, ObstacleType.BIRD2, ObstacleType.BIRD3]
        jumps = [0] + list(range(20,-1,-1)) # dino jumps 20,19,18,..,1,0 then falls 1,2,3,..,20
        falls = [0] + list(range(4,41,2)) + [40] * 3
        prefixes = [ground_level - x for x in list(accumulate(jumps))] + [0]
        falls_prefixes = list(accumulate(falls))

        down_move = DinoMove.DOWN_LEFT if dino.x > WIDTH / 5 else DinoMove.DOWN_RIGHT

        for o in obstacles:
            if(o.rect.x + o.type.width < dino.x):
                # print(f"PASSING OBJECT {o.type}")

                continue

            Agent1.write_dino(game)
            Agent1.write_object(o)
            
            o_moving_speed = game.speed + o.speed
            o_h = o.type.height            
            o_x_next = o.rect.x - (o_moving_speed)

            ticks_to_collision = ceil((o.rect.x - (dino.x + d_w)) / o_moving_speed) + 2
            
            ticks_to_collision_while_right = ceil((o.rect.x - (dino.x + d_w_duck)) / (o_moving_speed + game.speed)) + 2

            ticks_to_glide_over = ceil((o.rect.x + o.type.width - (dino.x + d_w)) / (o_moving_speed + game.speed)) + 2
            ticks_to_get_over = next(i for i,x in enumerate(prefixes) if x < o.rect.y)                        
            ticks_to_fall = abs(next(i for i,x in enumerate(prefixes) if x < dino.y + d_h) - ticks_to_get_over) + 2
            to_drop = (o.rect.y + o.type.height) - (dino.y - 21) if dino.y <= o.rect.x else 0
            ticks_to_fast_fall = next(i for i,x in enumerate(falls_prefixes) if x > dino_ground_y - (dino.y - 20))
            distance_made_by_fall = game.speed * (ticks_to_fast_fall + 1)


            # print(f"GS : {game.speed} FALL : {ticks_to_fast_fall} COLIS : {ticks_to_collision} OVER : {ticks_to_get_over} RIGHT : {ticks_to_collision_while_right}")

            if dino.state != DinoState.JUMPING and ticks_to_collision_while_right == ticks_to_get_over:
                # print("SKAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEMMMMMMMMMMMMMMM")
                return DinoMove.UP_RIGHT
            
            elif dino.state == DinoState.JUMPING and Agent1.overlapse(dino, o):
                # print("OVERLAPS")
                return DinoMove.RIGHT
            
            # elif dino.state == DinoState.JUMPING and ticks_to_fast_fall + ticks_to_get_over < ticks_to_collision - 2:
            #     # print("STIHAM IST DOLE")
            #     return DinoMove.DOWN
                                                            
            elif dino.state == DinoState.JUMPING and (0 <= ticks_to_collision_while_right <= ticks_to_get_over):
                # print("RIGHT VO VZDUCHU")
                return DinoMove.RIGHT
            
            elif dino.state == DinoState.JUMPING and (ticks_to_fall >= ticks_to_glide_over):
                # print("STIHAM")
                return DinoMove.RIGHT
            
            elif dino.state == DinoState.JUMPING and Agent1.can_reverse(game):
                # print("LEFT")
                return DinoMove.DOWN_LEFT
            
            elif dino.state == DinoState.JUMPING:
                # print("JUST DOWN")
                return DinoMove.DOWN
            elif dino.state == DinoState.RUNNING and Agent1.can_reverse(game):
                # print("TERAZ DOLAVA")
                return DinoMove.LEFT
            elif dino.state == DinoState.RUNNING:
                # print("no move")
                return DinoMove.NO_MOVE
            

            # if o.type in birds:
            #     # print(f"bird : {o.type}")
            # else:
            #     # print(f"cactus : {o.type}")

        # if dino.state == DinoState.RUNNING:
        #     pass
        # elif dino.state == DinoState.DUCKING:
        #     pass
        
        # Agent1.write_obstacles(game)
        # print(f"DOWNMOVE={down_move}")

        return DinoMove.NO_MOVE
        # return down_move