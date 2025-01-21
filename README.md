# Installation Instructions (for macOS)
There is a very particular order to this. If you miss anything, it will not work.

## Prerequisite
Ensure that homebrew is installed, a package manager will make this easier.
1. Install opencascade, conda, and miniforge
```bash
brew install opencascade
brew install conda
brew install miniforge
```
2. Create a conda environment for python 3.11
```bash
conda env create --file environment.yml
```
Note: you may need to deactivate and the environment and reactivate it (including the base environment) `conda deactivate` followed by `conda activate pyoccenv`.

In an ideal world I would use Astrals `uv` for both package management and environment management, but pythonocc-core is not available on the PyPi repository. Hence why we are using conda.
