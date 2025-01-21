from OCC.Core.STEPControl import (
    STEPControl_Reader,
    STEPControl_Writer,
    STEPControl_AsIs,
)
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeVertex, BRepBuilderAPI_MakeFace
from OCC.Core.TopoDS import TopoDS_Compound, TopoDS_Shape
from OCC.Core.BRep import BRep_Builder, BRep_Tool
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_VERTEX
from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Pln
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Section
import math
from typing import List, Tuple


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

    Status Codes and Messages:
        1: "File read successfully" - Indicates the file was read without issues.
        2: "File cannot be found" - Indicates the specified file does not exist.
        3: "Incorrect file type, is this a step file?" - Indicates the file is not in the expected STEP format.
       -1: "Unknown Error" - Indicates the error is not known refer to documentation.

    Notes:
        - This function uses the `STEPControl_Reader` class to read the file.
        - Ensure the file path provided points to a valid STEP file.
    """

    READ_FILE_RESULTS: dict[int, str] = {
        1: "File read successfully",
        2: "File cannot be found",
        3: "Incorrect file type, is this a step file?",
        -1: "Uknown Error",
    }

    step_reader = STEPControl_Reader()
    result = step_reader.ReadFile(file)

    match result:
        case 1:
            return (1, READ_FILE_RESULTS[1])
        case 2:
            return (2, READ_FILE_RESULTS[2])
        case 3:
            return (3, READ_FILE_RESULTS[3])
        case _:
            return (-1, READ_FILE_RESULTS[-1])


def read_plane(
    model: STEPControl_Reader,
    coordinates: Tuple[float, float, float, float, float, float],
    output_file: str = "intersection.stp",
) -> Tuple[bool, List[Tuple[float, float, float]]]:
    """
    Reads a plane definition, checks for intersections with the model's geometry,
    and writes intersections to a new STEP file if found.

    Args:
        model (STEPControl_Reader): The loaded STEP model.
        coordinates (Tuple[float, float, float, float, float, float]):
            A tuple representing the plane's point (x, y, z) and normal vector (nx, ny, nz).
        output_file (str): The path to the output STEP file for intersections.

    Returns:
        Tuple[bool, List[Tuple[float, float, float]]]:
            - Boolean indicating if intersections were found and written
            - List of intersection points as (x, y, z) tuples

    Raises:
        ValueError: If the normal vector is zero or contains invalid values
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

    # Create geometric plane
    point = gp_Pnt(px, py, pz)
    normal = gp_Dir(nx, ny, nz)
    plane = gp_Pln(point, normal)

    # Create a face from the plane
    plane_face = BRepBuilderAPI_MakeFace(plane).Face()

    # Transfer roots if not already done
    if model.NbRootsForTransfer() > 0:
        model.TransferRoots()

    # Get the shape from the model
    shape: TopoDS_Shape = model.Shape(1)

    # Initialize containers for results
    intersection_points: List[Tuple[float, float, float]] = []
    compound = TopoDS_Compound()
    builder = BRep_Builder()
    builder.MakeCompound(compound)

    # Create section between plane and shape
    section = BRepAlgoAPI_Section(shape, plane_face)
    section.Build()

    if section.IsDone():
        section_shape = section.Shape()

        # Extract vertices from the intersection
        explorer = TopExp_Explorer()
        explorer.Init(section_shape, TopAbs_VERTEX)

        while explorer.More():
            vertex = explorer.Current()
            point = BRep_Tool.Pnt(vertex)  # Get the gp_Pnt from the vertex
            builder.Add(compound, BRepBuilderAPI_MakeVertex(point).Shape())

            # Get point coordinates
            point_coords = (point.X(), point.Y(), point.Z())
            intersection_points.append(point_coords)

            explorer.Next()

    if intersection_points:
        # Write intersections to STEP file
        writer = STEPControl_Writer()
        status = writer.Transfer(compound, STEPControl_AsIs)

        if status:
            write_status = writer.Write(output_file)
            return write_status == 1, intersection_points

    return False, []
