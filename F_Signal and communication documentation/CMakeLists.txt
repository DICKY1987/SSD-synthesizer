cmake_minimum_required(VERSION 3.10)
project(MQL4_DLL_SocketBridge)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Set output directory
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)

# Windows-specific settings
if(WIN32)
    # Set Windows target version
    add_definitions(-D_WIN32_WINNT=0x0601)
    
    # Set DLL export definitions
    add_definitions(-DBUILDING_DLL)
endif()

# Source files
set(SOURCES
    MQL4_DLL_SocketBridge.cpp
    MQL4_DLL_SocketBridge.h
)

# Create the DLL
add_library(MQL4_DLL_SocketBridge SHARED ${SOURCES})

# Link Windows socket library
if(WIN32)
    target_link_libraries(MQL4_DLL_SocketBridge ws2_32)
endif()

# Set DLL properties
set_target_properties(MQL4_DLL_SocketBridge PROPERTIES
    OUTPUT_NAME "MQL4_DLL_SocketBridge"
    PREFIX ""
)

# Install target
install(TARGETS MQL4_DLL_SocketBridge
    RUNTIME DESTINATION bin
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
)