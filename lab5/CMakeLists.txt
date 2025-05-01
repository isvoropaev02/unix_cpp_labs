cmake_minimum_required(VERSION 3.12)

project(lab5)

set(CMAKE_CXX_STANDARD 20)

add_executable(run_spl src/run_spl.cpp)

set_target_properties(run_spl PROPERTIES OUTPUT_NAME "run_spl")