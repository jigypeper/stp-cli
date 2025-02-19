import pytest
import math
from src.domain.model import Point3D, Vector3D, Plane
from src.exceptions import ValidationError


def test_point_creation_with_nan():
    """Test Point3D creation with NaN values."""
    with pytest.raises(ValidationError):
        Point3D(1.0, math.nan, 3.0)


def test_point_creation_with_inf():
    """Test Point3D creation with infinite values."""
    with pytest.raises(ValidationError):
        Point3D(1.0, math.inf, 3.0)


@pytest.mark.parametrize(
    "coords", [(1.0, 2.0, 3.0), (-1.0, -2.0, -3.0), (0.0, 0.0, 1.0)]
)
def test_valid_point_creation(coords):
    """Test creation of valid Point3D."""
    x, y, z = coords
    point = Point3D(x, y, z)  # Should not raise
    assert (point.x, point.y, point.z) == coords


@pytest.mark.parametrize(
    "coords,should_raise",
    [
        ((0, 0, 0), True),
        ((1, 0, 0), False),
        ((0, 1, 0), False),
        ((0, 0, 1), False),
        ((0.5, 0.5, 0.5), False),
    ],
)
def test_vector_creation(coords, should_raise):
    """Test Vector3D creation with various inputs."""
    x, y, z = coords
    if should_raise:
        with pytest.raises(ValidationError):
            Vector3D(x, y, z)
    else:
        vector = Vector3D(x, y, z)  # Should not raise
        assert (vector.x, vector.y, vector.z) == coords


def test_plane_creation():
    """Test creation of valid Plane."""
    point = Point3D(1.0, 2.0, 3.0)
    normal = Vector3D(0.0, 0.0, 1.0)
    plane = Plane(point=point, normal=normal)  # Should not raise
    assert plane.point == point
    assert plane.normal == normal


def test_plane_creation_with_invalid_normal():
    """Test Plane creation with invalid normal vector."""
    point = Point3D(0, 0, 0)
    with pytest.raises(ValidationError):
        # This will fail during Vector3D creation
        normal = Vector3D(0, 0, 0)
        # We won't even get to Plane creation


def test_plane_creation_with_invalid_point():
    """Test Plane creation with invalid point."""
    with pytest.raises(ValidationError):
        point = Point3D(math.nan, 0, 0)
        # We won't even get to normal or Plane creation
