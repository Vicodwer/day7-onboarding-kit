"""
New Developer Onboarding Kit
============================
Run this script on your first day to verify your Python development setup.

Usage:
    python onboard.py
    python onboard.py --verbose
    python onboard.py --fix
"""

import argparse
import shutil
import sys
import time
import os


def check_python_version():
    """Check that Python version is 3.10 or higher. Returns (status, message)."""
    major = sys.version_info.major
    minor = sys.version_info.minor
    version_str = f"{major}.{minor}.{sys.version_info.micro}"
    if major >= 3 and minor >= 10:
        return True, f"Python version: {version_str} (>= 3.10 required)"
    return False, f"Python version: {version_str} — WARNING: 3.10+ required"


def check_virtual_environment():
    """Check whether the script is running inside a virtual environment."""
    in_venv = sys.prefix != sys.base_prefix
    if in_venv:
        env_name = os.path.basename(sys.prefix)
        return True, f"Virtual environment: Active ({env_name})"
    return False, "Virtual environment: NOT active — activate your venv first!"


def check_installed_packages(verbose=False):
    """List all installed packages. Returns (status, message, package_dict)."""
    try:
        import importlib.metadata as meta

        packages = {
            dist.metadata["Name"]: dist.version for dist in meta.distributions()
        }
        if verbose:
            print("\n  Installed packages:")
            for name, version in sorted(packages.items()):
                print(f"    {name}=={version}")
        return True, f"Installed packages: {len(packages)} found", packages
    except Exception as exc:  # pylint: disable=broad-except
        return False, f"Could not list packages: {exc}", {}


def check_tool_installed(tool_name, packages):
    """Check if pylint or black is installed. Returns (status, message)."""
    normalized = {k.lower(): v for k, v in packages.items()}
    version = normalized.get(tool_name.lower())
    if version:
        return True, f"{tool_name} installed: version {version}"
    try:
        mod = __import__(tool_name)
        ver = getattr(mod, "__version__", "unknown")
        return True, f"{tool_name} installed: version {ver}"
    except ImportError:
        return False, f"{tool_name}: NOT installed"


def check_internet_connectivity():
    """Test internet connectivity by hitting a known URL."""
    try:
        import requests  # pylint: disable=import-outside-toplevel

        response = requests.get("https://httpbin.org/get", timeout=5)
        if response.status_code == 200:
            return True, "Internet connectivity: OK"
        return False, f"Internet connectivity: HTTP {response.status_code}"
    except ImportError:
        return False, "Internet connectivity: requests not installed"
    except Exception as exc:  # pylint: disable=broad-except
        return False, f"Internet connectivity: FAILED ({exc})"


def check_numpy(packages):
    """Check if numpy is installed. Returns (status, message)."""
    normalized = {k.lower(): v for k, v in packages.items()}
    version = normalized.get("numpy")
    if version:
        return True, f"numpy installed: version {version}"
    try:
        import numpy as np  # pylint: disable=import-outside-toplevel

        return True, f"numpy installed: version {np.__version__}"
    except ImportError:
        return False, "numpy: NOT installed"


def check_disk_space(threshold_gb=1.0):
    """Warn if available disk space is below threshold. Returns (status, message)."""
    usage = shutil.disk_usage("/")
    free_gb = usage.free / (1024**3)
    if free_gb >= threshold_gb:
        return (
            True,
            f"Disk space: {free_gb:.1f} GB free (>= {threshold_gb} GB required)",
        )
    return False, f"Disk space: {free_gb:.1f} GB free — WARNING: low disk space!"


def build_report(results, total_time):
    """Build a formatted report string from check results."""
    lines = ["=== Developer Onboarding Check ===", ""]
    passed = sum(1 for status, _ in results.values() if status)
    total = len(results)
    for _label, (status, message) in results.items():
        tag = "[PASS]" if status else "[FAIL]"
        lines.append(f"{tag} {message}")
    lines.extend(
        [
            "",
            "-" * 40,
            f"Result: {passed}/{total} checks passed {'✓' if passed == total else '✗'}",
            f"Total time: {total_time:.2f}s",
        ]
    )
    return "\n".join(lines)


def save_report(report_text, filename="setup_report.txt"):
    """Save the report to a text file. Returns filename."""
    with open(filename, "w", encoding="utf-8") as fh:
        fh.write(report_text)
    return filename


def attempt_fix(packages):
    """Attempt to install missing required packages using pip. (--fix flag)"""
    import subprocess  # pylint: disable=import-outside-toplevel

    required = ["pylint", "black", "numpy", "requests"]
    normalized = {k.lower() for k in packages}
    missing = [pkg for pkg in required if pkg not in normalized]
    if not missing:
        print("\n[FIX] All required packages already installed.")
        return
    for pkg in missing:
        print(f"\n[FIX] Installing {pkg}...")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", pkg],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            print(f"  ✓ {pkg} installed successfully")
        else:
            print(f"  ✗ Failed to install {pkg}: {result.stderr.strip()}")


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="New Developer Onboarding Kit — verify your Python setup."
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show extra detail (full package list + timings)",
    )
    parser.add_argument(
        "--fix", action="store_true", help="Attempt to install any missing packages"
    )
    return parser.parse_args()


def run_checks(verbose=False):
    """Run all setup checks. Returns (results_dict, packages, total_time)."""
    results = {}
    timings = {}

    for label, fn in [
        ("Python Version", check_python_version),
        ("Virtual Environment", check_virtual_environment),
    ]:
        start = time.time()
        results[label] = fn()
        timings[label] = time.time() - start

    start = time.time()
    pkg_status, pkg_msg, packages = check_installed_packages(verbose=verbose)
    timings["Installed Packages"] = time.time() - start
    results["Installed Packages"] = (pkg_status, pkg_msg)

    for label, fn in [
        ("pylint", lambda: check_tool_installed("pylint", packages)),
        ("black", lambda: check_tool_installed("black", packages)),
        ("numpy", lambda: check_numpy(packages)),
    ]:
        start = time.time()
        results[label] = fn()
        timings[label] = time.time() - start

    start = time.time()
    results["Internet"] = check_internet_connectivity()
    timings["Internet"] = time.time() - start

    start = time.time()
    results["Disk Space"] = check_disk_space()
    timings["Disk Space"] = time.time() - start

    if verbose:
        print("\n  Check timings (seconds):")
        for label, elapsed in timings.items():
            print(f"    {label}: {elapsed:.3f}s")

    return results, packages, sum(timings.values())


def main():
    """Main function — orchestrates all checks and produces the report."""
    args = parse_args()
    print("Running developer onboarding checks...\n")
    global_start = time.time()
    results, packages, _ = run_checks(verbose=args.verbose)
    total_time = time.time() - global_start
    report = build_report(results, total_time)
    print(report)
    saved_path = save_report(report)
    print(f"\nReport saved to: {saved_path}")
    if args.fix:
        attempt_fix(packages)


if __name__ == "__main__":
    main()
