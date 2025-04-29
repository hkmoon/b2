cmake_minimum_required(VERSION 3.22)

project(bertini2)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

if(NOT WIN32)
  target_compile_options(
    ${PROJECT_NAME} PRIVATE $<$<CXX_COMPILER_ID:MSVC>:-bigobj -MP>
                            "-Wno-conversion")
else()
  target_compile_options(${PROJECT_NAME}
                         PRIVATE $<$<CXX_COMPILER_ID:MSVC>:-bigobj -MP>)
  target_compile_definitions(${PROJECT_NAME} PUBLIC "HAVE_SNPRINTF")
endif()

include(CMakePrintHelpers) # so we can print cmake variable values

include(GNUInstallDirs)  # so that `CMAKE_INSTALL_LIBDIR` is not blank. eg


# conda doesn't have 3.13 compatible eigenpy yet and build module needs 3.11
find_package(Python 3.11 REQUIRED COMPONENTS Interpreter Development.Module NumPy)



############################
# the core builds a library and an executable depending on that library
#

add_library(bertini2)

add_executable(bertini2_exe)
set_property(TARGET bertini2_exe PROPERTY OUTPUT_NAME bertini2)

add_subdirectory(core)




###########
# next, in `python_bindings`, build a shared python library, and a pure-python library that wraps around that.
#


python_add_library(_pybertini MODULE WITH_SOABI)

add_subdirectory(python_bindings)



###########
# finally, the pure-python part of the project.
#

add_subdirectory(python)
