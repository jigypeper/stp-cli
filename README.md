# PythonOCC Intersection Tool

## Overview
This project is a Python-based tool for working with 3D geometry in STEP files using PythonOCC. It allows users to define a plane in point-normal form, check for intersections with geometries in a STEP file, and export intersection points to a new STEP file.

## Features
- Read and process STEP files.
- Define planes using point-normal form.
- Check for intersections between the plane and geometries in the STEP file.
- Export intersections to a new STEP file if found.

---

## Installation Instructions (for macOS)

There is a very particular order to this. If you miss anything, it will not work.

### Prerequisite
Ensure that [Homebrew](https://brew.sh/) is installed, as it simplifies package management.

1. Install required dependencies:
   ```bash
   brew install opencascade
   brew install conda
   brew install miniforge
   ```

2. Create a Conda environment for Python 3.11:
   ```bash
   conda env create --file environment.yml
   ```

3. Activate the environment:
   ```bash
   conda activate pyoccenv
   ```

> **Note**: You may need to deactivate and reactivate the environment (including the base environment) if issues arise:
> ```bash
> conda deactivate
> conda activate pyoccenv
> ```

In an ideal world, we would use Astral's `uv` for both package and environment management. However, `pythonocc-core` is not available on the PyPI repository, so Conda is required.

---

## Usage

1. **Run the Program**
   ```bash
   python src/main.py --in-step <STEP_FILE_PATH> --in-plane x y z nx ny nz
   ```

   - Replace `<STEP_FILE_PATH>` with the path to your STEP file.
   - Replace `x, y, z, nx, ny, and nz` with the point and normal vector of the plane, the points are space seperated e.g.:
     ```bash
     python main.py --in-step random-shape.stp --in-plane 0 0 100 0.2 0.1 1.0
     ```

2. **Outputs**
   - If intersections are found, they are written to `intersection.stp` in the project directory.
   - If no intersections are found, no new STEP file is created, and a message informs you accordingly.

---

## Project Structure

```
stp_cli/
├── README.md               # Documentation
├── environment.yml         # Conda environment file
├── main.py                 # Main entry point
├── intersection.stp        # Example output STEP file
├── intersection.stp        # Example output STEP file
├── src/                    # Source code
│   ├── __init__.py         # Package initialization
│   └── model_fns.py        # STEP file processing functions
└── tests/                  # Unit tests
    ├── __init__.py
    ├── test_read_file.py
    └── test_read_plane.py
```

---

## Testing

Run the test suite using `pytest`:
```bash
pytest
```

### Sample Tests
- **File Reading Tests**:
  - Check if the STEP file is correctly read.
  - Validate error handling for non-existent or invalid files.
- **Intersection Tests**:
  - Verify that intersections are detected and written to the output STEP file.
  - Ensure no output file is created when no intersections are found.

---

## Dependencies

- [pythonocc-core](https://github.com/tpaviot/pythonocc-core)
- OpenCASCADE (via Homebrew)
- Python 3.11 (via Conda)

---

## Known Issues and Limitations

1. `pythonocc-core` must be installed via Conda due to its unavailability on PyPI.
2. The tool assumes valid STEP files as input; invalid or malformed files may cause unexpected errors.

---
