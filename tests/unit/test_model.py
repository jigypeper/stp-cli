import pytest
from src.domain.model import Point3D, Vector3D, Plane
from src.exceptions import ValidationError


@pytest.mark.parametrize("x,y,z", [(0, 0, 0), (1.0, 0, 0), (0, 1.0, 0), (0, 0, 1.0)])
def test_point_creation(x: float, y: float, z: float):
    point = Point3D(x, y, z)
    assert point.x == x
    assert point.y == y
    assert point.z == z


def test_vector_validation():
    with pytest.raises(ValidationError):
        Vector3D(0, 0, 0).validate()


def test_plane_validation():
    with pytest.raises(ValidationError):
        Plane(point=Point3D(0, 0, 0), normal=Vector3D(0, 0, 0)).validate()
