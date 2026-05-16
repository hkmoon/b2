
# bertini2 Changelog

All notable changes to this project will be documented in this file.

The format is based on [CHANGELOG.md][CHANGELOG.md]
and this project adheres to [Semantic Versioning][Semantic Versioning].

<!--
_______________________________________________________________________________

## [1.0.0] - 2026-04-02

Preparation for pypi release with github workflow

### Added

- github workflow for pypi and github release

### Changed

- `publish-to-test-pypi.yml` for handling the comments

### Changed

* merged the pull request for github ci release by @hkmoon in https://github.com/hkmoon/b2/pull/1
* windows release preparation
  * `size_t` is translated into `unsigned long` in linux, mac while `unsigned long long` in windows 10: `core/include/bertini2/eigen_extensions.hpp` and `core/test/classes/start_system_test.cpp` are modified
  * use `clang` of LLVM in Windows since MSVC has different compiling way for `template`
  * use `--no-isolation` for `scikit-build` in Windows
* For linux wheel naming convention, we cannot use x86_64, x86_i386 anymore for pypi repository. https://peps.python.org/pep-0600/
  * use `auditwheel` for it

### New Contributors
* @hkmoon made their first contribution in https://github.com/hkmoon/b2/pull/1

_______________________________________________________________________________

-->

<!--
_______________________________________________________________________________
TEMPLATE

## [major.minor.patch] - yyyy-mm-dd

A message that notes the main changes in the update.

### Added

### Changed

### Deprecated

### Fixed

### Removed

### Security

### New Contributors

_______________________________________________________________________________

-->


_______________________________________________________________________________

## [2.0.1] - 2026-05-16

First release under the `bertini2` PyPI name. This is the consolidation of
several months of cross-platform packaging work, dependency-compatibility
fixes, documentation, and a final round of precision-handling fixes in the
system / SLP path. Intel macOS is dropped from the supported platform list
for this release (see Removed below).

### Added

- Wheel distributions on PyPI for Linux, macOS (Apple Silicon), and Windows
  across Python 3.9 – 3.13. Linux wheels use the `manylinux_2_28` image; macOS
  and Linux wheels are produced via `cibuildwheel`; Windows wheels bundle
  required DLLs via `delvewheel` and a `windows_dll_manager.py` helper that
  registers DLL search paths before importing `_pybertini`.
- GitHub Pages documentation site: C++ API via Doxygen, Python API via Sphinx.
- Version numbers (b2, GMP, MPFR, Eigen, Boost) exposed from the Python
  package so users can query them at runtime.
- `CHANGELOG.md` itself, following the *Keep a Changelog* format.

### Changed

- **Package renamed: `pybertini` → `bertini` → `bertini2`.** The current PyPI
  name is `bertini2`. Update your `pip install` and import statements
  accordingly; the Python module still imports as `import bertini`.
- Version is now read from `pyproject.toml` by CMake, removing the two-place
  manual sync that previously drifted.
- Build system: `scikit-build-core` configures CMake for the wheel build;
  `pyproject.toml` is the single source of truth for build inputs. The Linux
  wheel build rebuilds Boost.Python and eigenpy per target Python version so
  each wheel ships a matching `libboost_python3X`.
- CI matrix expanded to cover Ubuntu, macOS (Apple Silicon), and Windows for
  Python 3.9 – 3.13. PRs targeting `develop` and pushes to `develop` / `main`
  run the full matrix; other branches run a fast Ubuntu + macos-14 + Python
  3.11 matrix.
- CI build now uses Boost 1.90 (was 1.87). Boost 1.90 pre-seeds
  `thread_default_precision` from the global default and guards against 0,
  removing a class of MPFR abort hazards.
- `boost_system` is now conditionally linked for Boost < 1.89 only (Boost 1.89
  dropped the separate library).
- Eigen requirement updated to `3.3...3.4` with the macOS install switched to
  Homebrew's `eigen@3` formula.
- Tests across platforms now use a unified precision-handling pattern,
  eliminating per-platform skips and conditional precision rituals.
