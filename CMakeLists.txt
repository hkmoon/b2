cmake_minimum_required(VERSION 3.22)

set(PROJECT_NAME bertini2)
set(PROJECT_DESCRIPTION "Implementation of the foundations of Numerical Algebraic Geometry")
set(PROJECT_URL "https://github.com/bertiniteam/b2")
set(PROJECT_USE_CMAKE_EXPORT TRUE)
set(PROJECT_USE_KEYWORD_LINK_LIBRARIES TRUE)
set(PROJECT_CUSTOM_HEADER_EXTENSION "hpp")

set(PROJECT_AUTO_RUN_FINALIZE FALSE)
set(PROJECT_SOURCE_DIR ${CMAKE_CURRENT_LIST_DIR})

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# Check if the submodule cmake have been initialized
set(JRL_CMAKE_MODULES "${CMAKE_CURRENT_LIST_DIR}/cmake")
if(EXISTS "${JRL_CMAKE_MODULES}/base.cmake")
  message(STATUS "JRL cmakemodules found in 'cmake/' git submodule")
else()
  find_package(jrl-cmakemodules QUIET CONFIG)
  if(jrl-cmakemodules_FOUND)
    get_property(
      JRL_CMAKE_MODULES
      TARGET jrl-cmakemodules::jrl-cmakemodules
      PROPERTY INTERFACE_INCLUDE_DIRECTORIES)
    message(STATUS "JRL cmakemodules found on system at ${JRL_CMAKE_MODULES}")
  elseif(${CMAKE_VERSION} VERSION_LESS "3.14.0")
    message(
      FATAL_ERROR
        "\nCan't find jrl-cmakemodules. Please either:\n"
        "  - use git submodule: 'git submodule update --init'\n"
        "  - or install https://github.com/jrl-umi3218/jrl-cmakemodules\n"
        "  - or upgrade your CMake version to >= 3.14 to allow automatic fetching\n"
    )
  else()
    message(STATUS "JRL cmakemodules not found. Let's fetch it.")
    include(FetchContent)
    FetchContent_Declare(
      "jrl-cmakemodules"
      GIT_REPOSITORY "https://github.com/jrl-umi3218/jrl-cmakemodules.git")
    FetchContent_MakeAvailable("jrl-cmakemodules")
    FetchContent_GetProperties("jrl-cmakemodules" SOURCE_DIR JRL_CMAKE_MODULES)
  endif()
endif()

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
include("${JRL_CMAKE_MODULES}/base.cmake")
compute_project_args(PROJECT_ARGS LANGUAGES CXX)
project(${PROJECT_NAME} ${PROJECT_ARGS})

include("${JRL_CMAKE_MODULES}/boost.cmake")
include("${JRL_CMAKE_MODULES}/python.cmake")
include("${JRL_CMAKE_MODULES}/ide.cmake")
include("${JRL_CMAKE_MODULES}/apple.cmake")


include(CMakePrintHelpers) # so we can print cmake variable values

include(GNUInstallDirs)  # so that `CMAKE_INSTALL_LIBDIR` is not blank. eg


# conda doesn't have 3.13 compatible eigenpy yet and build module needs 3.11
find_package(Python 3.11 REQUIRED COMPONENTS Interpreter Development.Module NumPy)

string(REPLACE "-pedantic" "" CMAKE_CXX_FLAGS ${CMAKE_CXX_FLAGS})


# If needed, fix CMake policy for APPLE systems
apply_default_apple_configuration()
check_minimal_cxx_standard(11 ENFORCE)


if(WIN32)
  set(LINK copy_if_different)
else(WIN32)
  set(LINK create_symlink)
endif(WIN32)

if(CMAKE_CROSSCOMPILING)
  set(PYTHON_COMPONENTS Interpreter NumPy)
else()
  set(PYTHON_COMPONENTS Interpreter Development.Module NumPy)
endif()
set(PYTHON_EXPORT_DEPENDENCY ON)
findpython(REQUIRED)

if(${NUMPY_VERSION} VERSION_LESS "1.16.0")
  set(NUMPY_WITH_BROKEN_UFUNC_SUPPORT TRUE)
endif()

if(WIN32)
  link_directories(${PYTHON_LIBRARY_DIRS})
  # # Set default Windows build paths SET(CMAKE_LIBRARY_OUTPUT_DIRECTORY
  # ${PROJECT_BINARY_DIR}/Bin CACHE PATH "Single directory for all libraries")
  # SET(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR}/Bin CACHE PATH
  # "Single directory for all executables") SET(CMAKE_ARCHIVE_OUTPUT_DIRECTORY
  # ${PROJECT_BINARY_DIR}/Bin CACHE PATH "Sing$le directory for all archives")
endif(WIN32)

# ----------------------------------------------------
# --- DEPENDENCIES -----------------------------------
# ----------------------------------------------------
add_project_dependency(Eigen3 REQUIRED PKG_CONFIG_REQUIRES "eigen3 >= 3.0.5")

set_boost_default_options()
export_boost_default_options()
find_package(Boost REQUIRED)
search_for_boost_python(REQUIRED)

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
