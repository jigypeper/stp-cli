from typing import Optional
import cadquery as cq
from ..domain.model import Plane, IntersectionResult, Point3D
from ..exceptions import GeometryError


class GeometryEngine:
    def __init__(self, model: cq.Workplane):
        self.model = model

    def find_intersections(self, plane: Plane) -> IntersectionResult:
        """
        Finds intersections between the model and a plane.

        Returns:
            IntersectionResult containing success status and intersection points
        """
        try:
            plane_face = self._create_plane_face(plane)
            split_result = self.model.split(plane_face)
            print(type(split_result.solids()))
            print(type(self.model.solids()))

            if split_result.solids() == self.model.solids():
                return IntersectionResult(success=False, points=[])

            intersection_points = []
            for side in split_result.solids():
                for vertex in side.Vertices():
                    x, y, z = vertex.toTuple()
                    intersection_points.append(Point3D(x, y, z))

            return IntersectionResult(
                success=True, points=list(set(intersection_points))
            )

        except Exception as e:
            raise GeometryError(f"Failed to compute intersections: {str(e)}")

    def _create_plane_face(self, plane: Plane) -> cq.Face:
        """Creates a CadQuery face from a plane definition."""
        try:
            return cq.Face.makePlane(
                None,
                None,
                cq.Vector(*plane.point.to_tuple()),
                cq.Vector(*plane.normal.to_tuple()),
            )
        except Exception as e:
            raise GeometryError(f"Failed to create plane: {str(e)}")
