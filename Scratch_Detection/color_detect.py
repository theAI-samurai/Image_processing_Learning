"""
The Following file can be used to detect Color of an object
if it belongs to the following Segment
RED, YELLOW, WHITE, BLACK, BLUE

"""

import cv2
import numpy as np

color_threshold_dict = \
    {'lower_black': np.array([0, 0, 0]),
     'higher_black': np.array([150, 100, 59]),
     'lower_gray': np.array([3,3,40]),
     'higher_gray': np.array([160, 45, 100]),
     'lower_blue': np.array([95, 100, 70]),
     'upper_blue': np.array([110, 200, 220]),
     'lower_brown': np.array([4,60,50]),
     'higher_brown': np.array([20, 200, 125]),
     'lower_yellow': np.array([25, 50, 50]),
     'high_yellow': np.array([31, 255, 255]),
     'lower_orange': np.array([5,107, 147]),
     'higher_orange': np.array([17,255, 245]),
     'lower_red': np.array([165, 50, 50]),
     'higher_red': np.array([179, 255, 255]),
     'lower_white': np.array([0, 0, 168]),
     'high_white': np.array([157, 35, 255]),
     'lower_silver': np.array([20, 7, 79]),
     'higher_silver': np.array([155, 50,160]),
     }


def crop_img_cordinate_extract(img_path):
    temp = img_path.split('.')[0]
    temp = temp.split('/')[-1]
    temp = temp.split('_')
    y = int(temp[2])
    h = int(temp[3])
    x = int(temp[4])
    w = int(temp[5])
    return y, h, x, w


def background_subtraction(image_ref, image_obj, iter = 10, learningRate1=0.5, learningRate2=0):
    """
    This function does a background subtraction between image_ref and image_obj
    image_obj - image_ref = Mask Image
    This Function Requires openCV - contrib library

    :param image_ref: Reference Image contains only Background with no object
    :param image_obj: Image with Objects in front of Background Image
    :param iter: Iterations to Train Background Subtractor
    :param learningRate1: Learning Rate on Background Image
    :param learningRate2: Learning Rate on Object Image, Keep it 0
    :return: A Binary Masked Image
    """
    backgroundSubtractor = cv2.bgsegm.createBackgroundSubtractorMOG()
    for i in range(1, iter):
        # feeding with background image
        backgroundSubtractor.apply(image_ref, learningRate=learningRate1)
    # apply the Algorithm for detection image using learning rate 0
    fgmask = backgroundSubtractor.apply(image_obj, learningRate=learningRate2)

    return fgmask


def get_foreground_pixel_only(image, mask_img):
    """
    This function takes a BGR image as input and outputs a BGR image with only Foreground Pixel value
    and rest frames are marked with black pixel.

    :param image: An Orignal RGB image with all pixel value
    :param mask_img: A Binary Image obtained after Background Subtraction
    :return: 3 Channel BGR Image with only Foreground image, All
             other pixel value are  Zero across all Channel
    """
    foreground_image = np.zeros(shape=image.shape, dtype='uint8', order='C')
    for i in range(mask_img.shape[0]):
        for j in range(mask_img.shape[1]):
            if mask_img[i, j] == 255:
                foreground_image[i, j, :] = image[i, j, :]

    return foreground_image


def count_pixel(arry):
    """
    This function counts the pixels where Values of
    all the 3 Channel of color = 0
    :param arry: An Image Array with 3 channel like RGB/HSV
    :return: count of Pixels where any of the values in 3 channel
             is Non-Zero
    """
    non_zero_count = 0
    for i in range(arry.shape[0]):
        for j in range(arry.shape[1]):
            temp = arry[i, j, :]
            if not np.all((temp == 0)):
                non_zero_count += 1
    return non_zero_count


def count_pixel_(arry):
    """
    This function counts the pixels where Values is Non-Zero
    :param arry: An Image Array with just 1 channel like H in HSV
    :return: count of Pixels where any of the values in 1 channel
             is Non-Zero
    """
    non_zero_count = 0
    for i in range(arry.shape[0]):
        for j in range(arry.shape[1]):
            if not arry[i,j] == 0:
                non_zero_count += 1
    return non_zero_count


