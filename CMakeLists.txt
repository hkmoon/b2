cmake_minimum_required(VERSION 3.22)

project(bertini2)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# ----------------------------------------------------
# --- Policy -----------------------------------------
# CMake Policy setup
# ----------------------------------------------------
# Policy can be removed when cmake_minimum_required is updated.

# We also set CMAKE_POLICY_DEFAULT_CMPXXXX because CMake modules can reset
# policy and redefine some macros like `find_dependency` that will not use our
# policy.

# Use BoostConfig module distributed by boost library instead of using FindBoost
# module distributed by CMake (to remove in 3.30).
if(POLICY CMP0167)
  cmake_policy(SET CMP0167 NEW)
  set(CMAKE_POLICY_DEFAULT_CMP0167 NEW)
endif()
# install() DESTINATION paths are normalized (to remove in 3.31).
if(POLICY CMP0177)
  cmake_policy(SET CMP0177 NEW)
  set(CMAKE_POLICY_DEFAULT_CMP0177 NEW)
endif()

include(CMakePrintHelpers) # so we can print cmake variable values

include(GNUInstallDirs)  # so that `CMAKE_INSTALL_LIBDIR` is not blank. eg


# conda doesn't have 3.13 compatible eigenpy yet and build module needs 3.11
find_package(Python3 REQUIRED COMPONENTS Interpreter Development.Module NumPy)



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
