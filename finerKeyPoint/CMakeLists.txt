cmake_minimum_required(VERSION 2.8)

set(CMAKE_CXX_FLAGS "-std=c++11")
project(keypoint)
find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS})
add_library(keypoint_shared SHARED libkeypoint.cpp)
add_executable(keypoint main.cpp)

target_link_libraries(keypoint ${OpenCV_LIBS})
target_link_libraries(keypoint keypoint_shared)
