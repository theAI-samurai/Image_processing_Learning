from darknet_detection import *
import cv2
from color_detect import *

obj = ObjectDetection(cfgPath='yolov3.cfg', wgtPath='yolov3.weights', dataPath='coco.data')

base_path = 'D:/cloned_repos/Image_processing_Learning/Scratch_Detection/image_dataset/'


for f in os.listdir(base_path):
    im = cv2.imread(base_path+f)
    res = obj.detect(base_path+f)
    print(f, res)
    if len(res) != 0 :
        for r in res:
            x1,y1,x2,y2 = bbox2points(r[2])

            # crop image
            try:
                crop_im = im[y1:y2, x1:x2]
                print(crop_im.shape)
                c = Color_Detection_RGB(crop_im)
                print(c)
                cv2.imshow('lklnllvk', crop_im)
                cv2.waitKey(0)
            except:
                pass

    else:
        color = Color_Detection_RGB(im)
        print(color)
        cv2.imshow('lklnllvk', im)
        cv2.waitKey(0)

cv2.destroyAllWindows()
