
# pybertini Changelog

All notable changes to this project will be documented in this file.

The format is based on [CHANGELOG.md][CHANGELOG.md]
and this project adheres to [Semantic Versioning][Semantic Versioning].

<!--
_______________________________________________________________________________

## [1.0.2] - 2025-05-07

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
