cmake_minimum_required(VERSION 3.12)

project(lab6)

set(CMAKE_CXX_STANDARD 20)

add_executable(main
    src/main.cpp
)

set_target_properties(main PROPERTIES OUTPUT_NAME "main")