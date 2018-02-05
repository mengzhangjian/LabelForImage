import cv2
import os
import xml.etree.ElementTree as ET
import json
import shutil
import argparse
"""
in the directory datapath ,there are Annotations and Image folder

"""
name_list = []
 
def load_annotation(datapath,index,idx):
  
    
    count = 0
    filename = os.path.join(datapath,'Annotations',index + '.xml')
    print filename
    imagename = os.path.join(datapath,'JPEGImages', index + '.jpg')
    #while  not os.path.isfile(imagename):
    #	pass
    image = cv2.imread(imagename)
    print imagename
    tree = ET.parse(filename)
    objs = tree.findall('object')
    num_objs = len(objs)
   
    for ix,obj in enumerate(objs):
        
        bbox = obj.find('bndbox')
        x1 = float(bbox.find('xmin').text) - 1
        y1 = float(bbox.find('ymin').text) - 1
        x2 = float(bbox.find('xmax').text) - 1
        y2 = float(bbox.find('ymax').text) - 1 
        width = x2 - x1 
        height = y2 - y1
	if x1 <0  or y1<0 or x2<0 or y2 <0 :
	   if os.path.exists(filename):
	   	os.remove(filename)
           else:
		continue
	   print("delete filename:",filename)
	   continue
        obj_name = obj.find('name').text.lower().strip()
#	print x1, width,y1,height
        im  = image[int(y1):int(y1) + int(height),int(x1):int(x1) + int(width)]
        imagename = str(idx)+'_'+str(count) + '.jpg'
        if obj_name in name_list:
            

            filepath = os.path.join(datapath,'Base',obj_name)
            image_name = os.path.join(filepath,imagename)
            cv2.imwrite(image_name,im)
        else:

        	filepath = os.path.join(datapath,'Base',obj_name)
		if os.path.exists(filepath):
 			pass
		else:
        		os.mkdir(filepath)
                image_name = os.path.join(filepath,imagename)
        	name_list.append(obj_name)
        	cv2.imwrite(image_name,im)
        count  = count + 1

def get_image_index(datapath):

	image_set_file = os.path.join(datapath,'ImageSets','Main','trainval.txt')

	assert os.path.exists(image_set_file), \
	  'Path does not exist: {}'.format(image_set_file)
	with open(image_set_file) as f:
		image_index = [x.strip() for x in f.readlines()]
	return image_index

if __name__=='__main__':


   #conf_file =  os.path.join('.','conf.json')
   #assert os.path.exists(conf_file),\
    #  'Path does not exist:{}'.format(conf_file)
   file = open('log.txt','w')
   conf = json.load(open('conf.json'))
   datapath = conf["datapath"]
   image_index = get_image_index(datapath)
   #print image_index
   for idx,index in enumerate(image_index):
 #     print index
       print '---------loading the %d %s images',idx,index

       file.write(str(idx) + ' ' +str(index) +'\n')
       filename = os.path.join(datapath,'Annotations',index + '.xml')
       if os.path.exists(filename):
       		load_annotation(datapath,index,idx)
       else:
		continue
   file.close()






