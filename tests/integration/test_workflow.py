import pytest
import os
from src.fileio.reader import STEPReader
from src.geometry.engine import GeometryEngine
from src.fileio.writer import STEPWriter
from src.domain.model import Point3D, Vector3D, Plane


def cleanup_file(output_file):
    if os.path.exists(output_file):
        os.remove(output_file)


def test_complete_workflow(cube_model, output_file, cube_plane_test_cases):
    """Test the complete workflow with the cube model."""
    engine = GeometryEngine(cube_model)

    # Test each plane case from our test cases
    for point, normal, expected_success, expected_points in cube_plane_test_cases:
        plane = Plane(point=point, normal=normal)
        result = engine.find_intersections(plane)

        assert result.success == expected_success

        if result.success:
            # Write results to file
            STEPWriter.write_intersection_points(result.points, output_file)
            assert os.path.exists(output_file)
            assert len(result.points) == expected_points

            # Verify point coordinates (for cube, should be 5 units from center)
            for point in result.points:
                max_coord = max(abs(point.x), abs(point.y), abs(point.z))
                assert abs(max_coord - 5.0) < 0.001

            cleanup_file(output_file)
        else:
            assert len(result.points) == 0
            assert not os.path.exists(output_file)


def test_edge_cases(cube_model, output_file):
    """Test edge cases with cube model."""
    engine = GeometryEngine(cube_model)

    # Test case: Plane exactly on cube edge
    edge_plane = Plane(
        point=Point3D(5, 0, 0), normal=Vector3D(1, 0, 0)  # Right face of cube
    )

    result = engine.find_intersections(edge_plane)
    assert not result.success  # exactly on the edge won't split anything
    assert len(result.points) == 0
