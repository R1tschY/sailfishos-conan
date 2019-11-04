cmake_minimum_required(VERSION 3.1)
project(PackageTest CXX)

set(CMAKE_CXX_STANDARD 11)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

find_package(ECM 5.0.0 REQUIRED NO_MODULE)
set(CMAKE_MODULE_PATH ${ECM_MODULE_PATH})

include(FeatureSummary)

set_package_properties(ECM PROPERTIES TYPE REQUIRED 
DESCRIPTION "Extra CMake Modules" 
URL "https://projects.kde.org/projects/kdesupport/extra-cmake-modules")

find_package(KF5 ${KF5_MIN_VERSION} REQUIRED COMPONENTS Config)
find_package(Qt5Core)

add_executable(example example.cpp)
target_link_libraries(example Qt5::Core KF5::ConfigCore)

feature_summary(
  FATAL_ON_MISSING_REQUIRED_PACKAGES
  WHAT ALL
)
