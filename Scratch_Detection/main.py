from darknet_detection import *


obj = ObjectDetection(cfgPath='yolov3-tiny.cfg', wgtPath='yolov3-tiny.weights', dataPath='coco.data')

res = obj.detect('D:/cloned_repos/Image_processing_Learning/Scratch_Detection/image_dataset/n.jpg')
print(res)
