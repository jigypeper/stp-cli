import pytest
import cadquery as cq
import os
from src.domain.model import Point3D, Vector3D, Plane


@pytest.fixture
def output_file(tmp_path):
    """Creates a temporary file path for test output."""
    return str(tmp_path / "test_output.stp")


@pytest.fixture
def cube_model():
    """Creates a 10x10x10 cube centered at origin for testing."""
    return (
        cq.Workplane().box(10, 10, 10).val()  # Create 10x10x10 cube centered at origin
    )  # Get the underlying shape


@pytest.fixture
def cube_plane_test_cases():
    """
    Returns test cases for cube intersection with known results.
    Each case contains: plane point, plane normal, expected success, expected points count
    """
    return [
        # Horizontal plane through middle (y=0)
        (
            Point3D(0, 0, 0),
            Vector3D(0, 1, 0),
            True,
            12,  # Should intersect in a square -> 4 points
        ),
        # Vertical plane through middle (x=0)
        (Point3D(0, 0, 0), Vector3D(1, 0, 0), True, 12),
        # Diagonal plane through middle
        (Point3D(0, 0, 0), Vector3D(1, 1, 0), True, 8),
        # Plane outside cube
        (Point3D(10, 0, 0), Vector3D(1, 0, 0), False, 0),
    ]


def test_cube_intersections(cube_model, cube_plane_test_cases):
    """Test intersections with a simple cube where we know the expected results."""
    from src.geometry.engine import GeometryEngine

    engine = GeometryEngine(cube_model)

    for point, normal, expected_success, expected_points in cube_plane_test_cases:
        plane = Plane(point=point, normal=normal)
        result = engine.find_intersections(plane)

        assert (
            result.success == expected_success
        ), f"Failed for plane at {point} with normal {normal}"
        assert result.points == expected_points, (
            f"Expected {expected_points} intersection points, got {len(result.points)} "
            f"for plane at {point} with normal {normal}"
        )

        if result.success:
            # For middle planes, verify points are at the expected distances
            # e.g., for a 10x10x10 cube, points should be 5 units from center
            for point in result.points:
                # At least one coordinate should be at ±5 (half the cube size)
                max_coord = max(abs(point.x), abs(point.y), abs(point.z))
                assert abs(max_coord - 5.0) < 0.001, (
                    f"Expected point to be 5 units from center, "
                    f"got point at {point}"
                )
