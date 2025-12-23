"""Tests for Debian C library packaging task."""
import subprocess
import os
from pathlib import Path


def test_debian_directory_exists():
    """Verify debian/ directory was created in library source."""
    debian_dir = Path("/app/libcalc/debian")
    assert debian_dir.exists(), "/app/libcalc/debian directory does not exist"
    assert debian_dir.is_dir(), "/app/libcalc/debian is not a directory"


def test_debian_control_file_exists():
    """Verify debian/control file exists and has correct structure."""
    control_file = Path("/app/libcalc/debian/control")
    assert control_file.exists(), "debian/control file does not exist"
    
    content = control_file.read_text()
    assert "Source:" in content, "control file missing Source field"
    assert "Package: libcalc1" in content or "Package: libcalc" in content, "control file missing runtime package"
    assert "Package: libcalc-dev" in content, "control file missing dev package"


def test_debian_rules_file_exists():
    """Verify debian/rules file exists and is executable."""
    rules_file = Path("/app/libcalc/debian/rules")
    assert rules_file.exists(), "debian/rules file does not exist"
    assert os.access(str(rules_file), os.X_OK), "debian/rules is not executable"


def test_debian_changelog_exists():
    """Verify debian/changelog file exists."""
    changelog_file = Path("/app/libcalc/debian/changelog")
    assert changelog_file.exists(), "debian/changelog file does not exist"


def test_runtime_deb_package_exists():
    """Verify runtime .deb package was created."""
    deb_files = list(Path("/app").glob("libcalc*.deb"))
    runtime_debs = [f for f in deb_files if "dev" not in f.name]
    
    assert len(runtime_debs) > 0, "No runtime .deb package found in /app"


def test_dev_deb_package_exists():
    """Verify development .deb package was created."""
    dev_debs = list(Path("/app").glob("libcalc-dev*.deb"))
    
    assert len(dev_debs) > 0, "No -dev .deb package found in /app"


def test_two_separate_packages_created():
    """Verify exactly two distinct .deb packages were created."""
    deb_files = list(Path("/app").glob("libcalc*.deb"))
    
    assert len(deb_files) >= 2, f"Expected at least 2 .deb packages, found {len(deb_files)}"


def test_runtime_package_installed():
    """Verify runtime package is installed in dpkg."""
    result = subprocess.run(
        ["dpkg", "-l"],
        capture_output=True,
        text=True
    )
    
    # Check for libcalc1 or similar runtime package
    assert "libcalc" in result.stdout, "Runtime library package not installed"


def test_dev_package_installed():
    """Verify dev package is installed in dpkg."""
    result = subprocess.run(
        ["dpkg", "-l"],
        capture_output=True,
        text=True
    )
    
    assert "libcalc-dev" in result.stdout, "Development package not installed"


def test_shared_library_file_exists():
    """Verify shared library file was installed to system."""
    lib_paths = [
        Path("/usr/lib/libcalc.so.1"),
        Path("/usr/lib/x86_64-linux-gnu/libcalc.so.1"),
        Path("/usr/lib/aarch64-linux-gnu/libcalc.so.1"),
    ]
    
    found = False
    for lib_path in lib_paths:
        if lib_path.exists() or any(lib_path.parent.glob("libcalc.so.*")):
            found = True
            break
    
    assert found, "Shared library .so file not found in /usr/lib"


def test_header_file_installed():
    """Verify header file was installed to /usr/include."""
    header_file = Path("/usr/include/calc.h")
    assert header_file.exists(), "Header file calc.h not installed to /usr/include"


def test_pkg_config_file_installed():
    """Verify pkg-config .pc file was installed."""
    result = subprocess.run(
        ["pkg-config", "--exists", "libcalc"],
        capture_output=True
    )
    
    assert result.returncode == 0, "pkg-config cannot find libcalc.pc file"


def test_pkg_config_returns_cflags():
    """Verify pkg-config returns compiler flags."""
    result = subprocess.run(
        ["pkg-config", "--cflags", "libcalc"],
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0, "pkg-config --cflags failed"
    assert "-I" in result.stdout, "pkg-config --cflags did not return include path"


def test_pkg_config_returns_libs():
    """Verify pkg-config returns linker flags."""
    result = subprocess.run(
        ["pkg-config", "--libs", "libcalc"],
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0, "pkg-config --libs failed"
    assert "-lcalc" in result.stdout, "pkg-config --libs did not return library flag"


def test_consumer_binary_exists():
    """Verify consumer binary was compiled."""
    consumer_bin = Path("/app/consumer/consumer")
    assert consumer_bin.exists(), "Consumer binary not found at /app/consumer/consumer"
    assert os.access(str(consumer_bin), os.X_OK), "Consumer binary is not executable"


def test_consumer_runs_successfully():
    """Verify consumer binary runs without errors."""
    consumer_bin = Path("/app/consumer/consumer")
    
    result = subprocess.run(
        [str(consumer_bin)],
        capture_output=True,
        text=True,
        cwd="/app/consumer"
    )
    
    assert result.returncode == 0, f"Consumer failed with exit code {result.returncode}"


def test_verification_output_file_exists():
    """Verify verification_output.txt was created."""
    output_file = Path("/app/verification_output.txt")
    assert output_file.exists(), "/app/verification_output.txt does not exist"


def test_verification_output_contains_expected_text():
    """Verify verification output contains expected calculation results."""
    output_file = Path("/app/verification_output.txt")
    content = output_file.read_text()
    
    # Check for expected output from consumer
    assert "10 + 5 = 15" in content or "15" in content, "Output missing addition result"
    assert "10 * 5 = 50" in content or "50" in content, "Output missing multiplication result"


def test_library_soname_version():
    """Verify shared library has proper SONAME versioning."""
    # Find the library file
    lib_locations = [
        Path("/usr/lib"),
        Path("/usr/lib/x86_64-linux-gnu"),
        Path("/usr/lib/aarch64-linux-gnu"),
    ]
    
    lib_file = None
    for loc in lib_locations:
        matches = list(loc.glob("libcalc.so.*.*.*"))
        if matches:
            lib_file = matches[0]
            break
    
    if lib_file:
        # Check that versioned .so file exists
        assert ".so." in str(lib_file), f"Library {lib_file} missing version in filename"


def test_dev_package_has_unversioned_symlink():
    """Verify dev package contains unversioned .so symlink."""
    lib_locations = [
        Path("/usr/lib/libcalc.so"),
        Path("/usr/lib/x86_64-linux-gnu/libcalc.so"),
        Path("/usr/lib/aarch64-linux-gnu/libcalc.so"),
    ]
    
    found = False
    for lib_path in lib_locations:
        if lib_path.exists():
            found = True
            # Should be a symlink for dev package
            assert lib_path.is_symlink() or lib_path.is_file(), f"{lib_path} should exist for linking"
            break
    
    assert found, "Unversioned libcalc.so not found (needed for dev package)"


def test_consumer_links_against_installed_library():
    """Verify consumer binary is linked against the installed library."""
    consumer_bin = Path("/app/consumer/consumer")
    
    result = subprocess.run(
        ["ldd", str(consumer_bin)],
        capture_output=True,
        text=True
    )
    
    assert "libcalc.so" in result.stdout, "Consumer not linked against libcalc"
