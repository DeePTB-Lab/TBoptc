cmake_minimum_required(VERSION 3.17...3.26)

option(BUILD_FORTRAN "Build Fortran extensions" ON)
option(USE_OPENMP "Use OpenMP" ON)

if(BUILD_FORTRAN)
    # Detect OS and architecture
    if(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
        set(MACOS TRUE)
    elseif(CMAKE_SYSTEM_NAME STREQUAL "Linux")
        set(LINUX TRUE)
    endif()

    # Find compilers
    find_program(ICX_COMPILER icx)
    find_program(IFX_COMPILER ifx)
    find_program(GCC_COMPILER gcc)
    find_program(GFORTRAN_COMPILER gfortran)

    # Set compilers and flags
    if(ICX_COMPILER AND IFX_COMPILER)
        set(CMAKE_C_COMPILER ${ICX_COMPILER})
        set(CMAKE_Fortran_COMPILER ${IFX_COMPILER})
        set(CMAKE_Fortran_FLAGS "-fpp -O3 -xHost -qopenmp -ipo -heap-arrays 32 -unroll -fma -align")
        set(CMAKE_C_FLAGS  "-O3 -xHost -ipo -fma -align")
    elseif(GCC_COMPILER AND GFORTRAN_COMPILER)
        set(CMAKE_C_COMPILER ${GCC_COMPILER})
        set(CMAKE_Fortran_COMPILER ${GFORTRAN_COMPILER})
        set(CMAKE_C_FLAGS "-O3")
        set(CMAKE_Fortran_FLAGS "-O3")
    else()
        message(FATAL_ERROR "Could not find a compatible C and Fortran compiler.")
    endif()

    project(${SKBUILD_PROJECT_NAME} LANGUAGES C Fortran)
    
    if(USE_OPENMP)
        find_package(OpenMP)
        if(OpenMP_FOUND)
            message(STATUS "OpenMP found, enabling OpenMP support.")
            set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
            set(CMAKE_Fortran_FLAGS "${CMAKE_Fortran_FLAGS} ${OpenMP_Fortran_FLAGS}")
        else()
            message(WARNING "OpenMP not found, disabling OpenMP support.")
        endif()
    endif()

    # Search for packages and commands
    find_package(Python COMPONENTS Interpreter Development.Module NumPy REQUIRED)

    #----------------------------- Fortran extension ------------------------------#
    # Define the fortranobject
    execute_process(
      COMMAND "${Python_EXECUTABLE}" -c
              "import numpy.f2py; print(numpy.f2py.get_include())"
      OUTPUT_VARIABLE F2PY_INCLUDE_DIR
      OUTPUT_STRIP_TRAILING_WHITESPACE)
    add_library(fortranobject OBJECT "${F2PY_INCLUDE_DIR}/fortranobject.c")
    target_link_libraries(fortranobject PUBLIC Python::NumPy)
    target_include_directories(fortranobject PUBLIC "${F2PY_INCLUDE_DIR}")
    set_property(TARGET fortranobject PROPERTY POSITION_INDEPENDENT_CODE ON)

    # Set the Fortran source file path
    set(FORTRAN_SOURCE "${CMAKE_CURRENT_SOURCE_DIR}/tboptc/fortran/ac_cond.f90")

    # Generate the interface
    add_custom_command(
      OUTPUT "${CMAKE_CURRENT_BINARY_DIR}/ac_condmodule.c"
      DEPENDS "${FORTRAN_SOURCE}"
      COMMAND "${Python_EXECUTABLE}" -m numpy.f2py "${FORTRAN_SOURCE}"
              -m ac_cond --lower
      WORKING_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}"
      VERBATIM
    )

    # Define the python module
    python_add_library(ac_cond MODULE
                       "${CMAKE_CURRENT_BINARY_DIR}/ac_condmodule.c"
                       "${FORTRAN_SOURCE}"
                       WITH_SOABI)
    target_link_libraries(ac_cond PRIVATE fortranobject)
    if(OpenMP_Fortran_FOUND)
      target_link_libraries(ac_cond PRIVATE OpenMP::OpenMP_Fortran)
    endif()

    install(TARGETS ac_cond DESTINATION ./tboptc/fortran)
else()
    project(${SKBUILD_PROJECT_NAME})
    message(STATUS "Fortran extensions are disabled")
endif()
