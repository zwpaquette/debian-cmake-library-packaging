# Package C Library into Debian Packages with CMake

Your task is to package a small C library built with CMake into proper Debian packages: a versioned runtime shared library package and a development package, then verify the installation by building a consumer application.

## Problem Description

A simple C library with CMake build system exists at `/app/libcalc`. You must create proper Debian packaging for this library following Debian policy, build the packages using `dpkg-buildpackage`, install them, and verify functionality by compiling a test consumer program.

## Requirements

Your solution must:

1. **Create Debian packaging files** in `/app/libcalc/debian/` directory including:
   - `control` file defining two binary packages: runtime library (e.g., `libcalc1`) and dev package (`libcalc-dev`)
   - `rules` file using debhelper to build with CMake
   - `changelog` file with proper Debian format
   - `compat` file specifying debhelper compatibility level
   - Any other required packaging files

2. **Ensure correct library versioning**:
   - Runtime package name must include SONAME version (e.g., `libcalc1` for SONAME 1)
   - Shared library must have proper SONAME set in CMake
   - Library files installed to `/usr/lib/` or `/usr/lib/x86_64-linux-gnu/`

3. **Create proper package splits**:
   - **Runtime package** (`libcalc1`): Contains only the shared library (`.so.X.Y.Z` and `.so.X` symlink)
   - **Dev package** (`libcalc-dev`): Contains headers, unversioned `.so` symlink, and pkg-config `.pc` file

4. **Build packages** using `dpkg-buildpackage` in `/app/libcalc/`

5. **Install both packages** using `dpkg -i` from the generated `.deb` files

6. **Verify installation** by:
   - Compiling `/app/consumer/main.c` that uses the library
   - Using `pkg-config` to get compiler and linker flags
   - Running the compiled consumer binary successfully
   - Writing the consumer binary output to `/app/verification_output.txt`

## Constraints

- Must use debhelper and follow Debian packaging conventions
- Must use `dpkg-buildpackage` (not manual ar/tar creation)
- Library must be properly versioned with SONAME
- pkg-config file must be included and functional
- Consumer must compile and link using `pkg-config --cflags --libs`
- All files must follow Debian filesystem hierarchy standards

## Files

- Input: `/app/libcalc/` (source directory with C library and CMakeLists.txt)
- Input: `/app/consumer/main.c` (test consumer program)
- Output: `/app/libcalc/debian/*` (all Debian packaging files)
- Output: `/app/*.deb` (built Debian packages)
- Output: `/app/consumer/consumer` (compiled consumer binary)
- Output: `/app/verification_output.txt` (output from running consumer)

## Success Criteria

1. Debian packages build successfully without errors
2. Two separate `.deb` files are created (runtime and dev packages)
3. Runtime package contains only shared library files
4. Dev package contains headers, unversioned symlink, and pkg-config file
5. Both packages install successfully with `dpkg -i`
6. Consumer compiles successfully using pkg-config
7. Consumer runs and produces expected output
8. `/app/verification_output.txt` contains the consumer program output