def Color_Detection_HSV(image_frame):
    """
    Takes a masked BGR Frame with only detected Item.
    Converts this BGR to HSV Domain for Color Thresholding.

    The Identification of color is performed using the HSV domain

    :param image_frame: A BGR Image Frame
    :return: String with Color Identified
    """

    test_hsv = cv2.cvtColor(image_frame, cv2.COLOR_BGR2HSV)                # BGR - HSV Domain   masked Detected

    mask_black = cv2.inRange(test_hsv, color_threshold_dict['lower_black'], color_threshold_dict['higher_black'])       # masking with in range BLACK
    mask_gray = cv2.inRange(test_hsv, color_threshold_dict['lower_gray'], color_threshold_dict['higher_gray'])          # masking with in range GRAY
    mask_blue = cv2.inRange(test_hsv, color_threshold_dict['lower_blue'], color_threshold_dict['upper_blue'])           # masking with in range BLUE
    mask_brown = cv2.inRange(test_hsv, color_threshold_dict['lower_brown'], color_threshold_dict['higher_brown'])       # masking with in range BROWN
    mask_yellow = cv2.inRange(test_hsv, color_threshold_dict['lower_yellow'], color_threshold_dict['high_yellow'])      # masking with in range YELLOW
    mask_orange = cv2.inRange(test_hsv, color_threshold_dict['lower_orange'], color_threshold_dict['higher_orange'])      # masking with in range ORANGE
    mask_red = cv2.inRange(test_hsv, color_threshold_dict['lower_red'], color_threshold_dict['higher_red'])             # masking with in range RED
    mask_silver = cv2.inRange(test_hsv, color_threshold_dict['lower_silver'], color_threshold_dict['high_silver'])      # masking with in range SILVER
    mask_white = cv2.inRange(test_hsv, color_threshold_dict['lower_white'], color_threshold_dict['high_white'])         # masking with in range WHITE

    res_hsv_black = cv2.bitwise_and(test_hsv, test_hsv, mask=mask_black)     # DOUBLE Masked  HSV
    res_hsv_gray = cv2.bitwise_and(test_hsv, test_hsv, mask=mask_gray)       # DOUBLE Masked  HSV
    res_hsv_blue = cv2.bitwise_and(test_hsv, test_hsv, mask=mask_blue)       # DOUBLE Masked  HSV
    res_hsv_brown = cv2.bitwise_and(test_hsv, test_hsv, mask=mask_brown)     # DOUBLE Masked  HSV
    res_hsv_yellow = cv2.bitwise_and(test_hsv, test_hsv, mask=mask_yellow)   # DOUBLE Masked  HSV
    res_hsv_orange = cv2.bitwise_and(test_hsv, test_hsv, mask=mask_orange)   # DOUBLE Masked  HSV
    res_hsv_red = cv2.bitwise_and(test_hsv, test_hsv, mask=mask_red)         # DOUBLE Masked  HSV
    res_hsv_white = cv2.bitwise_and(test_hsv, test_hsv, mask=mask_white)     # DOUBLE Masked  HSV
    res_hsv_silver = cv2.bitwise_and(test_hsv, test_hsv, mask=mask_silver)   # DOUBLE Masked  HSV


    nz_balck_bgr = count_pixel_(cv2.split(res_hsv_black)[0])
    nz_gray_bgr = count_pixel_(cv2.split(res_hsv_gray)[0])
    nz_blue_bgr = count_pixel_(cv2.split(res_hsv_blue)[0])
    nz_brown_bgr = count_pixel_(cv2.split(res_hsv_brown)[0])
    nz_red_bgr = count_pixel_(cv2.split(res_hsv_red)[0])
    nz_orange_bgr = count_pixel_(cv2.split(res_hsv_orange)[0])
    nz_white_bgr = count_pixel_(cv2.split(res_hsv_white)[0])
    nz_silver_bgr = count_pixel_(cv2.split(res_hsv_silver)[0])
    nz_yellow_bgr = count_pixel_(cv2.split(res_hsv_yellow)[0])

    if nz_balck_bgr > nz_white_bgr and nz_balck_bgr > nz_red_bgr and nz_balck_bgr > nz_blue_bgr \
            and nz_balck_bgr > nz_yellow_bgr and nz_balck_bgr > nz_gray_bgr and nz_balck_bgr > nz_brown_bgr \
            and nz_balck_bgr > nz_orange_bgr and nz_balck_bgr > nz_silver_bgr:
        return "BLACK"
    elif nz_white_bgr > nz_balck_bgr and nz_white_bgr > nz_red_bgr and nz_white_bgr > nz_blue_bgr \
            and nz_white_bgr > nz_yellow_bgr and nz_white_bgr > nz_gray_bgr and nz_white_bgr > nz_brown_bgr \
            and nz_white_bgr > nz_orange_bgr and nz_white_bgr > nz_silver_bgr:
        return "WHITE"
    elif nz_red_bgr > nz_balck_bgr and nz_red_bgr > nz_white_bgr and nz_red_bgr > nz_blue_bgr \
            and nz_red_bgr > nz_yellow_bgr and nz_red_bgr > nz_gray_bgr and nz_red_bgr > nz_brown_bgr \
            and nz_red_bgr > nz_orange_bgr and nz_red_bgr > nz_silver_bgr:
        return "RED"
    elif nz_blue_bgr > nz_balck_bgr and nz_blue_bgr > nz_white_bgr and nz_blue_bgr > nz_red_bgr \
            and nz_blue_bgr > nz_yellow_bgr and nz_blue_bgr > nz_gray_bgr and nz_blue_bgr > nz_brown_bgr \
            and nz_blue_bgr > nz_orange_bgr and nz_blue_bgr > nz_silver_bgr:
        return "BLUE"
    elif nz_yellow_bgr > nz_balck_bgr and nz_yellow_bgr > nz_white_bgr and nz_yellow_bgr > nz_blue_bgr and nz_yellow_bgr > nz_red_bgr \
            and nz_yellow_bgr > nz_gray_bgr and nz_yellow_bgr > nz_brown_bgr and nz_yellow_bgr > nz_orange_bgr and nz_yellow_bgr > nz_silver_bgr:
        return "YELLOW"
    elif nz_gray_bgr > nz_balck_bgr and nz_gray_bgr > nz_white_bgr and nz_gray_bgr > nz_blue_bgr and nz_gray_bgr > nz_red_bgr \
            and nz_gray_bgr > nz_yellow_bgr and nz_gray_bgr > nz_brown_bgr and nz_gray_bgr > nz_orange_bgr and nz_gray_bgr > nz_silver_bgr:
        return "GRAY"
    elif nz_brown_bgr > nz_balck_bgr and nz_brown_bgr > nz_white_bgr and nz_brown_bgr > nz_blue_bgr and nz_brown_bgr > nz_red_bgr \
            and nz_brown_bgr > nz_yellow_bgr and nz_brown_bgr > nz_gray_bgr and nz_brown_bgr > nz_orange_bgr and nz_brown_bgr > nz_silver_bgr:
        return "BROWN"
    elif nz_orange_bgr > nz_balck_bgr and nz_orange_bgr > nz_white_bgr and nz_orange_bgr > nz_blue_bgr and nz_orange_bgr > nz_red_bgr \
            and nz_orange_bgr > nz_yellow_bgr and nz_orange_bgr > nz_gray_bgr and nz_orange_bgr > nz_brown_bgr and nz_orange_bgr > nz_silver_bgr:
        return "ORANGE"
    elif nz_silver_bgr > nz_balck_bgr and nz_silver_bgr > nz_white_bgr and nz_silver_bgr > nz_blue_bgr and nz_silver_bgr > nz_red_bgr \
            and nz_silver_bgr > nz_yellow_bgr and nz_silver_bgr > nz_gray_bgr and nz_silver_bgr > nz_brown_bgr and nz_silver_bgr > nz_orange_bgr:
        return "SILVER"


