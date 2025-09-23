
# Windows Build Instructions

This document provides instructions for building the project on Windows. It covers the installation of necessary dependencies, setting up the environment, and compiling the code.

## Prerequisites

- Install [Visual Studio](https://visualstudio.microsoft.com/) with the "Desktop development with C++" workload.
  
- In the Visual Studio Installer I selected three things (https://stackoverflow.com/questions/18711595/how-run-clang-from-command-line-on-windows):
  Desktop development with C++ from the Workload tab
  C++ Clang Compiler for Windows (13.0.1) from the Individual Components tab.
  C++ Clang-cl for v143 build tools (x64/x86) from the Individual Components tab.

- Install [Micromamba](https://mamba.readthedocs.io/en/latest/installation.html#micromamba).

- Use `Developer PowerShell for VS 2022` to have access to `cl` and `clang-cl`.

  ![img/powershell.png](img/powershell.png)

## Setting Up the Environment

1. Create and activate the Micromamba environment:

```powershell
micromamba env create --file environment-win.yml
micromamba activate b2-windows

# To remove the environment later:
# micromamba deactivate
# micromamba env remove -n b2-windows
```

2. Install additional dependencies:

- Replace `public virtual std::exception` with `public std::exception` in the boost archive exception header:

```powershell
# Find your micromamba environment path
$envPath = micromamba info | Select-String "envs directories" | ForEach-Object { ($_ -split ":", 2)[1].Trim() }
$boostFile = "$envPath\b2-windows\Library\include\boost\archive\archive_exception.hpp"
(Get-Content $boostFile).Replace('public virtual std::exception', 'public std::exception') | Set-Content $boostFile
```

- Set `CMAKE_PREFIX_PATH` environment variable to your micromamba environment:

```powershell
# Automatically detect micromamba environment path
$envPath = micromamba info | Select-String "envs directories" | ForEach-Object { ($_ -split ":", 2)[1].Trim() }
$env:CMAKE_PREFIX_PATH="$envPath\b2-windows\Library"
```

- Set `CC` and `CXX` environment variables to use clang:

```powershell
$env:CC='clang-cl'
$env:CXX='clang-cl'
```

## Building the Project

1. Create a build directory and run CMake:

```powershell
cmake -DENABLE_UNIT_TESTING=ON -G Ninja -B bld .
cmake --build bld --target all --config Release
ctest --test-dir bld/core
```

## Changes to Note

* requires-python = ">= 3.13" -> requires-python = ">= 3.11"
* For Windows convention: uint -> unsigned int due to `error: unknown type name 'uint'; did you mean 'int'?`
* All the python bindings are commented out because core needs to be compiled first
* Generating dlls for windows binaries
* Add _WIN32 in #ifndef BERTINI_DISABLE_PRECISION_CHECKS otherwise it causes precision errors
* this->template Set(stepping); -> this->template Set<SteppingConfig>(stepping);
* this->template Set(newton); -> this->template Set<NewtonConfig>(newton);
* Remove #define BOOST_TEST_DYN_LINK 1
* const double threshold_clearance_d = 1e-15; -> const double threshold_clearance_d = 1e-14;
* use size_t index = 0; for tests
* remove scikit-build 

