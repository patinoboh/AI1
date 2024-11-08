import numpy as np

_deleno = 1.95
_max_v_pred_prekazkou = 5
_max_usek = 3
_krat_v_menej = 3
_const_v_menej = -6
_const_vo_viac = -4
_krat_vo_viac = 3
_speed_thresshold = 13
_max_minus = -2

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

for deleno in deleno_range:
    for max_v_pred_prekazkou in max_v_pred_prekazkou_range:
        for max_usek in max_usek_range:
            for krat_v_menej in krat_v_menej_range:
                for const_v_menej in const_v_menej_range:
                    for const_vo_viac in const_vo_viac_range:
                        for krat_vo_viac in krat_vo_viac_range:
                            for speed_thresshold in speed_thresshold_range:
                                for max_minus in max_minus_range:
                                    # print(f"deleno={deleno}")
                                    # print(f"max_v_pred_prekazkou={max_v_pred_prekazkou}")
                                    # print(f"max_usek={max_usek}")
                                    # print(f"krat_v_menej={krat_v_menej}")
                                    # print(f"const_v_menej={const_v_menej}")
                                    # print(f"const_vo_viac={const_vo_viac}")
                                    # print(f"krat_vo_viac={krat_vo_viac}")
                                    # print(f"speed_thresshold={speed_thresshold}")
                                    # print(f"max_minus={max_minus}")
                                    # print this large table as a csv file
                                    print(f"{deleno},{max_v_pred_prekazkou},{max_usek},{krat_v_menej},{const_v_menej},{const_vo_viac},{krat_vo_viac},{speed_thresshold},{max_minus}")


