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
conda create --name=pyoccenv python=3.11
```
