import cadquery as cq
from typing import List
from ..domain.model import Point3D
from ..exceptions import FileOperationError


class STEPWriter:
    @staticmethod
    def write_intersection_points(points: List[Point3D], output_path: str) -> None:
        """Writes intersection points to a STEP file."""
        try:
            vertices = cq.Workplane().pushPoints([p.to_tuple() for p in points])
            cq.exporters.export(vertices, output_path, "STEP")
        except Exception as e:
            raise FileOperationError(
                f"Failed to write intersection points: {str(e)}", output_path
            )
