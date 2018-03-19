import cv2
import os
import xml.etree.ElementTree as ET
import json
import shutil
import numpy as np
import argparse

            
def load_annotation(datapath,index,idx):
    filename = os.path.join(datapath,'Annotations',index + '.xml')
    imageName = os.path.join(datapath,'JPEGImages',index + '.jpg')
    tree = ET.parse(filename)
    objs = tree.findall('object')
    img = cv2.imread(imageName)
    height,width,channel = img.shape
    blank_image = np.zeros((height,width,3),np.uint8)
    for ix,obj in enumerate(objs):

        bbox = obj.findall('polygon')
        for idx,ele in enumerate(bbox):
	#print index.find('username').text
	        a = ele.findall('pt')
	        point = []
	        for i,h in enumerate(a):
		        x = float(h.find('x').text)
		        y = float(h.find('y').text)
		        point.append([x,y])
                pts = np.array(point,np.int32)
	        cv2.polylines(blank_image,[pts],True,(255,255,255),2)
    savename = os.path.join(datapath,'BinaryImages',str(index)+ '.jpg')
    cv2.imwrite(savename,blank_image)


def get_image_index(datapath):

	image_set_file = os.path.join(datapath,'ImageSets','Main','trainval.txt')

	assert os.path.exists(image_set_file), \
	  'Path does not exist: {}'.format(image_set_file)
	with open(image_set_file) as f:
		image_index = [x.strip() for x in f.readlines()]
	return image_index

def parse_args():

    "Parse input arguments"
    parser = argparse.ArgumentParser(description='Parser input arguments')
    parser.add_argument('--path',dest='datapath',help='Voc data path',default = './')
    args = parser.parse_args()
    return args


if __name__=='__main__':

    args = parse_args()
    image_index = get_image_index(args.datapath)
    for idx,index in enumerate(image_index):
        filename = os.path.join(args.datapath,'Annotations',index +'.xml')
        if os.path.exists(filename):
            load_annotation(args.datapath,index,idx)
        else:
            continue
    
        

    
