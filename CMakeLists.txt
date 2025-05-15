cmake_minimum_required(VERSION 3.22)

set(PROJECT_NAME bertini2)
set(PROJECT_DESCRIPTION "Implementation of the foundations of Numerical Algebraic Geometry")
set(PROJECT_URL "https://github.com/bertiniteam/b2")
set(PROJECT_USE_CMAKE_EXPORT TRUE)
set(PROJECT_USE_KEYWORD_LINK_LIBRARIES TRUE)
set(PROJECT_CUSTOM_HEADER_EXTENSION "hpp")
set(PROJECT_COMPATIBILITY_VERSION AnyNewerVersion)
# To enable jrl-cmakemodules compatibility with workspace we must define the two
# following lines
set(PROJECT_AUTO_RUN_FINALIZE FALSE)
set(PROJECT_SOURCE_DIR ${CMAKE_CURRENT_LIST_DIR})

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

function(set_standard_output_directory target)
  set_target_properties(
    ${target}
    PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR}/bin
               LIBRARY_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR}/lib
               ARCHIVE_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR}/lib)
endfunction()

# Disable -Werror on Unix for now.
set(CXX_DISABLE_WERROR True)
set(CMAKE_VERBOSE_MAKEFILE True)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# ----------------------------------------------------
# --- OPTIONS  ---------------------------------------
# Need to be set before including base.cmake
# ----------------------------------------------------
option(INSTALL_DOCUMENTATION "Generate and install the documentation" OFF)
option(SUFFIX_SO_VERSION "Suffix library name with its version" OFF)
option(BUILD_TESTING_SCIPY
       "Build the SciPy tests (scipy should be installed on the machine)" ON)

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

option(GENERATE_PYTHON_STUBS
       "Generate the Python stubs associated to the Python library" OFF)


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

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")

find_package(GMP REQUIRED)
find_package(MPFR REQUIRED)
find_package(MPC REQUIRED)
find_package(Eigen3 REQUIRED)

include_directories(${GMP_INCLUDES})
include_directories(${MPC_INCLUDES})
include_directories(${EIGEN3_INCLUDES})

set_boost_default_options()
export_boost_default_options()
find_package(Boost REQUIRED
                COMPONENTS
                    serialization
                    unit_test_framework
                    filesystem
                    graph
                    system
                    chrono
                    regex
                    timer
                    log
                    log_setup
                    thread
)
search_for_boost_python(REQUIRED)

# This was from a makemodule.am, take the lists and define them in seperate blocks with the variables they already have, then add the variable name to library_headrs
set(endgames_headers
	core/include/${PROJECT_NAME}/endgames/amp_endgame.hpp
	core/include/${PROJECT_NAME}/endgames/base_endgame.hpp
	core/include/${PROJECT_NAME}/endgames/cauchy.hpp
	core/include/${PROJECT_NAME}/endgames/config.hpp
	core/include/${PROJECT_NAME}/endgames/events.hpp
	core/include/${PROJECT_NAME}/endgames/fixed_prec_endgame.hpp
	core/include/${PROJECT_NAME}/endgames/interpolation.hpp
	core/include/${PROJECT_NAME}/endgames/observers.hpp
	core/include/${PROJECT_NAME}/endgames/powerseries.hpp
	core/include/${PROJECT_NAME}/endgames/prec_base.hpp
)

set(basics_rootinclude_headers
    core/include/${PROJECT_NAME}/have_bertini.hpp
    core/include/${PROJECT_NAME}/mpfr_extensions.hpp
    core/include/${PROJECT_NAME}/mpfr_complex.hpp
    core/include/${PROJECT_NAME}/forbid_mixed_arithmetic.hpp
    core/include/${PROJECT_NAME}/double_extensions.hpp
    core/include/${PROJECT_NAME}/random.hpp
    core/include/${PROJECT_NAME}/num_traits.hpp
    core/include/${PROJECT_NAME}/classic.hpp
    core/include/${PROJECT_NAME}/eigen_extensions.hpp
    core/include/${PROJECT_NAME}/eigen_serialization_addon.hpp
    core/include/${PROJECT_NAME}/logging.hpp
    core/include/${PROJECT_NAME}/endgames.hpp
    core/include/${PROJECT_NAME}/bertini.hpp
    core/include/${PROJECT_NAME}/version.hpp
)

set(common_headers
    core/include/${PROJECT_NAME}/common/config.hpp
    core/include/${PROJECT_NAME}/common/stream_enum.hpp
)

