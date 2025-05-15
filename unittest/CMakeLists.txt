#
# Copyright (c) 2014-2019 CNRS Copyright (c) 2018-2024 INRIA
#
find_package(GMP REQUIRED)
find_package(MPFR REQUIRED)
find_package(MPC REQUIRED)

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
find_package(Eigen3 3.3 REQUIRED NO_MODULE)

function(ADD_LIB_UNIT_TEST test)
  create_ctest_build_tests_target()
  set(test_target ${PROJECT_NAME}-${test})

  if(BUILD_TESTING)
    add_library(${test_target} SHARED "${test}.cpp")
  else()
    add_library(${test_target} SHARED EXCLUDE_FROM_ALL "${test}.cpp")
  endif()
  set_standard_output_directory(${test_target})

  target_link_libraries(${test_target} ${MPC_LIBRARIES}
  	${MPFR_LIBRARIES} ${GMP_LIBRARIES} ${Boost_LIBRARIES} Eigen3::Eigen ${PROJECT_NAME})

  set_target_properties(
    ${test_target}
    PROPERTIES PREFIX ""
               LIBRARY_OUTPUT_NAME ${test}
               RUNTIME_OUTPUT_NAME ${test})

  set_target_properties(${test_target} PROPERTIES SUFFIX ${PYTHON_EXT_SUFFIX})

  add_test(
    NAME ${test_target}
    COMMAND ${PYTHON_EXECUTABLE} -c "import ${test}"
    WORKING_DIRECTORY $<TARGET_FILE_DIR:${test_target}>)

  add_dependencies(build_tests ${test_target})
  if(NOT BUILD_TESTING)
    set_tests_properties(${test_target} PROPERTIES DEPENDS ctest_build_tests)
  endif(NOT BUILD_TESTING)
endfunction()

add_dependencies(build_tests ${PYWRAP})
#add_lib_unit_test(matrix)


function(add_python_lib_unit_test name source)
  set(test_target ${PROJECT_NAME}-${name})
  add_python_unit_test(${test_target} ${source} "lib" "bin")
endfunction()


add_python_lib_unit_test("py-matrix" "unittest/python/test_matrix.py")
