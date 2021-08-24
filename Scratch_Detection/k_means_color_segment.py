import cv2
import numpy as np
import matplotlib.pyplot as plt
import sys

path = r'D:\cloned_repos\Image_processing_Learning\Scratch_Detection\image_dataset\5.jpg'


def k_mean_image(img, num_clusters):
    # read the image
    # image = cv2.imread(path)
    # image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    image = img

    # reshape the image to a 2D array of pixels and 3 color values (RGB)
    pixel_values = image.reshape((-1, 3))
    pixel_values = np.float32(pixel_values)

    # define stopping criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)

    # number of clusters (K)
    k = num_clusters
    compactness, labels, (centers) = cv2.kmeans(pixel_values, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # convert back to 8 bit values
    centers = np.uint8(centers)
    labels = labels.flatten()

    # convert all pixels to the color of the centroids
    segmented_image = centers[labels]

    # reshape back to the original image dimension
    segmented_image = segmented_image.reshape(image.shape)

    return segmented_image