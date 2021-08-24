import numpy as np
import cv2


def unique_counts(channel_img):
    ele, count_ele = np.unique(channel_img, return_counts=True)
    return list(ele), list(count_ele)


def identifying_right_value(value, counts):
    v = value
    c = counts
    for ind, ele in enumerate(v):
        if ele == 0 or ele < 7:
            del v[ind]
            del c[ind]
    return v, c


def ratio_cal(val, cnt):
    dic = {}
    lst = []
    total_cnt = sum(cnt)
    for ind,e in enumerate(val):
        dic.update({e:cnt[ind]/total_cnt})
        lst.append(cnt[ind]/total_cnt)
    return dic, lst


def decision_cal(val, ratio_lst):
    min_ = min(ratio_lst)
    max_ = max(ratio_lst)

    if min_ > 0.15 * max_:
        return True
    else:
        return False


def decision(img):
    b = img[:, :, 0]
    g = img[:, :, 1]
    r = img[:, :, 2]

    ele, count_ele = unique_counts(b)
    val, cnt = identifying_right_value(ele, count_ele)
    ratio_dict, ratio_lst = ratio_cal(val=val, cnt=cnt)
    print(ratio_dict)
    decision_ = decision_cal(val, ratio_lst)
    return decision_



