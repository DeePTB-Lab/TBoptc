# TBoptc

[![License: LGPL v3](https://img.shields.io/badge/License-LGPL_v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)

## Description

`TBoptc` is a Python package for calculating optical spectra of Tight-Binding (TB) models, specifically designed and optimized for the DeePTB model. It combines the ease of use of Python with the computational efficiency of Fortran (optional).

## Features

*   Calculates optical conductivity.
*   Supports DeePTB models.
*   Built with `scikit-build-core` and CMake.

## Installation

### Prerequisites

*   Python >= 3.8
*   CMake >= 3.17
*   A C compiler (e.g., GCC, Clang, or Intel ICX)
*   A Fortran compiler (e.g., GFortran or Intel IFX)
*   NumPy

### Install from Source

1.  Clone the repository:
    ```bash
    git clone https://github.com/DeePTB-Lab/TBoptc.git
    cd TBoptc
    ```

2.  Install dependencies:
    Core dependencies are listed in `pyproject.toml` and are usually installed automatically in the next step. Ensure you have `numpy` and `scikit-build-core` installed:
    ```bash
    pip install numpy scikit-build-core
    ```
3.  Install DeePTB:
    please refer to its documentation: <https://github.com/deepmodeling/DeePTB>

3.  Install the package:
    ```bash
    pip install .
    ```
## Build Options (for Developers)
The project uses scikit-build-core and CMake for building. The main build options are defined in CMakeLists.txt :

- BUILD_FORTRAN : (ON/OFF, default ON) Whether to build Fortran extensions. Can be controlled by the BUILD_FORTRAN environment variable.
- USE_INTEL : (ON/OFF, default ON) If BUILD_FORTRAN is ON, whether to try using Intel compilers (icx, ifx). If OFF, system default compilers are used.
- USE_OPENMP : (ON/OFF, default ON) If BUILD_FORTRAN is ON, whether to enable OpenMP support.
During the build, CMake automatically finds the Python interpreter, development modules, and NumPy.

## Dependencies
Main dependencies include:

- Python (>=3.8)
- NumPy
- SciPy
- Spglib
- Matplotlib
- Torch (>=1.13.0)
- ASE
- PyYAML
- future
- dargs
- dptb
Development and testing dependencies:

- pytest (>=7.2.0)
- pytest-order (==1.2.0)
- scikit-build-core
- setuptools (>=45)
- setuptools-scm[toml] (>=6.2)
## Contributing
Contributions are welcome! Please participate in the project by submitting Pull Requests or creating Issues.

## License
This project is licensed under the LGPL-3.0 License.

## Contact
- Author: Q. Gu ( guqq@ustc.edu.cn )
- Repository: https://github.com/DeePTB-Lab/TBoptc
