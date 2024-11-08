#!/usr/bin/env python3

from game.dino import *
from game.agent import Agent
from itertools import accumulate
from math import ceil, floor

# parser.add_argument("--deleno", default=1.95, type=float, help="Deleno.")
# parser.add_argument("--max_v_pred_prekazkou", default=5, type=float, help="Max v pred prekazkou.")
# parser.add_argument("--max_usek", default=3, type=float, help="Max usek.")
# parser.add_argument("--krat_v_menej", default=3, type=float, help="Krat v menej.")
# parser.add_argument("--const_v_menej", default=-6, type=float, help="Const v menej.")
# parser.add_argument("--const_vo_viac", default=-4, type=float, help="Const vo viac.")
# parser.add_argument("--krat_vo_viac", default=3, type=float, help="Krat vo viac.")
# parser.add_argument("--speed_thresshold", default=13, type=float, help="Speed thresshold.")
# parser.add_argument("--max_minus", default=-2, type=float, help="Max minus.")

g_deleno = 1.95
g_max_v_pred_prekazkou = 5
g_max_usek = 3
g_krat_v_menej = 3
g_const_v_menej = -6
g_const_vo_viac = -4
g_krat_vo_viac = 3
g_speed_thresshold = 13
g_max_minus = -2


def set_params(deleno, max_v_pred_prekazkou, max_usek, krat_v_menej, const_v_menej, const_vo_viac, krat_vo_viac, speed_thresshold, max_minus):
    global g_deleno, g_max_v_pred_prekazkou, g_max_usek, g_krat_v_menej, g_const_v_menej, g_const_vo_viac, g_krat_vo_viac, g_speed_thresshold, g_max_minus
    g_deleno = deleno
    g_max_v_pred_prekazkou = max_v_pred_prekazkou
    g_max_usek = max_usek
    g_krat_v_menej = krat_v_menej
    g_const_v_menej = const_v_menej
    g_const_vo_viac = const_vo_viac
    g_krat_vo_viac = krat_vo_viac
    g_speed_thresshold = speed_thresshold
    g_max_minus = max_minus

def print_params():
    global g_deleno, g_max_v_pred_prekazkou, g_max_usek, g_krat_v_menej, g_const_v_menej, g_const_vo_viac, g_krat_vo_viac, g_speed_thresshold, g_max_minus
    print("PRINTING PARAMS FROM PYTHON MIDDLE AGENT")
    print(f"deleno={g_deleno}")
    print(f"max_v_pred_prekazkou={g_max_v_pred_prekazkou}")
    print(f"max_usek={g_max_usek}")
    print(f"krat_v_menej={g_krat_v_menej}")
    print(f"const_v_menej={g_const_v_menej}")
    print(f"const_vo_viac={g_const_vo_viac}")
    print(f"krat_vo_viac={g_krat_vo_viac}")
    print(f"speed_thresshold={g_speed_thresshold}")
    print(f"max_minus={g_max_minus}")

# 1.9, 2, 1, 2.0, -6, -5, 2.8000000000000007, 8.700000000000001, -3,3413.37

def read_params(path):
    global g_deleno, g_max_v_pred_prekazkou, g_max_usek, g_krat_v_menej, g_const_v_menej, g_const_vo_viac, g_krat_vo_viac, g_speed_thresshold, g_max_minus
    with open(path, "r") as file:
        lines = file.readlines()
        for line in lines:
            key, value = line.split("=")
            if key == "deleno":
                g_deleno = float(value)
            elif key == "max_v_pred_prekazkou":
                g_max_v_pred_prekazkou = float(value)
            elif key == "max_usek":
                g_max_usek = float(value)
            elif key == "krat_v_menej":
                g_krat_v_menej = float(value)
            elif key == "const_v_menej":
                g_const_v_menej = float(value)
            elif key == "const_vo_viac":
                g_const_vo_viac = float(value)
            elif key == "krat_vo_viac":
                g_krat_vo_viac = float(value)
            elif key == "speed_thresshold":
                g_speed_thresshold = float(value)
            elif key == "max_minus":
                g_max_minus = float(value)
    # print_params()




class MiddleAgent(Agent):
    def __init__(self):
        print("INIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIT")
        # read_params("/home/patrik/Documents/ai1/AI1/dino/params.txt")

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
        global g_deleno, g_max_v_pred_prekazkou, g_max_usek, g_krat_v_menej, g_const_v_menej, g_const_vo_viac, g_krat_vo_viac, g_speed_thresshold, g_max_minus
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
                MiddleAgent.write_dino(game)
                return DinoMove.UP
            
            elif dino.state != J:
                # print("VRACIAM BALANCE MOVE?")
                MiddleAgent.write_dino(game)

                return balance_move

            elif dino.state == J and MiddleAgent.overlapse(dino, o) and fast_fall_on > get_behind_right:
                
                # ticks_right = undefined
                # ticks_normal = undefined
                start = o_x - d_w
                end = o_x + o_w + d_w
                l = end - start
                
                max_usek = g_max_usek
                krat_v_menej = g_krat_v_menej
                const_v_menej = g_const_v_menej
                const_vo_viac = g_const_vo_viac
                krat_vo_viac = g_krat_vo_viac
                speed_thresshold = g_speed_thresshold
                max_minus = g_max_minus

                konstanta = 0 if not next_o else max_usek - (l - abs(d_x - start )) / l * max_usek # predtym *5* alebo 6
                konstanta = ceil(konstanta * krat_v_menej) + const_v_menej if game.speed < 13 else ceil(konstanta * krat_vo_viac) + const_vo_viac
                konstanta = max(max_minus, konstanta) if game.speed < 13 else konstanta
                # print(f"TESNE TESNE {konstanta}")

                if not next_o:
                    # print("NIKTO DALSI, IDEM DOLE")
                    return DinoMove.DOWN_RIGHT
                elif next_o.type in can_sneak and fast_fall_under_next < crash_next + konstanta:
                    # print(f"DALSIEHO STIHNEM PODLIEZT")
                    return DinoMove.DOWN_RIGHT

                elif fast_fall + jump_over_next < crash_next + konstanta:
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
                
                deleno = g_deleno
                max_v_pred_prekazkou = g_max_v_pred_prekazkou

                k = min(game.speed / deleno, max_v_pred_prekazkou)

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


if __name__ != "__main__":    
    read_params("/home/patrik/Documents/ai1/AI1/dino/params.txt")