set(detail_headers
    core/include/${PROJECT_NAME}/detail/configured.hpp
    core/include/${PROJECT_NAME}/detail/events.hpp
    core/include/${PROJECT_NAME}/detail/visitable.hpp
    core/include/${PROJECT_NAME}/detail/visitor.hpp
    core/include/${PROJECT_NAME}/detail/observer.hpp
    core/include/${PROJECT_NAME}/detail/observable.hpp
    core/include/${PROJECT_NAME}/detail/is_template_parameter.hpp
    core/include/${PROJECT_NAME}/detail/enable_permuted_arguments.hpp
    core/include/${PROJECT_NAME}/detail/typelist.hpp
)

set(function_tree_headers
    core/include/${PROJECT_NAME}/function_tree.hpp
    core/include/${PROJECT_NAME}/function_tree/node.hpp
    core/include/${PROJECT_NAME}/function_tree/forward_declares.hpp
    core/include/${PROJECT_NAME}/function_tree/simplify.hpp
    core/include/${PROJECT_NAME}/function_tree/operators/operator.hpp
    core/include/${PROJECT_NAME}/function_tree/symbols/symbol.hpp
    core/include/${PROJECT_NAME}/function_tree/symbols/variable.hpp
    core/include/${PROJECT_NAME}/function_tree/symbols/differential.hpp
    core/include/${PROJECT_NAME}/function_tree/symbols/special_number.hpp
    core/include/${PROJECT_NAME}/function_tree/symbols/number.hpp
    core/include/${PROJECT_NAME}/function_tree/symbols/linear_product.hpp
    core/include/${PROJECT_NAME}/function_tree/roots/function.hpp
    core/include/${PROJECT_NAME}/function_tree/roots/jacobian.hpp
    core/include/${PROJECT_NAME}/function_tree/operators/arithmetic.hpp
    core/include/${PROJECT_NAME}/function_tree/operators/trig.hpp
)

set(function_tree_headers_rootinclude_HEADERS
	core/include/${PROJECT_NAME}/function_tree.hpp
)

set(settings_headers
    core/include/${PROJECT_NAME}/settings/configIni_parse.hpp
)

set(functiontreeinclude_HEADERS
	core/include/${PROJECT_NAME}/function_tree/node.hpp
	core/include/${PROJECT_NAME}/function_tree/factory.hpp
	core/include/${PROJECT_NAME}/function_tree/forward_declares.hpp
	core/include/${PROJECT_NAME}/function_tree/simplify.hpp
)

set(functiontree_operators_HEADERS
	core/include/${PROJECT_NAME}/function_tree/operators/operator.hpp
	core/include/${PROJECT_NAME}/function_tree/operators/arithmetic.hpp
	core/include/${PROJECT_NAME}/function_tree/operators/trig.hpp
)

set(functiontree_symbols_HEADERS
	core/include/${PROJECT_NAME}/function_tree/symbols/symbol.hpp
	core/include/${PROJECT_NAME}/function_tree/symbols/variable.hpp
	core/include/${PROJECT_NAME}/function_tree/symbols/differential.hpp
	core/include/${PROJECT_NAME}/function_tree/symbols/special_number.hpp
	core/include/${PROJECT_NAME}/function_tree/symbols/number.hpp
    core/include/${PROJECT_NAME}/function_tree/symbols/linear_product.hpp
)

set(functiontree_roots_HEADERS
	core/include/${PROJECT_NAME}/function_tree/roots/function.hpp
	core/include/${PROJECT_NAME}/function_tree/roots/jacobian.hpp
)

set(io_headers
    core/include/${PROJECT_NAME}/io/file_utilities.hpp
    core/include/${PROJECT_NAME}/io/generators.hpp
    core/include/${PROJECT_NAME}/io/parsing.hpp
    core/include/${PROJECT_NAME}/io/splash.hpp
)

set(io_parsing_headers
    core/include/${PROJECT_NAME}/io/parsing/classic_utilities.hpp
    core/include/${PROJECT_NAME}/io/parsing/function_parsers.hpp
    core/include/${PROJECT_NAME}/io/parsing/function_rules.hpp
    core/include/${PROJECT_NAME}/io/parsing/number_parsers.hpp
    core/include/${PROJECT_NAME}/io/parsing/number_rules.hpp
    core/include/${PROJECT_NAME}/io/parsing/qi_files.hpp
    core/include/${PROJECT_NAME}/io/parsing/settings_parsers.hpp
    core/include/${PROJECT_NAME}/io/parsing/settings_rules.hpp
    core/include/${PROJECT_NAME}/io/parsing/system_parsers.hpp
    core/include/${PROJECT_NAME}/io/parsing/system_rules.hpp
)

