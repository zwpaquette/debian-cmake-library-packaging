cmake_minimum_required(VERSION 3.10)
project(libcalc VERSION 1.2.3 LANGUAGES C)

# Create shared library
add_library(calc SHARED
    src/calc.c
)

# Set SONAME version
set_target_properties(calc PROPERTIES
    VERSION ${PROJECT_VERSION}
    SOVERSION 1
    PUBLIC_HEADER include/calc.h
)

# Include directories
target_include_directories(calc PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>
)

# Install library
install(TARGETS calc
    LIBRARY DESTINATION lib
    PUBLIC_HEADER DESTINATION include
)

# Create and install pkg-config file
configure_file(libcalc.pc.in libcalc.pc @ONLY)
install(FILES ${CMAKE_BINARY_DIR}/libcalc.pc
    DESTINATION lib/pkgconfig
)
