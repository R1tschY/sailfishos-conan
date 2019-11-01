cmake_minimum_required(VERSION 3.1)
project(PackageTest CXX)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

include(FeatureSummary)
find_package(ECM 5.0.0 REQUIRED NO_MODULE)

set_package_properties(ECM PROPERTIES TYPE REQUIRED 
  DESCRIPTION "Extra CMake Modules" 
  URL "https://projects.kde.org/projects/kdesupport/extra-cmake-modules")

feature_summary(
    FATAL_ON_MISSING_REQUIRED_PACKAGES
    WHAT ALL
)

set(CMAKE_MODULE_PATH ${ECM_MODULE_PATH})
include(ECMQtDeclareLoggingCategory)