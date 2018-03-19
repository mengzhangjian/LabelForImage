import tensorflow as tf
import cv2
import os
import numpy as np
from PIL import Image

def load_image(filename):
    
    test_filename = os.path.join('test',filename)
    image = Image.open(test_filename)
    image = image.resize((480,320))
    #image = np.array(image,np.float32)
    #image = image[:,:,[2,1,0]]
    #image -=[103.939,116.779,123.68]


    return image
image = load_image("1.jpg")
image.show()