set(io_parsing_settings_headers
    core/include/${PROJECT_NAME}/io/parsing/settings_parsers/algorithm.hpp
    core/include/${PROJECT_NAME}/io/parsing/settings_parsers/base.hpp
    core/include/${PROJECT_NAME}/io/parsing/settings_parsers/endgames.hpp
    core/include/${PROJECT_NAME}/io/parsing/settings_parsers/tracking.hpp
)

set(nag_algorithms_headers
	core/include/${PROJECT_NAME}/nag_algorithms/midpath_check.hpp
	core/include/${PROJECT_NAME}/nag_algorithms/numerical_irreducible_decomposition.hpp
	core/include/${PROJECT_NAME}/nag_algorithms/output.hpp
	core/include/${PROJECT_NAME}/nag_algorithms/sharpen.hpp
	core/include/${PROJECT_NAME}/nag_algorithms/trace.hpp
	core/include/${PROJECT_NAME}/nag_algorithms/zero_dim_solve.hpp
)

set(nag_algorithms_common_headers
    core/include/${PROJECT_NAME}/nag_algorithms/common/algorithm_base.hpp
    core/include/${PROJECT_NAME}/nag_algorithms/common/config.hpp
    core/include/${PROJECT_NAME}/nag_algorithms/common/policies.hpp
)

set(nag_datatypes_headers
	core/include/${PROJECT_NAME}/nag_datatypes/numerical_irreducible_decomposition.hpp
	core/include/${PROJECT_NAME}/nag_datatypes/witness_set.hpp
)

set(nag_datatypes_common_headers
	core/include/${PROJECT_NAME}/nag_datatypes/common/policies.hpp
)

set(parallel_headers
    core/include/${PROJECT_NAME}/parallel/initialize_finalize.hpp
)

set(parallel_rootinclude_HEADERS
    core/include/${PROJECT_NAME}/parallel.hpp
)

set(pool_headers
    core/include/${PROJECT_NAME}/pool/pool.hpp
    core/include/${PROJECT_NAME}/pool/system.hpp
)

set(system_headers
	core/include/${PROJECT_NAME}/system/patch.hpp
	core/include/${PROJECT_NAME}/system/precon.hpp
	core/include/${PROJECT_NAME}/system/slice.hpp
	core/include/${PROJECT_NAME}/system/start_base.hpp
	core/include/${PROJECT_NAME}/system/start_systems.hpp
	core/include/${PROJECT_NAME}/system/straight_line_program.hpp
	core/include/${PROJECT_NAME}/system/system.hpp
)

set(system_start_headers
	core/include/${PROJECT_NAME}/system/start/total_degree.hpp
	core/include/${PROJECT_NAME}/system/start/mhom.hpp
	core/include/${PROJECT_NAME}/system/start/user.hpp
	core/include/${PROJECT_NAME}/system/start/utility.hpp
)

set(system_rootinclude_HEADERS
	core/include/${PROJECT_NAME}/system.hpp
)

set(trackers_HEADERS
	core/include/${PROJECT_NAME}/trackers/adaptive_precision_utilities.hpp
	core/include/${PROJECT_NAME}/trackers/amp_criteria.hpp
	core/include/${PROJECT_NAME}/trackers/amp_tracker.hpp
	core/include/${PROJECT_NAME}/trackers/base_predictor.hpp
	core/include/${PROJECT_NAME}/trackers/base_tracker.hpp
	core/include/${PROJECT_NAME}/trackers/config.hpp
	core/include/${PROJECT_NAME}/trackers/events.hpp
	core/include/${PROJECT_NAME}/trackers/explicit_predictors.hpp
	core/include/${PROJECT_NAME}/trackers/fixed_precision_tracker.hpp
	core/include/${PROJECT_NAME}/trackers/fixed_precision_utilities.hpp
	core/include/${PROJECT_NAME}/trackers/newton_correct.hpp
	core/include/${PROJECT_NAME}/trackers/newton_corrector.hpp
	core/include/${PROJECT_NAME}/trackers/observers.hpp
	core/include/${PROJECT_NAME}/trackers/ode_predictors.hpp
	core/include/${PROJECT_NAME}/trackers/predict.hpp
	core/include/${PROJECT_NAME}/trackers/step.hpp
	core/include/${PROJECT_NAME}/trackers/tracker.hpp
)

