# CadQuery Intersection Tool

## Overview
This project is a Python-based tool for working with 3D geometry in STEP files using CadQuery. It allows users to define a plane in point-normal form, check for intersections with geometries in a STEP file, and export intersection points to a new STEP file.

## Features
- Read and process STEP files
- Define planes using point-normal form
- Check for intersections between the plane and geometries in the STEP file
- Export intersections to a new STEP file if found

---

## Installation Instructions (for macOS)

### Prerequisites
Ensure [Homebrew](https://brew.sh/) is installed.

1. Install Python:
   ```bash
   brew install python
   ```

2. Install `uv` package manager:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. Create a virtual environment and install dependencies:
   ```bash
   uv venv
   uv sync
   ```

---

## Usage

1. **Run the Program**
   ```bash
   uv run main.py --in-step <STEP_FILE_PATH> --in-plane x y z nx ny nz
   ```

   - Replace `<STEP_FILE_PATH>` with the path to your STEP file.
   - Replace `x, y, z, nx, ny, and nz` with the point and normal vector of the plane, space-separated e.g.:
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
├── requirements.txt        # Project dependencies
├── main.py                 # Main entry point
├── src/                    # Source code
│   ├── __init__.py         
│   ├── exceptions.py       # custom exceptions
│   ├── domain/             # data structures
│   │   ├── __init__.py
│   │   └── model.py
│   ├── fileio/             # io functions
│   │   ├── __init__.py
│   │   ├── reader.py
│   │   └── writer.py
│   └── geometry/           # 3D processing
│       ├── __init__.py
│       └── engine.py
│
└── tests/                  # Tests
    ├── __init__.py
    ├── conftest.py         # Fixtures
    ├── unit/               # Unit tests
    │   ├── __init__.py
    │   ├── test_fileio.py
    │   ├── test_model.py
    │   └── test_plane.py
    └── integration/        # Integration tests
        ├── __init__.py
        └── test_workflow.py
```

---

## Testing

Run the test suite using `pytest`:
```bash
uv run pytest
```

### Sample Tests
- **File Reading Tests**:
  - Check if the STEP file is correctly read
  - Validate error handling for non-existent or invalid files
- **Intersection Tests**:
  - Verify that intersections are detected and written to the output STEP file
  - Ensure no output file is created when no intersections are found

---

## Dependencies

- [CadQuery](https://cadquery.readthedocs.io/)
- Python 3.11+
- `uv` package manager

---

## Known Issues and Limitations

1. The tool assumes valid STEP files as input; invalid or malformed files may cause unexpected errors.
2. Intersection detection depends on the geometric complexity of the input model.

---
