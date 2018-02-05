import cv2
import os
import xml.etree.ElementTree as ET
import json
import shutil
import numpy as np

filename = 'img1.xml'
tree = ET.parse(filename)
objs = tree.findall('object')
num_objs = len(objs)

img = cv2.imread('img1.jpg')
height,width,channel = img.shape
print img.shape
blank_image = np.zeros((height,width,3),np.uint8)
for ix,obj in enumerate(objs):

   bbox = obj.findall('polygon')
   for idx,index in enumerate(bbox):
	#print index.find('username').text
	a = index.findall('pt')
	point = []
	for i,h in enumerate(a):
		x = float(h.find('x').text)
		y = float(h.find('y').text)
		point.append([x,y])
        pts = np.array(point,np.int32)
	cv2.polylines(blank_image,[pts],True,(255,255,255))
cv2.namedWindow('img', cv2.WINDOW_NORMAL)
cv2.imshow("img",blank_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
