import os
import cadquery as cq
from typing import Tuple
from ..exceptions import FileOperationError


class STEPReader:
    @staticmethod
    def validate_file(path: str) -> None:
        """Validates STEP file existence and format."""
        if not path.lower().endswith((".stp", ".step")):
            raise FileOperationError("Invalid file format", path)

        if not os.path.exists(path):
            raise FileOperationError("File does not exist", path)

    @staticmethod
    def read_model(path: str) -> cq.Workplane:
        """Reads and returns a CadQuery model from a STEP file."""
        try:
            STEPReader.validate_file(path)
            return cq.importers.importStep(path)
        except FileOperationError:
            raise
        except Exception as e:
            raise FileOperationError(f"Failed to read STEP file: {str(e)}", path)
