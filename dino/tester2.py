import os
import numpy as np

# with open("/home/patrik/Documents/ai1/AI1/dino/params.csv", "r") as file:
#     lines = file.readlines()
#     i = 0
#     for line in lines:
#         splitted = line.split(",")
#         deleno = float(splitted[0])
#         max_v_pred_prekazkou = float(splitted[1])
#         max_usek = float(splitted[2])
#         krat_v_menej = float(splitted[3])
#         const_v_menej = float(splitted[4])
#         const_vo_viac = float(splitted[5])
#         krat_vo_viac = float(splitted[6])
#         speed_thresshold = float(splitted[7])
#         max_minus = float(splitted[8])

#         with open("/home/patrik/Documents/ai1/AI1/dino/params.txt", "w") as file2:
#             # at first make sure that the file is empty
#             file2.write(f"deleno={deleno}\n")
#             file2.write(f"max_v_pred_prekazkou={max_v_pred_prekazkou}\n")
#             file2.write(f"max_usek={max_usek}\n")
#             file2.write(f"krat_v_menej={krat_v_menej}\n")
#             file2.write(f"const_v_menej={const_v_menej}\n")
#             file2.write(f"const_vo_viac={const_vo_viac}\n")
#             file2.write(f"krat_vo_viac={krat_vo_viac}\n")
#             file2.write(f"speed_thresshold={speed_thresshold}\n")
#             file2.write(f"max_minus={max_minus}\n")
#         # execute bash script
#         os.system(f"./play_dino -a MiddleAgent -s 200 >> \"/home/patrik/Documents/ai1/AI1/dino/results.csv\"")
#         i += 1
#         print(f"Done {i} out of {len(lines)}")
        

deleno_range = [float(x) for x in np.arange(1.9,3.3,0.2)]
max_v_pred_prekazkou_range = range(2, 6, 1)
max_usek_range = range(1, 4, 1)
krat_v_menej_range = [float(x) for x in np.arange(2,4,0.2)]
const_v_menej_range = range(-6, 0, 1)
const_vo_viac_range = range(-6, 0, 1)
krat_vo_viac_range = [float(x) for x in np.arange(2,4,0.2)]
speed_thresshold_range = [float(x) for x in np.arange(8.4, 13, 0.3)]
max_minus_range = range(-3, 0, 1)

# print(len(deleno_range) * len(max_v_pred_prekazkou_range) * len(max_usek_range) * len(krat_v_menej_range) * len(const_v_menej_range) * len(const_vo_viac_range) * len(krat_vo_viac_range) * len(speed_thresshold_range) * len(max_minus_range))

# deleno = 0.1
# max_v_pred_prekazkou = 0.1
# max_usek = 0.1
# krat_v_menej = 0.1
# const_v_menej = 0.1
# const_vo_viac = 0.1
# krat_vo_viac = 0.1
# speed_thresshold = 0.1
# max_minus = 0.1


count = len(deleno_range) * len(max_v_pred_prekazkou_range) * len(max_usek_range) * len(krat_v_menej_range) * len(const_v_menej_range) * len(const_vo_viac_range) * len(krat_vo_viac_range) * len(speed_thresshold_range) * len(max_minus_range)
i = 1
for deleno in deleno_range:
    for max_v_pred_prekazkou in max_v_pred_prekazkou_range:
        for max_usek in max_usek_range:
            for krat_v_menej in krat_v_menej_range:
                for const_v_menej in const_v_menej_range:
                    for const_vo_viac in const_vo_viac_range:
                        for krat_vo_viac in krat_vo_viac_range:
                            for speed_thresshold in speed_thresshold_range:
                                for max_minus in max_minus_range:
                                    with open("/home/patrik/Documents/ai1/AI1/dino/params.txt", "w") as file2:
                                        # at first make sure that the file is empty
                                        file2.write(f"deleno={deleno}\n")
                                        file2.write(f"max_v_pred_prekazkou={max_v_pred_prekazkou}\n")
                                        file2.write(f"max_usek={max_usek}\n")
                                        file2.write(f"krat_v_menej={krat_v_menej}\n")
                                        file2.write(f"const_v_menej={const_v_menej}\n")
                                        file2.write(f"const_vo_viac={const_vo_viac}\n")
                                        file2.write(f"krat_vo_viac={krat_vo_viac}\n")
                                        file2.write(f"speed_thresshold={speed_thresshold}\n")
                                        file2.write(f"max_minus={max_minus}\n")
                                    # execute bash script                                    
                                    os.system(f"echo -n {deleno}, {max_v_pred_prekazkou}, {max_usek}, {krat_v_menej}, {const_v_menej}, {const_vo_viac}, {krat_vo_viac}, {speed_thresshold}, {max_minus},  >> \"/home/patrik/Documents/ai1/AI1/dino/vysledky2.csv\"")
                                    os.system(f"./play_dino.py -a MiddleAgent -s 100 >> \"/home/patrik/Documents/ai1/AI1/dino/vysledky2.csv\"")
                                    print(f"Done {i} out of {count} => {round(i / count * 100,3)} %")
                                    i += 1

            
        
            
            



    #     def read_params(path):
    # global g_deleno, g_max_v_pred_prekazkou, g_max_usek, g_krat_v_menej, g_const_v_menej, g_const_vo_viac, g_krat_vo_viac, g_speed_thresshold, g_max_minus
    # with open(path, "r") as file:
    #     lines = file.readlines()
    #     for line in lines:
    #         key, value = line.split("=")
    #         if key == "deleno":
    #             g_deleno = float(value)
    #         elif key == "max_v_pred_prekazkou":
    #             g_max_v_pred_prekazkou = float(value)
    #         elif key == "max_usek":
    #             g_max_usek = float(value)
    #         elif key == "krat_v_menej":
    #             g_krat_v_menej = float(value)
    #         elif key == "const_v_menej":
    #             g_const_v_menej = float(value)
    #         elif key == "const_vo_viac":
    #             g_const_vo_viac = float(value)
    #         elif key == "krat_vo_viac":
    #             g_krat_vo_viac = float(value)
    #         elif key == "speed_thresshold":
    #             g_speed_thresshold = float(value)
    #         elif key == "max_minus":
    #             g_max_minus = float(value)