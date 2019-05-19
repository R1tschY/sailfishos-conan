cmake_minimum_required(VERSION 3.1)
project(PackageTest CXX)

set(CMAKE_MODULE_PATH ${CMAKE_BINARY_DIR})
set(CMAKE_CXX_STANDARD 11)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

find_package(Qt5Core)

add_executable(example example.cpp)
target_link_libraries(example Qt5::Core CONAN_PKG::KCoreAddons)

# CTest is a testing tool that can be used to test your project.
# enable_testing()
# add_test(NAME example
#          WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/bin
#          COMMAND example)
