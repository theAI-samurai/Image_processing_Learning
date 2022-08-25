import cv2
import gc
import numpy as np
import pandas as pd
gc.collect()


def img_crop_table(img, tabl_lst):
    '''
    img         : Page Image without any croppings
    tabl_lst    : coordinates of table in format [x0,y0,x1,y1]
    '''
    return img[tabl_lst[1]:tabl_lst[3], tabl_lst[0]:tabl_lst[2]]


def img_mask_horizontal_vertical(src_img):
    '''
    img : this is cropped table area from orignal image
    '''
    kernel_horiz = np.ones((1, 2), np.uint8)
    kernel_vert = np.ones((2, 1), np.uint8)
    img_erode_horizontal = cv2.erode(src_img, kernel_horiz, iterations=15)
    img_erode_vertical = cv2.erode(img_erode_horizontal, kernel_vert, iterations=10)
    return img_erode_vertical


def get_col_index(img, tabl_lst):
    '''
    img         : this img is a Masked image
    tabl_lst    : coordinates of table in format [x0,y0,x1,y1],
    ids_orignal :
    '''
    ids_mask = {}
    ids_orignal = {}
    x0, y0, x1, y1 = tabl_lst
    for c in range(img.shape[1]):
        if np.all(img[:, c] == 1):      # ignoring column_index where all pixels are white
            pass
        else:
            white_pixel_percent = np.sum(img[:, c]) / len(img)
            if white_pixel_percent > 0.7:
                ids_mask.update({c: white_pixel_percent})
                ids_orignal.update({c+x0: white_pixel_percent})
    return ids_orignal, list(ids_orignal.keys())


def column_genration(src_img, tabl_lst):
    '''
    img         : this img is a Masked image
    tabl_lst    : coordinates of table in format [x0,y0,x1,y1],
    ids_orignal :
    '''
    _, index_lst = get_col_index(src_img, tabl_lst)
    index_strt_end = {}
    stflag = True

    # ------------------ creating start and end points for column gaps identified ----------------
    for i in range(1, len(index_lst)):
        if stflag is True:
            st = index_lst[i - 1]
            stflag = False
        else:
            if i != len(index_lst)-1:
                if (index_lst[i] - index_lst[i - 1]) < 5:
                    pass
                else:
                    en = index_lst[i - 1]
                    index_strt_end.update({st: (en, en - st)})
                    stflag = True
            else:
                en = index_lst[i]
                index_strt_end.update({st: (en, en - st)})
                stflag = True

    # ---------------- creating column width using identified index of gaps above ----
    # NOTE : column index here denote x values of start and end of column
    # y values will be the start and end of Table height -----------------------------

    col_lst = []
    df_col = pd.DataFrame(columns=['x', 'y', 'w', 'h', 'x2', 'y2'])
    prev_ind = None
    for id in index_strt_end.keys():
        st = id
        en = index_strt_end[id][0]
        if prev_ind is None:
            prev_ind = en - 5
        else:
            col_lst.append((prev_ind, st + 5))
            prev_ind = en - 5
    return col_lst


file = r'D:\ForageAI\tables_project\table_cell\backup\740749/4.jpeg'        #[83, 670, 2839, 3021]
file = r'D:\ForageAI\tables_project\table_cell\pdf_to_excel_output_\202013928\522.jpeg'     #[43, 593, 2740, 3674]
file = r'D:\ForageAI\tables_project\table_cell\pdf_to_excel_output_\202013928\40.jpeg'
tabl_lst_ = [83, 670, 2839, 3021]
tabl_lst_ = [252,478,2730,3826]
img_orignal = cv2.imread(file)
img_crop = img_crop_table(img_orignal, tabl_lst_)
img_crop = cv2.cvtColor(img_crop, cv2.COLOR_BGR2GRAY)
cv2.imwrite('zo.jpeg', img_crop)

img_mask = img_mask_horizontal_vertical(img_crop)
cv2.imwrite('zv.jpeg', img_mask)
img_mask = (img_mask/255)
img_mask = img_mask.astype('uint8')

col = column_genration(src_img=img_mask, tabl_lst=tabl_lst_)
imgoc = img_orignal.copy()
for ele in col:
    xc1, xc2 = ele
    imgoc = cv2.rectangle(imgoc, (xc1,tabl_lst_[1]), (xc2,tabl_lst_[3]),color=(0,0,255), thickness=2, lineType=cv2.LINE_AA)
cv2.imwrite('zoFinal.jpeg', imgoc)
