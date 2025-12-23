#!/bin/bash
# CANARY_STRING_PLACEHOLDER

set -e  # Exit immediately if any command fails

echo "=========================================="
echo "Building Debian Packages for C Library"
echo "=========================================="

# Step 1: Navigate to library directory
cd /app/libcalc

# Step 2: Create debian directory structure
echo "Step 1: Creating debian/ directory structure..."
mkdir -p debian/source

# Step 3: Create debian/control file
echo "Step 2: Creating debian/control..."
cat > debian/control << 'EOF'
Source: libcalc
Section: libs
Priority: optional
Maintainer: Anonymous <anonymous@example.com>
Build-Depends: debhelper (>= 13), cmake (>= 3.10)
Standards-Version: 4.6.0

Package: libcalc1
Architecture: any
Depends: ${shlibs:Depends}, ${misc:Depends}
Description: Simple calculation library - runtime
 A simple C library providing basic calculation functions
 like addition and multiplication.
 .
 This package contains the shared library.

Package: libcalc-dev
Section: libdevel
Architecture: any
Depends: libcalc1 (= ${binary:Version}), ${misc:Depends}
Description: Simple calculation library - development files
 A simple C library providing basic calculation functions
 like addition and multiplication.
 .
 This package contains the development files (headers and pkg-config).
EOF

# Step 4: Create debian/rules file
echo "Step 3: Creating debian/rules..."
cat > debian/rules << 'EOF'
#!/usr/bin/make -f

%:
	dh $@ --buildsystem=cmake

override_dh_auto_configure:
	dh_auto_configure -- -DCMAKE_INSTALL_PREFIX=/usr

override_dh_auto_install:
	dh_auto_install --destdir=debian/tmp
EOF
chmod +x debian/rules

# Step 5: Create debian/changelog
echo "Step 4: Creating debian/changelog..."
cat > debian/changelog << 'EOF'
libcalc (1.2.3-1) unstable; urgency=medium

  * Initial release

 -- Anonymous <anonymous@example.com>  Mon, 23 Dec 2024 00:00:00 +0000
EOF

# Step 6: Create debian/compat
echo "Step 5: Creating debian/compat..."
echo "13" > debian/compat

# Step 7: Create debian/libcalc1.install (runtime package)
echo "Step 6: Creating package install files..."
cat > debian/libcalc1.install << 'EOF'
usr/lib/*/libcalc.so.*
EOF

# Step 8: Create debian/libcalc-dev.install (dev package)
cat > debian/libcalc-dev.install << 'EOF'
usr/include/*
usr/lib/*/libcalc.so
usr/lib/*/pkgconfig/*
EOF

# Step 9: Create debian/source/format
cat > debian/source/format << 'EOF'
3.0 (native)
EOF

# Step 10: Build the packages
echo "Step 7: Building Debian packages with dpkg-buildpackage..."
dpkg-buildpackage -us -uc -b

# Step 11: Move .deb files to /app
echo "Step 8: Moving .deb files to /app..."
mv ../libcalc1_*.deb /app/
mv ../libcalc-dev_*.deb /app/

# Step 12: Install the packages
echo "Step 9: Installing Debian packages..."
dpkg -i /app/libcalc1_*.deb
dpkg -i /app/libcalc-dev_*.deb

# Step 13: Verify installation with ldconfig
echo "Step 10: Running ldconfig..."
ldconfig

# Step 14: Compile consumer using pkg-config
echo "Step 11: Compiling consumer application..."
cd /app/consumer

# Get flags from pkg-config
CFLAGS=$(pkg-config --cflags libcalc)
LIBS=$(pkg-config --libs libcalc)

echo "  pkg-config --cflags: $CFLAGS"
echo "  pkg-config --libs: $LIBS"

# Compile the consumer
gcc $CFLAGS main.c $LIBS -o consumer

# Step 15: Run the consumer and save output
echo "Step 12: Running consumer application..."
./consumer | tee /app/verification_output.txt

# Step 16: Verify output exists
if [ -f /app/verification_output.txt ]; then
    echo "✓ Created /app/verification_output.txt"
    echo "Contents:"
    cat /app/verification_output.txt
else
    echo "✗ Failed to create verification output"
    exit 1
fi

echo "=========================================="
echo "✓ Task completed successfully!"
echo "✓ Debian packages built and installed"
echo "✓ Consumer compiled and verified"
echo "=========================================="
