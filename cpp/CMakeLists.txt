cmake_minimum_required(VERSION 3.16)
project(HumanDetectionDVR)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find required packages
find_package(OpenCV REQUIRED)
find_package(PkgConfig REQUIRED)
find_package(jsoncpp CONFIG REQUIRED)
find_package(cppzmq CONFIG REQUIRED)
find_package(zeromq CONFIG REQUIRED)

# include_directories(${OpenCV_INCLUDE_DIRS})
# include_directories(${ZMQ_INCLUDE_DIRS})
include_directories(include)

# Source files
set(SOURCES
    src/main.cpp
    src/video_capture.cpp
    src/zmq_sender.cpp
)

# Create executable
add_executable(video_capture ${SOURCES})

# Link libraries
target_link_libraries(video_capture 
    ${OpenCV_LIBS}
    cppzmq
    libzmq
    JsonCpp::JsonCpp
)

# Compiler flags
target_compile_options(video_capture PRIVATE ${ZMQ_CFLAGS_OTHER})

# Set output directory
set_target_properties(video_capture PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}
)

# Print configuration info
message(STATUS "OpenCV version: ${OpenCV_VERSION}")
message(STATUS "ZMQ version: ${ZMQ_VERSION}")
message(STATUS "Build type: ${CMAKE_BUILD_TYPE}")