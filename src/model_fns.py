import cadquery as cq
import math
from typing import List, Tuple
import os

from cadquery.occ_impl.shapes import intersect


def read_file(file: str) -> Tuple[int, str]:
    """
    Reads a STEP file and returns the status of the operation along with a descriptive message.

    Args:
        file (str): The path to the file to be read.

    Returns:
        tuple[int, str]:
            - If the file is successfully read, returns a tuple containing:
                - An integer status code (1 for success, 2 for file not found, 3 for incorrect file type).
                - A string message describing the result.
            - If an unknown error occurs, returns a -1 code and a string "Unknown Error".
    """
    READ_FILE_RESULTS: dict[int, str] = {
        1: "File read successfully",
        2: "File cannot be found",
        3: "Incorrect file type, is this a step file?",
        -1: "Unknown Error",
    }

    try:
        # Try to load the file
        if not os.path.exists(file):
            return (2, READ_FILE_RESULTS[2])
        
        # Check file extension
        if not file.lower().endswith('.stp') and not file.lower().endswith('.step'):
            return (3, READ_FILE_RESULTS[3])
        
        # Try to load the model
        model = cq.importers.importStep(file)
        
        return (1, READ_FILE_RESULTS[1])
    except Exception:
        return (-1, READ_FILE_RESULTS[-1])


def read_plane(
    model: cq.Workplane,
    coordinates: Tuple[float, float, float, float, float, float],
    output_file: str = "intersection.stp",
) -> Tuple[bool, List[Tuple[float, float, float]]]:
    """
    Finds intersections between a model and a plane.
    """
    # Validate coordinates
    px, py, pz, nx, ny, nz = coordinates
    
    # Check for invalid values
    for val in coordinates:
        if math.isnan(val) or math.isinf(val):
            raise ValueError("Coordinates contain NaN or infinite values")
    
    # Check for zero normal vector
    if nx == 0 and ny == 0 and nz == 0:
        raise ValueError("Normal vector cannot be zero")
    
    try:
        # Create plane
        plane_point = cq.Vector(px, py, pz)
        plane_normal = cq.Vector(nx, ny, nz)
        
        # Create plane face
        plane_face = cq.Face.makePlane(
            None,  # No width specified
            None,  # No height specified
            plane_point, 
            plane_normal
        )
        
        # Split the model
        split_result = model.split(plane_face)
        
        # Check if the split result is different from the original model
        if split_result.solids().size() != model.solids().size():
            # Find intersection points (vertices from the split parts)
            intersection_points = []
            for side in split_result.solids():
                for vertex in side.Vertices():
                    intersection_points.append(vertex.toTuple())
            
            # Remove duplicate points
            unique_points = list(set(intersection_points))
            
            # If intersections exist, write to file
            if unique_points:
                vertices = cq.Workplane().pushPoints(unique_points)
                cq.exporters.export(vertices, output_file, "STEP")
                return True, unique_points
        
        return False, []
    
    except Exception as e:
        print(f"Intersection error: {e}")
        return False, []