set(tracking_rootinclude_HEADERS
	core/include/${PROJECT_NAME}/tracking.hpp
)

set(BERTINI2_LIBRARY_HEADERS
    ${endgames_headers}
    ${basics_headers}
    ${common_headers}
    ${details_headers}
    ${function_tree_headers}
    ${io_headers}
    ${io_parsing_headers}
    ${io_parsing_settings_headers}
    ${nag_algorithms_headers}
    ${nag_algorithms_common_headers}
    ${nag_datatypes_headers}
    ${nag_datatypes_common_headers}
    ${parallel_headers}
    ${parallel_rootinclude_HEADERS}
    ${pool_headers}
    ${system_headers}
    ${system_start_headers}
    ${system_rootinclude_HEADERS}
    ${systeminclude_HEADERS}
    ${startinclude_HEADERS}
    ${trackers_HEADERS}
    ${tracking_header_files}
    ${tracking_rootinclude_HEADERS}
    ${trackersinclude_HEADERS}
)

set(basics_sources
    core/src/basics/random.cpp
    core/src/basics/have_bertini.cpp
)

set(function_tree_sources
    core/src/function_tree/node.cpp
    core/src/function_tree/simplify.cpp
    core/src/function_tree/operators/arithmetic.cpp
    core/src/function_tree/operators/trig.cpp
    core/src/function_tree/linear_product.cpp
    core/src/function_tree/operators/operator.cpp
    core/src/function_tree/symbols/special_number.cpp
    core/src/function_tree/symbols/differential.cpp
    core/src/function_tree/symbols/symbol.cpp
    core/src/function_tree/symbols/variable.cpp
    core/src/function_tree/symbols/number.cpp
    core/src/function_tree/roots/jacobian.cpp
    core/src/function_tree/roots/function.cpp
)

set(parallel_sources
    core/src/parallel/parallel.cpp
    core/src/parallel/initialize_finalize.cpp
)

set(system_source_files
    core/src/system/precon.cpp
    core/src/system/slice.cpp
    core/src/system/start_base.cpp
    core/src/system/system.cpp
    core/src/system/straight_line_program.cpp
    core/src/system/start/total_degree.cpp
    core/src/system/start/mhom.cpp
    core/src/system/start/user.cpp
)

set(tracking_source_files
    core/src/tracking/explicit_predictors.cpp
)

set(BERTINI2_LIBRARY_SOURCES
    ${basics_sources}
    ${libbertini2_la_SOURCES}
    ${function_tree_sources}
    ${parallel_sources}
    ${system_source_files}
    ${tracking_source_files}
)

set(BERTINI2_EXE_SOURCES
    core/src/blackbox/bertini.cpp
    core/src/blackbox/main_mode_switch.cpp
    core/src/blackbox/argc_argv.cpp
)

set(BERTINI2_EXE_HEADERS
    core/include/${PROJECT_NAME}/blackbox/main_mode_switch.hpp
    core/include/${PROJECT_NAME}/blackbox/argc_argv.hpp
    core/include/${PROJECT_NAME}/blackbox/config.hpp
    core/include/${PROJECT_NAME}/blackbox/algorithm_builder.hpp
    core/include/${PROJECT_NAME}/blackbox/global_configs.hpp
    core/include/${PROJECT_NAME}/blackbox/switches_zerodim.hpp
    core/include/${PROJECT_NAME}/blackbox/user_homotopy.hpp
)

include_directories(${CMAKE_CURRENT_SOURCE_DIR}/core/include)

#add_library(${PROJECT_NAME} SHARED ${BERTINI2_LIBRARY_SOURCES} ${BERTINI2_LIBRARY_HEADERS})
#add_library(${PROJECT_NAME}::${PROJECT_NAME} ALIAS ${PROJECT_NAME})
add_library(${PROJECT_NAME} SHARED ${BERTINI2_LIBRARY_SOURCES} ${BERTINI2_LIBRARY_HEADERS})
add_library(${PROJECT_NAME}::${PROJECT_NAME} ALIAS ${PROJECT_NAME})
set_standard_output_directory(${PROJECT_NAME})
target_include_directories(
  ${PROJECT_NAME} SYSTEM
  PUBLIC $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}/include>
         $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
         $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>)


modernize_target_link_libraries(
  ${PROJECT_NAME}
  SCOPE
  PUBLIC
  TARGETS
  ${GMP_LIBRARIES}
  INCLUDE_DIRS
  ${GMP_INCLUDE_DIR})

