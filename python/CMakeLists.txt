# --- LIBRARY --- #
set(PYWRAP ${PROJECT_NAME}_pywrap)
set(PYWRAP
    ${PYWRAP}
    PARENT_SCOPE)

make_directory("${${PROJECT_NAME}_BINARY_DIR}/python/bertini")
include(${JRL_CMAKE_MODULES}/python-helpers.cmake)
include("${JRL_CMAKE_MODULES}/stubs.cmake")

add_custom_target(${PROJECT_NAME}_python)
set_target_properties(${PROJECT_NAME}_python
                      PROPERTIES EXCLUDE_FROM_DEFAULT_BUILD True)

set(PYBERTINI_HEADERS
    include/bertini_python.hpp
    include/eigenpy_interaction.hpp
    include/function_tree_export.hpp
    include/mpfr_export.hpp
    include/random_export.hpp
    include/node_export.hpp
    include/symbol_export.hpp
    include/operator_export.hpp
    include/root_export.hpp
    include/system_export.hpp
    include/tracker_export.hpp
    include/endgame_export.hpp
    include/parser_export.hpp
    include/generic_observer.hpp
    include/generic_observable.hpp
    include/tracker_observers.hpp
    include/endgame_observers.hpp
    include/detail.hpp
    include/logging.hpp
)

set(PYBERTINI_SOURCES
    src/eigenpy_interaction.cpp
    src/logging.cpp
    src/detail.cpp
    src/containers.cpp
    src/tracker_export.cpp
    src/endgame_export.cpp
    src/random_export.cpp
    src/mpfr_export.cpp
    src/node_export.cpp
    src/symbol_export.cpp
    src/operator_export.cpp
    src/root_export.cpp
    src/system_export.cpp
    src/parser_export.cpp
    src/generic_observable.cpp
    src/generic_observer.cpp
    src/tracker_observers.cpp
    src/endgame_observers.cpp
    src/zero_dim_export.cpp
    src/bertini_python.cpp
)

add_library(${PYWRAP} MODULE ${PYBERTINI_SOURCES} ${PYBERTINI_HEADERS})
add_dependencies(${PROJECT_NAME}_python ${PYWRAP})
target_link_libraries(${PYWRAP} PUBLIC ${Boost_LIBRARIES} ${PROJECT_NAME})

python_build_get_target(python_build_target)
add_dependencies(${PYWRAP} ${python_build_target})

# BOOST_PYTHON_MEMBER_FUNCTION_OVERLOADS spews conversion warnings from int to
# long unsigned int. Unfortunately, using literals does not work in a macro. As
# such, this turns them off for the entire wrapper:
if(NOT WIN32)
  target_compile_options(${PYWRAP} PRIVATE "-Wno-conversion")
endif()
if(IS_ABSOLUTE ${PYTHON_SITELIB})
  set(ABSOLUTE_PYTHON_SITELIB ${PYTHON_SITELIB})
else()
  set(ABSOLUTE_PYTHON_SITELIB ${CMAKE_INSTALL_PREFIX}/${PYTHON_SITELIB})
endif()
set(${PYWRAP}_INSTALL_DIR ${ABSOLUTE_PYTHON_SITELIB}/bertini)

set_target_properties(
  ${PYWRAP}
  PROPERTIES PREFIX ""
             SUFFIX ${PYTHON_EXT_SUFFIX}
             LIBRARY_OUTPUT_DIRECTORY
             "${PROJECT_BINARY_DIR}/python/bertini"
             LIBRARY_OUTPUT_DIRECTORY_<CONFIG>
             "${PROJECT_BINARY_DIR}/python/bertini"
             RUNTIME_OUTPUT_DIRECTORY
             "${PROJECT_BINARY_DIR}/python/bertini"
             RUNTIME_OUTPUT_DIRECTORY_<CONFIG>
             "${PROJECT_BINARY_DIR}/python/bertini")

if(UNIX)
  get_relative_rpath(${${PYWRAP}_INSTALL_DIR} ${PYWRAP}_INSTALL_RPATH)
  set_target_properties(${PYWRAP} PROPERTIES INSTALL_RPATH
                                             "${${PYWRAP}_INSTALL_RPATH}")
endif()

install(TARGETS ${PYWRAP} DESTINATION ${${PYWRAP}_INSTALL_DIR})

# --- GENERATE STUBS
if(GENERATE_PYTHON_STUBS)
  load_stubgen()

  # Set PYWRAP and PROJECT_NAME as stubs dependencies PROJECT_NAME is mandatory
  # (even if it's a PYWRAP dependency) to find PROJECT_NAME name DLL on windows
  generate_stubs(${CMAKE_CURRENT_BINARY_DIR} bertini
                 ${ABSOLUTE_PYTHON_SITELIB} ${PYWRAP} bertini)
endif(GENERATE_PYTHON_STUBS)

# --- INSTALL SCRIPTS
set(PYTHON_FILES __init__.py _version.py windows_dll_manager.py)
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/include)
foreach(python ${PYTHON_FILES})
  python_build(bertini ${python})
  install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/bertini/${python}"
          DESTINATION ${${PYWRAP}_INSTALL_DIR})
endforeach(python)
