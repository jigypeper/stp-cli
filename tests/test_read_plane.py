import os
import pytest
from OCC.Core.STEPControl import STEPControl_Reader
from src.model_fns import read_plane


@pytest.fixture
def step_model():
    """Load a sample STEP model for testing."""
    step_reader = STEPControl_Reader()
    status = step_reader.ReadFile("./random-shape.stp")
    assert status == 1, "Failed to load test STEP file"
    return step_reader


@pytest.fixture
def cleanup_output():
    """Fixture to clean up output files before and after tests."""
    output_file = "test_intersection.stp"
    if os.path.exists(output_file):
        os.remove(output_file)
    yield output_file
    if os.path.exists(output_file):
        os.remove(output_file)


def test_plane_intersects_creates_file(step_model, cleanup_output):
    """Test if intersections produce a new STEP file and return valid points."""
    # Plane at origin with normal along Z-axis
    plane_coords = (0, 0, 0, 0, 0, 1)

    success, points = read_plane(step_model, plane_coords, cleanup_output)

    assert success is True
    assert os.path.exists(cleanup_output)
    assert len(points) > 0

    # Verify point structure
    for point in points:
        assert len(point) == 3
        assert all(isinstance(coord, float) for coord in point)


def test_plane_no_intersects_no_file(step_model, cleanup_output):
    """Test if no intersections produce no new STEP file and empty points list."""
    # Plane far away from geometry
    plane_coords = (1000, 1000, 1000, 0, 0, 1)

    success, points = read_plane(step_model, plane_coords, cleanup_output)

    assert success is False
    assert not os.path.exists(cleanup_output)
    assert len(points) == 0


def test_plane_with_different_normal(step_model, cleanup_output):
    """Test intersection with plane having different normal vector."""
    # Plane at origin with normal along X-axis
    plane_coords = (0, 0, 0, 1, 0, 0)

    success, points = read_plane(step_model, plane_coords, cleanup_output)

    assert success in [True, False]  # Could be either depending on geometry
    if success:
        assert os.path.exists(cleanup_output)
        assert len(points) > 0
        for point in points:
            assert len(point) == 3
    else:
        assert not os.path.exists(cleanup_output)
        assert len(points) == 0


def test_plane_coordinates_validation(step_model):
    """Test function with various invalid plane coordinates."""
    # Test zero normal vector
    with pytest.raises(ValueError) as exc_info:
        read_plane(step_model, (0, 0, 0, 0, 0, 0), "test_intersection.stp")
    assert "Normal vector cannot be zero" in str(exc_info.value)

    # Test infinite values
    with pytest.raises(ValueError) as exc_info:
        read_plane(step_model, (0, 0, 0, float("inf"), 0, 1), "test_intersection.stp")
    assert "NaN or infinite values" in str(exc_info.value)

    # Test NaN values
    with pytest.raises(ValueError) as exc_info:
        read_plane(step_model, (0, 0, 0, float("nan"), 0, 1), "test_intersection.stp")
    assert "NaN or infinite values" in str(exc_info.value)
