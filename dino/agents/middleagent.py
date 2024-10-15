#!/usr/bin/env python3

from game.dino import *
from game.agent import Agent
from itertools import accumulate
from math import ceil, floor

class MiddleAgent(Agent):
    def print_object(o, name=None):
        name = name if name else o.type
        print(f"{name} (x,y)=({o.rect.x},{o.rect.y}) (w,h)=({o.rect.width},{o.rect.height}) speed={o.speed}")
        
    
    def print_dino(game):
        dino = game.dino
        print(f"POSIITON    DINO ({dino.x},{dino.y})    BODY ({dino.body.x},{dino.body.y})    HEAD ({dino.head.x},{dino.head.y})")
        print(f"HW    BODY ({dino.body.height},{dino.body.width})    HEAD ({dino.head.height},{dino.head.width})    GAME ({HEIGHT},{WIDTH})")
        print(f"state {dino.state}")

    def print_obstacles(game):
        obstacles = sorted(game.obstacles, key=lambda obs: obs.rect.x)

        print(f"obstacles count : {len(obstacles)}")
        print(f"game speed : {game.speed}")
        print(f"dino (x,y)=({game.dino.x},{game.dino.y})")
        for i,o in enumerate(obstacles):
            MiddleAgent.print_object(o)

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
        return MiddleAgent.overlapse2(d_l, d_r, o_l, o_r)

    def can_reverse(game: Game):
        can_he = True
        for o in game.obstacles:
            o_moving_speed = game.speed + o.speed
            o_x_next = o.rect.x - (o_moving_speed)
            can_he &= MiddleAgent.overlapse2(game.dino.x - 20, game.dino.x + 77 - 20, o_x_next, o_x_next + o.type.width)
        print(f"CAN REVERSE ?? {can_he} size {len(game.obstacles)}")
        return can_he


    @staticmethod
    def get_move(game: Game) -> DinoMove:
        print()
        
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
        can_sneak = [ObstacleType.BIRD1, ObstacleType.BIRD2]
        jumps = [0] + list(range(20,-1,-1)) # dino jumps 20,19,18,..,1,0 then falls 1,2,3,..,20
        falls = [0] + list(range(4,41,2)) + [40] * 3
        prefixes = [ground_level - x for x in list(accumulate(jumps))] + [0]
        falls_prefixes = list(accumulate(falls))

        
        for o in obstacles:
            if(o.rect.x + o.type.width < dino.x):
                print(f"PASSING OBJECT {o.type}")

                continue

            MiddleAgent.print_dino(game)
            MiddleAgent.print_object(o)
            
            o_moving_speed = game.speed + o.speed
            o_h = o.type.height            
            o_x_next = o.rect.x - (o_moving_speed)

            down_move = DinoMove.DOWN_LEFT if dino.x > WIDTH / 5 else DinoMove.DOWN_RIGHT
            move_move = DinoMove.LEFT if dino.x > WIDTH / 5 and MiddleAgent.can_reverse(game) else (DinoMove.RIGHT if not MiddleAgent.overlapse2(dino.x + 20, dino.x + d_w_duck + 20, o_x_next, o_x_next + o.type.width) else DinoMove.NO_MOVE)


            ticks_to_collision = ceil((o.rect.x - (dino.x + d_w)) / o_moving_speed) + 1
            
            # movement to right underestimates and it cannot be fixed, because there is no way to know whether we moved right before
            ticks_to_collision_while_right = ceil((o.rect.x - (dino.x + d_w_duck)) / (o_moving_speed + game.speed)) + 2 # not correct
            ticks_to_glide_over = ceil((o.rect.x + o.type.width - (dino.x + d_w)) / (o_moving_speed + game.speed)) + 2 # not correct, underestimates

            ticks_to_get_over = next(i for i,x in enumerate(prefixes) if x < o.rect.y)                        
            ticks_to_fall = abs(next(i for i,x in enumerate(prefixes) if x < dino.y + d_h) - ticks_to_get_over) + 2
            to_drop = (o.rect.y + o.type.height) - (dino.y - 21) if dino.y <= o.rect.x else 0
            ticks_to_fast_fall = next(i for i,x in enumerate(falls_prefixes) if x > dino_ground_y - (dino.y - 20))
            distance_made_by_fall = game.speed * (ticks_to_fast_fall + 1)


            print(f"GS : {game.speed} FALL : {ticks_to_fast_fall} COLIS : {ticks_to_collision} OVER : {ticks_to_get_over} RIGHT : {ticks_to_collision_while_right}")

            if dino.state != DinoState.JUMPING and o.type in can_sneak:
                down_move = down_move if down_move == DinoMove.DOWN_LEFT and MiddleAgent.can_reverse(game) else (down_move if down_move == DinoMove.DOWN_RIGHT else DinoMove.DOWN)
                print(f"PODLIEZAM : {down_move}")
                return down_move
            
            elif dino.state == DinoState.DUCKING and not MiddleAgent.overlapse(dino, o):
                print("NACO SA KRCI?")
                return move_move

            elif dino.state != DinoState.JUMPING and ticks_to_collision == ticks_to_get_over + 1:
                print("SKAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEMMMMMMMMMMMMMMM")
                return DinoMove.UP
                        
            elif dino.state == DinoState.JUMPING and MiddleAgent.overlapse(dino, o):
                print("OVERLAPS")
                return DinoMove.RIGHT
            
            elif dino.state == DinoState.JUMPING and ticks_to_fast_fall + ticks_to_get_over < ticks_to_collision - 2:
                print("STIHAM IST DOLE")
                return DinoMove.DOWN

            elif dino.state == DinoState.JUMPING and (ticks_to_fall >= ticks_to_glide_over):
                print("STIHAM")
                return DinoMove.RIGHT

            elif dino.state == DinoState.JUMPING and (0 <= ticks_to_collision <= ticks_to_get_over + 1):
                print("RIGHT VO VZDUCHU - NO MOVE/UP")
                return DinoMove.UP
            
            elif dino.state == DinoState.JUMPING and MiddleAgent.can_reverse(game):
                print("LEFT")
                return DinoMove.DOWN_LEFT
            
            elif dino.state == DinoState.JUMPING and ticks_to_get_over > ticks_to_collision:
                print("SKUS UP_LEFT")
                return DinoMove.UP_LEFT
            
            elif dino.state == DinoState.JUMPING and ticks_to_fast_fall + ticks_to_get_over < ticks_to_collision:
                print("JUST DOWN")
                return DinoMove.DOWN
            
            elif dino.state != DinoState.JUMPING and MiddleAgent.can_reverse(game):
                print("MOZE IST DOLAVA")
                return DinoMove.NO_MOVE
                # return move_move
            
            elif dino.state != DinoState.DUCKING:
                print("move move")
                return DinoMove.NO_MOVE
                # return move_move
            
            else:
                print(f"ELSE?? {10}")
                return DinoMove.NO_MOVE




        print("NEVRACIAM NIC")
        return DinoMove.NO_MOVE
        # return down_move