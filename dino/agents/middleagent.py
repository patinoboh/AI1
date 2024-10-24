#!/usr/bin/env python3

from game.dino import *
from game.agent import Agent
from itertools import accumulate
from math import ceil, floor

class MiddleAgent(Agent):
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
            MiddleAgent.write_object(o)

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
            can_he &= MiddleAgent.overlapse2(game.dino.x - 20 - game.speed, game.dino.x + 77 - 20 - game.speed, o_x_next, o_x_next + o.type.width)
        # print(f"CAN REVERSE ?? {can_he} size {len(game.obstacles)}")
        return can_he


    @staticmethod
    def get_move(game: Game) -> DinoMove:
        # print()
        
        dino = game.dino
        # [390, 370, 351, 333, 316, 300, 285, 271, 258, 246, 235, 225, 216, 208, 201, 195, 190, 186, 183, 181, 180, 180]        
        obstacles = sorted(game.obstacles, key=lambda obs: obs.rect.x) # TODO sort by which one will be first when they'll get to me

        d_w = 77 # head + offset of the head
        d_h = 80 # body + offset of the head
        d_w_duck = 45 + 56
        d_h_duck = 32 + 13

        dino_ground_y = 310
        ground_level = 310 + d_h
        birds = [ObstacleType.BIRD1, ObstacleType.BIRD2, ObstacleType.BIRD3]
        can_sneak = [ObstacleType.BIRD1, ObstacleType.BIRD2]
        
        jumps = [0] + list(range(20,-1,-1)) # dino jumps 20,19,18,..,1,0
        jumps_prefixes = list(accumulate(jumps))

        falls = list(range(0,51)) # dino falls 0,1,2,..
        falls_prefixes = list(accumulate(falls))
        
        f_falls = list(range(0,60,2)) # while down, dino falls 0,2,4,..
        f_falls_prefixes = list(accumulate(f_falls))

        movements = [0] + list(range(0,51)) # dino moves 0,1,2,.. to the right, left is bigger by game.speed in each step
        movements_prefixes = list(accumulate(movements))

        
        for i,o in enumerate(obstacles):
            # if(o.rect.x + o.type.width < 80):
            #     # print(f"PASSING OBJECT {o.type}")
            #     continue


            if(o.rect.x + o.type.width + 1 < dino.x):
                # print(f"PASSING OBJECT {o.type}")
                continue

            # MiddleAgent.write_dino(game)
            MiddleAgent.write_object(o)


            next_o = obstacles[i + 1] if i + 1 < len(obstacles) else None
            next_next_o = obstacles[i + 2] if i + 2 < len(obstacles) else None
            
            o_moving_speed = game.speed + o.speed
            o_h = o.type.height
            o_x_next = o.rect.x - (o_moving_speed)
            d_x = dino.x
            d_y = dino.y
            o_x = o.rect.x
            o_y = o.rect.y
            o_w = o.type.width
            o_h = o.type.height
            R = DinoState.RUNNING
            J = DinoState.JUMPING
            D = DinoState.DUCKING
            

            crash = ceil((o.rect.x - (dino.x + d_w)) / o_moving_speed) # ok
            crash_next = 0 if not next_o else ceil((next_o.rect.x - (dino.x + d_w)) / (next_o.speed + game.speed)) # ok
            
            # movement to right underestimates and it cannot be fixed, because there is no way to know whether we moved right before
            # the movement gradually increases so the only right estimate is the one made at the start of the movement, that in underestimates
            # or oversetimates, depending on the implementation           
            
            right_crash_prefixes = list(accumulate(list(map(lambda x: x + o_moving_speed, movements[1:]))))
            nextspeed = 0 if not next_o else next_o.speed + game.speed
            right_crash_prefixes_next = list(accumulate(list(map(lambda x: x + nextspeed, movements[1:]))))
            
            crash_right = next(i for i,x in enumerate(right_crash_prefixes) if x > o.rect.x - (dino.x + d_w_duck)) + 2 # unerestimates
            crash_right_next = 0 if not next_o else next(i for i,x in enumerate(right_crash_prefixes) if x > next_o.rect.x - (dino.x + d_w_duck)) + 2 # underestimates
            
            # get_behind_right_next = 0 if not next_o else next(i for i,x in enumerate(right_crash_prefixes) if x > next_o.rect.x + next_o.type.width - d_x) + 1

            get_behind_right = next(i for i,x in enumerate(right_crash_prefixes) if x > o_x + o_w - d_x) + 1
            get_behind_right_next = 0 if not next_o else next(i for i,x in enumerate(right_crash_prefixes_next) if x > next_o.rect.x + next_o.type.width - d_x) + 1

            speed_glide = next(i for i,x in enumerate(movements_prefixes) if x > o_x + o_w - d_x)
            
            # jump_over = next(i for i,x in enumerate(jumps_prefixes) if x > d_y + d_h - o_y)
            jump_over = next(i for i,x in enumerate(jumps_prefixes) if x > dino_ground_y + d_h - o_y) - 1
            jump_over_next = 0 if not next_o else next(i for i,x in enumerate(jumps_prefixes) if x > dino_ground_y + d_h - next_o.rect.y) - 1
            
            fall = next(i for i,x in enumerate(falls_prefixes) if x > dino_ground_y - d_y)
            
            fast_fall = next(i for i,x in enumerate(f_falls_prefixes) if x > dino_ground_y - d_y)

            drop_on = next(i for i,x in enumerate(jumps_prefixes[1:]) if x > o_y - d_y - d_h)

            fast_fall_on = next(i for i,x in enumerate(f_falls_prefixes) if x > o_y - d_y - d_h)
            fast_fall_on_next = 0 if not next_o else next(i for i,x in enumerate(f_falls_prefixes) if x > next_o.rect.y - d_y - d_h)

            fast_fall_under = next(i for i,x in enumerate(f_falls_prefixes) if x > o_y + o_h - d_y)
            fast_fall_under_next = 0 if not next_o else next(i for i,x in enumerate(f_falls_prefixes) if x > next_o.rect.y + next_o.type.height - d_y) + 1

            balance_move = DinoMove.RIGHT if jump_over < crash_right and d_x < WIDTH / 4 else (DinoMove.LEFT if MiddleAgent.can_reverse(game) else DinoMove.NO_MOVE)
            down_balance = DinoMove.DOWN_RIGHT if balance_move == DinoMove.RIGHT else (DinoMove.DOWN_LEFT if balance_move == DinoMove.LEFT else DinoMove.DOWN)

            # print(f"GS {game.speed}, OVER {jump_over}, FFALL {fast_fall}, FALL {fall}, FFON {fast_fall_on}, DROP_ON {drop_on}, CRASH {crash}, C_RIGHT {crash_right}, BEHIND_R {get_behind_right}")

            if dino.state != J and o.type in can_sneak and (not next_o or (next_o.type in can_sneak or next_o.rect.x - o_x + o_w > 150)):
                # print("SNEAKING")
                return DinoMove.DOWN
            
            elif dino.state != J and jump_over in range(crash, crash + 4):
                # print("UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUP")
                return DinoMove.UP
            
            elif dino.state != J:
                return balance_move

            elif dino.state == J and MiddleAgent.overlapse(dino, o) and fast_fall_on > get_behind_right:
                
                # ticks_right = undefined
                # ticks_normal = undefined
                start = o_x - d_w
                end = o_x + o_w + d_w
                l = end - start
                k2 = 3
                k1 = 0 if not next_o else k2 - (l - abs(d_x - start )) / l * k2 # predtym *5* alebo 6
                k1 = ceil(k1 * 3) - 6 if game.speed < 13 else ceil(k1 * 3) - 4
                # print(f"TESNE TESNE {k1}")

                if not next_o:
                    # print("NIKTO DALSI, IDEM DOLE")
                    return DinoMove.DOWN_RIGHT
                elif next_o.type in can_sneak and fast_fall_under_next < crash_next + k1:
                    # print(f"DALSIEHO STIHNEM PODLIEZT")
                    return DinoMove.DOWN_RIGHT

                elif fast_fall + jump_over_next < crash_next + k1:
                    # print(f"STIHAM DOLE HORE")
                    return DinoMove.DOWN_RIGHT
                else:
                    # print("NESTIHAM IST DOLE")
                    if(d_y + d_h < next_o.rect.y):
                        # print("ALE SOM NAD NIM, TAK HO SEKNEM")
                        return DinoMove.RIGHT
                    else:
                        # print("NESTIHAM IST DOLE A SOM POD NIM, TAK IDEM DOLAVA HORE / teda len hore")
                        return DinoMove.UP_LEFT
            
            elif dino.state == J and MiddleAgent.overlapse(dino, o) and fast_fall_on <= get_behind_right:
                # print("NAD ALE NESTIHA")
                return DinoMove.RIGHT
            
            # elif dino.state == J and d_x > o_x + o_w:
            #     # print("ZA PREKAZKOU")
            #     return DinoMove.DOWN
            
            elif dino.state == J:

                k = o_x - d_x - d_h
                k = min(game.speed / 2.5, 5)
                # print(f"PRED PREKAZKOU {k}")

                if o.type in can_sneak and fast_fall_under < crash + k:
                    # print("DALSIEHO STIHNEM PODLIEZT ROVNO TU")
                    return DinoMove.DOWN


                if(jump_over > crash):
                    if(d_y + d_h < o_y):
                        # print("SOM PRED ALE NAD TAK IDEM DOPRAVA")
                        return DinoMove.RIGHT
                    # print("PRED PRED = UP")
                    return DinoMove.UP
                
                if o.type in can_sneak and fast_fall_under < crash + k:
                    # print("DALSIEHO STIHNEM PODLIEZT")
                    if(MiddleAgent.can_reverse(game)):
                        # print("MOZEM REVERSE")
                        return DinoMove.DOWN_LEFT
                    return DinoMove.DOWN
                elif fast_fall + jump_over < crash + k:
                    # print("STIHAM DOLE HORE")
                    if(MiddleAgent.can_reverse(game)):
                        # print("MOZEM REVERSE")
                        return DinoMove.DOWN_LEFT
                    return DinoMove.DOWN
                else:
                    # print("NESTIHAM IST DOLE")
                    if(d_y + d_h < o_y):
                        # print("NESTIHAM IST DOLE ALE SOM NAD NIM TAK HO SEKNEM")
                        return DinoMove.RIGHT
                    else:
                        # print("NESTIHAM IST DOLE A SOM POD NIM TAK IDEM HORE DOLAVA")
                        return DinoMove.UP_LEFT
                        
            elif dino.state == J:
                # print("JUMPING RIGHT")
                return DinoMove.DOWN
            
            # print("OTHERWISE")
            return DinoMove.NO_MOVE



        # print("NEVRACIAM NIC")
        return DinoMove.NO_MOVE
        # return down_move