#include<opencv2/opencv.hpp>
#include"libkeypoint.h"
using namespace cv;

int main(int argc,char** argv)

{
  Mat image = imread("1.png",0);
  
  std::cout<< keypoint(image)<<std::endl;
  return 0;
}