def Color_Detection_RGB(image_frame):
    """
    Takes a masked BGR Frame with only detected Item.
    Converts this BGR to HSV Domain for Color Thresholding.

    The Identification of color is performed using the BGR domain.

    :param image_frame: A BGR Image Frame
    :return: String with Color Identified
    """

    test_hsv = cv2.cvtColor(image_frame, cv2.COLOR_BGR2HSV)                # BGR - HSV Domain   masked Detected

    mask_black = cv2.inRange(test_hsv, color_threshold_dict['lower_black'], color_threshold_dict['higher_black'])       # masking with in range BLACK
    mask_gray = cv2.inRange(test_hsv, color_threshold_dict['lower_gray'], color_threshold_dict['higher_gray'])          # masking with in range GRAY
    mask_blue = cv2.inRange(test_hsv, color_threshold_dict['lower_blue'], color_threshold_dict['upper_blue'])           # masking with in range BLUE
    mask_brown = cv2.inRange(test_hsv, color_threshold_dict['lower_brown'], color_threshold_dict['higher_brown'])       # masking with in range BROWN
    mask_yellow = cv2.inRange(test_hsv, color_threshold_dict['lower_yellow'], color_threshold_dict['high_yellow'])      # masking with in range YELLOW
    mask_orange = cv2.inRange(test_hsv, color_threshold_dict['lower_orange'], color_threshold_dict['higher_orange'])      # masking with in range ORANGE
    mask_red = cv2.inRange(test_hsv, color_threshold_dict['lower_red'], color_threshold_dict['higher_red'])             # masking with in range RED
    mask_silver = cv2.inRange(test_hsv, color_threshold_dict['lower_silver'], color_threshold_dict['higher_silver'])      # masking with in range SILVER
    mask_white = cv2.inRange(test_hsv, color_threshold_dict['lower_white'], color_threshold_dict['high_white'])         # masking with in range WHITE

    res_bgr_black = cv2.bitwise_and(image_frame, image_frame, mask=mask_black)  # DOUBLE Masked  HSV
    res_bgr_gray = cv2.bitwise_and(image_frame, image_frame, mask=mask_gray)  # DOUBLE Masked  HSV
    res_bgr_blue = cv2.bitwise_and(image_frame, image_frame, mask=mask_blue)  # DOUBLE Masked  HSV
    res_bgr_brown = cv2.bitwise_and(image_frame, image_frame, mask=mask_brown)  # DOUBLE Masked  HSV
    res_bgr_yellow = cv2.bitwise_and(image_frame, image_frame, mask=mask_yellow)  # DOUBLE Masked  HSV
    res_bgr_orange = cv2.bitwise_and(image_frame, image_frame, mask=mask_orange)  # DOUBLE Masked  HSV
    res_bgr_red = cv2.bitwise_and(image_frame, image_frame, mask=mask_red)  # DOUBLE Masked  HSV
    res_bgr_white = cv2.bitwise_and(image_frame, image_frame, mask=mask_white)  # DOUBLE Masked  HSV
    res_bgr_silver = cv2.bitwise_and(image_frame, image_frame, mask=mask_silver)  # DOUBLE Masked  HSV


    nz_balck_bgr = count_pixel_(cv2.split(res_bgr_black)[0])
    nz_gray_bgr = count_pixel_(cv2.split(res_bgr_gray)[0])
    nz_blue_bgr = count_pixel_(cv2.split(res_bgr_blue)[0])
    nz_brown_bgr = count_pixel_(cv2.split(res_bgr_brown)[0])
    nz_red_bgr = count_pixel_(cv2.split(res_bgr_red)[0])
    nz_orange_bgr = count_pixel_(cv2.split(res_bgr_orange)[0])
    nz_white_bgr = count_pixel_(cv2.split(res_bgr_white)[0])
    nz_silver_bgr = count_pixel_(cv2.split(res_bgr_silver)[0])
    nz_yellow_bgr = count_pixel_(cv2.split(res_bgr_yellow)[0])


    if nz_balck_bgr > nz_white_bgr and nz_balck_bgr > nz_red_bgr and nz_balck_bgr > nz_blue_bgr \
            and nz_balck_bgr > nz_yellow_bgr and nz_balck_bgr > nz_gray_bgr and nz_balck_bgr > nz_brown_bgr \
            and nz_balck_bgr > nz_orange_bgr and nz_balck_bgr > nz_silver_bgr:
        return "BLACK"
    elif nz_white_bgr > nz_balck_bgr and nz_white_bgr > nz_red_bgr and nz_white_bgr > nz_blue_bgr \
            and nz_white_bgr > nz_yellow_bgr and nz_white_bgr > nz_gray_bgr and nz_white_bgr > nz_brown_bgr \
            and nz_white_bgr > nz_orange_bgr and nz_white_bgr > nz_silver_bgr:
        return "WHITE"
    elif nz_red_bgr > nz_balck_bgr and nz_red_bgr > nz_white_bgr and nz_red_bgr > nz_blue_bgr \
            and nz_red_bgr > nz_yellow_bgr and nz_red_bgr > nz_gray_bgr and nz_red_bgr > nz_brown_bgr \
            and nz_red_bgr > nz_orange_bgr and nz_red_bgr > nz_silver_bgr:
        return "RED"
    elif nz_blue_bgr > nz_balck_bgr and nz_blue_bgr > nz_white_bgr and nz_blue_bgr > nz_red_bgr \
            and nz_blue_bgr > nz_yellow_bgr and nz_blue_bgr > nz_gray_bgr and nz_blue_bgr > nz_brown_bgr \
            and nz_blue_bgr > nz_orange_bgr and nz_blue_bgr > nz_silver_bgr:
        return "BLUE"
    elif nz_yellow_bgr > nz_balck_bgr and nz_yellow_bgr > nz_white_bgr and nz_yellow_bgr > nz_blue_bgr and nz_yellow_bgr > nz_red_bgr \
            and nz_yellow_bgr > nz_gray_bgr and nz_yellow_bgr > nz_brown_bgr and nz_yellow_bgr > nz_orange_bgr and nz_yellow_bgr > nz_silver_bgr:
        return "YELLOW"
    elif nz_gray_bgr > nz_balck_bgr and nz_gray_bgr > nz_white_bgr and nz_gray_bgr > nz_blue_bgr and nz_gray_bgr > nz_red_bgr \
            and nz_gray_bgr > nz_yellow_bgr and nz_gray_bgr > nz_brown_bgr and nz_gray_bgr > nz_orange_bgr and nz_gray_bgr > nz_silver_bgr:
        return "GRAY"
    elif nz_brown_bgr > nz_balck_bgr and nz_brown_bgr > nz_white_bgr and nz_brown_bgr > nz_blue_bgr and nz_brown_bgr > nz_red_bgr \
            and nz_brown_bgr > nz_yellow_bgr and nz_brown_bgr > nz_gray_bgr and nz_brown_bgr > nz_orange_bgr and nz_brown_bgr > nz_silver_bgr:
        return "BROWN"
    elif nz_orange_bgr > nz_balck_bgr and nz_orange_bgr > nz_white_bgr and nz_orange_bgr > nz_blue_bgr and nz_orange_bgr > nz_red_bgr \
            and nz_orange_bgr > nz_yellow_bgr and nz_orange_bgr > nz_gray_bgr and nz_orange_bgr > nz_brown_bgr and nz_orange_bgr > nz_silver_bgr:
        return "ORANGE"
    elif nz_silver_bgr > nz_balck_bgr and nz_silver_bgr > nz_white_bgr and nz_silver_bgr > nz_blue_bgr and nz_silver_bgr > nz_red_bgr \
            and nz_silver_bgr > nz_yellow_bgr and nz_silver_bgr > nz_gray_bgr and nz_silver_bgr > nz_brown_bgr and nz_silver_bgr > nz_orange_bgr:
        return "SILVER"