#ifndef KEYPOINT_H
#define KEYPOINT_H
using namespace cv;
using namespace std;
void thinningIteration(Mat& im, int iter);
int keypoint(Mat &input);
void thinning(Mat& im);
#endif // KEYPOINT_H
