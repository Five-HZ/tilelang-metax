# todo: support prebuilt tvm

set(TVM_BUILD_FROM_SOURCE TRUE)
set(TVM_SOURCE ${CMAKE_SOURCE_DIR}/3rdparty/tvm)

if(DEFINED ENV{TVM_ROOT})
  if(EXISTS $ENV{TVM_ROOT}/cmake/config.cmake)
    set(TVM_SOURCE $ENV{TVM_ROOT})
    message(STATUS "Using TVM_ROOT from environment variable: ${TVM_SOURCE}")
  endif()
endif()

message(STATUS "Using TVM source: ${TVM_SOURCE}")

message(STATUS "Checking and switching TVM to tile-ai/tilelang_main")
execute_process(
  COMMAND git merge-base --is-ancestor tileai/tilelang_main HEAD
  WORKING_DIRECTORY ${TVM_SOURCE}
  RESULT_VARIABLE MERGE_CHECK_RESULT
  OUTPUT_QUIET
  ERROR_VARIABLE MERGE_CHECK_ERROR
)
if(NOT MERGE_CHECK_ERROR STREQUAL "" OR NOT MERGE_CHECK_RESULT EQUAL 0)
  execute_process(
    COMMAND git remote get-url tileai
    WORKING_DIRECTORY ${TVM_SOURCE}
    RESULT_VARIABLE TILEAI_REMOTE_EXIST
    OUTPUT_QUIET
    ERROR_VARIABLE REMOTE_CHECK_ERROR
  )
  if(NOT REMOTE_CHECK_ERROR STREQUAL "" OR NOT TILEAI_REMOTE_EXIST EQUAL 0)
    execute_process(
      COMMAND git remote add tileai http://github.com/tile-ai/tvm.git
      WORKING_DIRECTORY ${TVM_SOURCE}
      COMMAND_ERROR_IS_FATAL ANY
    )
  endif()
  execute_process(
    COMMAND git fetch --no-recurse-submodules tileai tilelang_main
    WORKING_DIRECTORY ${TVM_SOURCE}
    COMMAND_ERROR_IS_FATAL ANY
  )
  execute_process(
    COMMAND git merge --allow-unrelated-histories -Xours tileai/tilelang_main
    WORKING_DIRECTORY ${TVM_SOURCE}
    COMMAND_ERROR_IS_FATAL ANY
  )
else()
  message(STATUS "Already merged tileai/tilelang_main, skip all operations")
endif()

execute_process(
  COMMAND git log --oneline -1
  WORKING_DIRECTORY ${TVM_SOURCE}
  OUTPUT_VARIABLE TVM_COMMIT
  OUTPUT_STRIP_TRAILING_WHITESPACE
  ERROR_QUIET
)
message(STATUS "TVM current commit: ${TVM_COMMIT}")

set(TVM_INCLUDES
  ${TVM_SOURCE}/include
  ${TVM_SOURCE}/src
  ${TVM_SOURCE}/3rdparty/dlpack/include
  ${TVM_SOURCE}/3rdparty/dmlc-core/include
)

if(EXISTS ${TVM_SOURCE}/ffi/include)
  list(APPEND TVM_INCLUDES ${TVM_SOURCE}/ffi/include)
elseif(EXISTS ${TVM_SOURCE}/3rdparty/tvm-ffi/include)
  list(APPEND TVM_INCLUDES ${TVM_SOURCE}/3rdparty/tvm-ffi/include)
endif()

if(EXISTS ${TVM_SOURCE}/3rdparty/tvm-ffi/3rdparty/dlpack/include)
  list(APPEND TVM_INCLUDES ${TVM_SOURCE}/3rdparty/tvm-ffi/3rdparty/dlpack/include)
endif()
