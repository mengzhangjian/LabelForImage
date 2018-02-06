#include "opencv2/opencv.hpp"

using namespace std;
using namespace cv;
//using namespace cv::xfeatures2d;

// Perform a single thinning iteration, which is repeated until the skeletization is finalized
void thinningIteration(Mat& im, int iter)
{
    Mat marker = Mat::zeros(im.size(), CV_8UC1);
    for (int i = 1; i < im.rows-1; i++)
    {
        for (int j = 1; j < im.cols-1; j++)
        {
            uchar p2 = im.at<uchar>(i-1, j);
            uchar p3 = im.at<uchar>(i-1, j+1);
            uchar p4 = im.at<uchar>(i, j+1);
            uchar p5 = im.at<uchar>(i+1, j+1);
            uchar p6 = im.at<uchar>(i+1, j);
            uchar p7 = im.at<uchar>(i+1, j-1);
            uchar p8 = im.at<uchar>(i, j-1);
            uchar p9 = im.at<uchar>(i-1, j-1);

            int A  = (p2 == 0 && p3 == 1) + (p3 == 0 && p4 == 1) +
                     (p4 == 0 && p5 == 1) + (p5 == 0 && p6 == 1) +
                     (p6 == 0 && p7 == 1) + (p7 == 0 && p8 == 1) +
                     (p8 == 0 && p9 == 1) + (p9 == 0 && p2 == 1);
            int B  = p2 + p3 + p4 + p5 + p6 + p7 + p8 + p9;
            int m1 = iter == 0 ? (p2 * p4 * p6) : (p2 * p4 * p8);
            int m2 = iter == 0 ? (p4 * p6 * p8) : (p2 * p6 * p8);

            if (A == 1 && (B >= 2 && B <= 6) && m1 == 0 && m2 == 0)
                marker.at<uchar>(i,j) = 1;
        }
    }

    im &= ~marker;
}

// Function for thinning any given binary image within the range of 0-255. If not you should first make sure that your image has this range preset and configured!
void thinning(Mat& im)
{
     // Enforce the range tob e in between 0 - 255
    im /= 255;

    Mat prev = Mat::zeros(im.size(), CV_8UC1);
    Mat diff;

    do {
        thinningIteration(im, 0);
        thinningIteration(im, 1);
        absdiff(im, prev, diff);
        im.copyTo(prev);
    }
    while (countNonZero(diff) > 0);

    im *= 255;
}

int keypoint(Mat &input)
{
    Mat input_binary;
    threshold(input, input_binary,20, 255, THRESH_BINARY|THRESH_OTSU);
    //imshow("img",input_binary);
    Mat input_thinned = input_binary.clone();
    thinning(input_thinned);
    //imshow("img1",input_thinned);
    Mat harris_corners, harris_normalised;
    harris_corners = Mat::zeros(input_thinned.size(), CV_32FC1);
    cornerHarris(input_thinned, harris_corners, 2, 3, 0.04, BORDER_DEFAULT);
    normalize(harris_corners, harris_normalised, 0, 255, NORM_MINMAX, CV_32FC1, Mat());
    int threshold_harris = 125;
    vector<KeyPoint> keypoints;

    // Make a color clone for visualisation purposes
    Mat rescaled;
    convertScaleAbs(harris_normalised, rescaled);
    Mat harris_c(rescaled.rows, rescaled.cols, CV_8UC3);
    Mat in[] = { rescaled, rescaled, rescaled };
    int from_to[] = { 0,0, 1,1, 2,2 };
    mixChannels( in, 3, &harris_c, 1, from_to, 3 );
    for(int x=0; x<harris_normalised.cols; x++){
        for(int y=0; y<harris_normalised.rows; y++){
           if ( (int)harris_normalised.at<float>(y, x) > threshold_harris ){
              // Draw or store the keypoint location here, just like you decide. In our case we will store the location of the keypoint
              circle(harris_c, Point(x, y), 5, Scalar(0,255,0), 1);
              circle(harris_c, Point(x, y), 1, Scalar(0,0,255), 1);
              keypoints.push_back( KeyPoint (x, y, 1) );
           }
        }
     }
    imshow("temp", harris_c); waitKey(0);
    std::cout<<keypoints.size()<<std::endl;
    return keypoints.size();
}


