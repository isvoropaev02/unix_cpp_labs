cmake_minimum_required(VERSION 3.12)

project(lab5)

set(CMAKE_CXX_STANDARD 20)

add_executable(run_spl
    src/run_spl.cpp
    src/parser/parser.cpp
    src/core/core.cpp
)

target_include_directories(run_spl PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/parser
    ${CMAKE_CURRENT_SOURCE_DIR}/core
)

set_target_properties(run_spl PROPERTIES OUTPUT_NAME "run_spl")