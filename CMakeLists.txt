cmake_minimum_required(VERSION 3.16)
project(HumanDetectionDVR)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Add subdirectory for C++ component
add_subdirectory(cpp)

# Print project information
message(STATUS "=== Human Detection DVR System ===")
message(STATUS "Project: ${PROJECT_NAME}")
message(STATUS "Version: 1.0.0")
message(STATUS "Build type: ${CMAKE_BUILD_TYPE}")
message(STATUS "=====================================") 