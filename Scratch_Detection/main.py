from darknet_detection import *
import cv2
from color_detect import *
from k_means_color_segment import *
from classification_decision import *

obj = ObjectDetection(cfgPath='yolov3.cfg', wgtPath='yolov3.weights', dataPath='coco.data')

base_path = 'image_dataset/'
result_f = 'result/'

ctr = 0

for f in os.listdir(base_path):
    im = cv2.imread(base_path+f)
    res = obj.detect(base_path+f)
    if len(res) != 0:
        for r in res:
            x1,y1,x2,y2 = bbox2points(r[2])
            print('-------------------------------------------------------', f)
            # crop image

            crop_im = im[y1:y2, x1:x2]
            label, msk_img = Color_Detection_RGB(crop_im)
            print(label)

            clus_img = k_mean_image(msk_img, num_clusters=4)

            # classification to faulty or not
            decision_ = decision(clus_img)

            if decision_:
                # image section needs review
                cv2.imwrite(result_f+'bad/'+f, im)
            else:
                cv2.imwrite(result_f + 'good/' + f, im)

            name = result_f + 'interim/' +f.split('.')[0] + '_'
            cv2.imwrite(name+str(ctr)+'_masked.jpg', msk_img)
            cv2.imwrite(name + str(ctr) + '_cluster.jpg', clus_img)
            ctr += 1


    else:
        #color = Color_Detection_RGB(im)
        cv2.imwrite(result_f+'bad/'+f, im)
        print('Model couldnt find a car object')