- `MACOSX_DEPLOYMENT_TARGET` co-varies with the runner version so wheels
  produced on macos-14 are loadable on the same OS family.
- TestPyPI publishes on every push to `develop`; PyPI publishes on tagged
  releases (`v*.*.*`) with Sigstore signing and a GitHub Release.

### Fixed

- `System::operator+=` and `System::operator*=` now invalidate the cached
  derivatives flag (`is_differentiated_`), so a subsequent `eval` rebuilds the
  SLP instead of evaluating against stale derivatives. The companion mutators
  `Reorder`, `Simplify`, and `ClearVariables` also invalidate the cache.
- `SLPCompiler::Compile` now seeds the mpfr default precision from the SLP's
  own `precision_` immediately before growing the `mpfr_complex` memory block.
  This prevents a `mpfr_init2(x, 0)` abort when `thread_default_precision()`
  is left at 0 on a fresh thread under Boost ≥ 1.87.
- Python module init seeds `thread_default_precision` so the first MPFR
  construction on the interpreter thread is always valid.
- `eval` overload registration order in the Python bindings changed so the
  double-precision overload is tried before the multi-precision overload for
  ambiguous inputs (e.g. NumPy int64 arrays); this avoids the eigenpy
  `Vec<mpfr>` extractor probing MPFR construction with precision 0.
- `EIGEN_MAKE_ALIGNED_OPERATOR_NEW` moved to the `public` section of the
  `System` class (was incorrectly placed in a non-public section).
- A second `find_package(Boost)` no longer clobbers `Boost_LIBRARIES`.
- The `_pybertini` target is always created (previously it was only created
  when bertini was the top-level CMake project, breaking out-of-tree builds).
- Various MSVC-specific build fixes: `/bigobj`, `/EHsc`, explicit-type
  workarounds for template instantiation issues, Release-config library
  linking.

### Removed

- **Intel macOS (`macos-15-intel`) is not built or tested in this release.**
  A SIGABRT in pytest involving MPFR/Boost surfaces only on Intel runners and
  cannot be reproduced on the maintainer's development hardware. Intel wheels
  will return once a reproducer or upstream fix is in hand. Users on Intel
  Macs should pin to a 1.0.x release or build from source.
- Stale build artifacts and outdated Python-binding documentation removed
  from the repo.

_______________________________________________________________________________

## [1.0.3] - 2025-05-16

Preparation for pypi release with github workflow

### Changed

* make it compatible for Windows

_______________________________________________________________________________

## [1.0.2] - 2025-05-07

Preparation for pypi release with github workflow

### Added

- github workflow for pypi and github release

### Changed

- `publish-to-test-pypi.yml` for handling the comments correctly

### Changed

* merged the pull request for github ci release by @hkmoon in https://github.com/hkmoon/b2/pull/1
* windows release preparation
    * `size_t` is translated into `unsigned long` in linux, mac while `unsigned long long` in windows 10: `core/include/bertini2/eigen_extensions.hpp` and `core/test/classes/start_system_test.cpp` are modified
    * use `clang` of LLVM in Windows since MSVC has different compiling way for `template`
    * use `--no-isolation` for `scikit-build` in Windows
* For linux wheel naming convention, we cannot use x86_64, x86_i386 anymore for pypi repository. https://peps.python.org/pep-0600/
    * use `auditwheel` for it

### New Contributors
* @hkmoon made their first contribution in https://github.com/hkmoon/b2/pull/1

_______________________________________________________________________________

## [1.0.1] - 2025-05-06

This is the initial version of the project.

### Added

- The base project

[CHANGELOG.md]: https://keepachangelog.com/en/1.1.0/
[Semantic Versioning]: http://semver.org/

<!-- markdownlint-configure-file {
    "MD022": false,
    "MD024": false,
    "MD030": false,
    "MD032": false
} -->
<!--
    MD022: Blanks around headings
    MD024: No duplicate headings
    MD030: Spaces after list markers
    MD032: Blanks around lists
-->