modernize_target_link_libraries(
  ${PROJECT_NAME}
  SCOPE
  PUBLIC
  TARGETS
  ${MPFR_LIBRARIES}
  INCLUDE_DIRS
  ${MPFR_INCLUDE_DIR})

modernize_target_link_libraries(
  ${PROJECT_NAME}
  SCOPE
  PUBLIC
  TARGETS
  Eigen3::Eigen
  INCLUDE_DIRS
  ${EIGEN3_INCLUDE_DIR})

modernize_target_link_libraries(
  ${PROJECT_NAME}
  SCOPE
  PUBLIC
  TARGETS
  Python${PYTHON_VERSION_MAJOR}::NumPy
  INCLUDE_DIRS
  ${NUMPY_INCLUDE_DIRS}
  ${PYTHON_INCLUDE_DIR})

if(SUFFIX_SO_VERSION)
  set_target_properties(bertini2 PROPERTIES SOVERSION ${PROJECT_VERSION})
endif(SUFFIX_SO_VERSION)

if(NOT WIN32)
  target_compile_options(
    ${PROJECT_NAME} PRIVATE $<$<CXX_COMPILER_ID:MSVC>:-bigobj -MP>
                            "-Wno-conversion")
else()
  target_compile_options(${PROJECT_NAME}
                         PRIVATE $<$<CXX_COMPILER_ID:MSVC>:-bigobj -MP>)
  target_compile_definitions(${PROJECT_NAME} PUBLIC "HAVE_SNPRINTF")
endif()

target_link_boost_python(${PROJECT_NAME} PUBLIC)
install(
  TARGETS ${PROJECT_NAME}
  EXPORT ${TARGETS_EXPORT_NAME}
  PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
  INCLUDES
  DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
  LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
  ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
  RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})

add_header_group(${PROJECT_NAME}_HEADERS)
add_source_group(${PROJECT_NAME}_SOURCES)

add_executable(bertini2_exe)
set_property(TARGET bertini2_exe PROPERTY OUTPUT_NAME ${PROJECT_NAME})

target_sources(bertini2_exe PUBLIC ${BERTINI2_EXE_SOURCES} ${BERTINI2_EXE_HEADERS})
target_link_libraries(bertini2_exe ${Boost_LIBRARIES} ${PROJECT_NAME})

# ----------------------------------------------------
# --- PYTHON LIBRARY ---------------------------------
# ----------------------------------------------------
#add_subdirectory(python_bindings)
add_subdirectory(python)

# ----------------------------------------------------
# --- UNIT TEST --------------------------------------
# ----------------------------------------------------
add_subdirectory(unittest)

pkg_config_append_libs(${PROJECT_NAME})
pkg_config_append_cflags("-I${PYTHON_INCLUDE_DIRS}")
pkg_config_append_cflags("-I${NUMPY_INCLUDE_DIRS}")
pkg_config_append_boost_libs(${BOOST_COMPONENTS})

setup_project_finalize()


############################
# the core builds a library and an executable depending on that library
#

#add_library(bertini2 SHARED ${${PROJECT_NAME}_SOURCES}
#                            ${${PROJECT_NAME}_HEADERS})
#add_library(${PROJECT_NAME}::${PROJECT_NAME} ALIAS ${PROJECT_NAME})
#set_standard_output_directory(${PROJECT_NAME})

#set_standard_output_directory(${PROJECT_NAME})

#if(NOT WIN32)
#  target_compile_options(
#    ${PROJECT_NAME} PRIVATE $<$<CXX_COMPILER_ID:MSVC>:-bigobj -MP>
#                            "-Wno-conversion")
#else()
#  target_compile_options(${PROJECT_NAME}
#                         PRIVATE $<$<CXX_COMPILER_ID:MSVC>:-bigobj -MP>)
#  target_compile_definitions(${PROJECT_NAME} PUBLIC "HAVE_SNPRINTF")
#endif()

#target_link_boost_python(${PROJECT_NAME} PUBLIC)
#add_subdirectory(core)

#add_executable(bertini2_exe)
#set_property(TARGET bertini2_exe PROPERTY OUTPUT_NAME bertini2)






###########
# next, in `python_bindings`, build a shared python library, and a pure-python library that wraps around that.
#


#python_add_library(_pybertini MODULE WITH_SOABI)

#add_subdirectory(python_bindings)



###########
# finally, the pure-python part of the project.
#

#add_subdirectory(python)
