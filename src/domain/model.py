from dataclasses import dataclass
from typing import List, Tuple
from ..exceptions import ValidationError
import math


@dataclass(frozen=True)
class Point3D:
    x: float
    y: float
    z: float

    def __post_init__(self):
        """Validates coordinates after initialization."""
        self.validate()

    def validate(self) -> None:
        """Validates coordinate values."""
        for val in (self.x, self.y, self.z):
            if math.isnan(val) or math.isinf(val):
                raise ValidationError("Coordinates contain NaN or infinite values")

    def to_tuple(self) -> Tuple[float, float, float]:
        return (self.x, self.y, self.z)

    def __hash__(self):
        """Make the class hashable for use in sets."""
        return hash((self.x, self.y, self.z))

    def __eq__(self, other):
        """Define equality for hash comparison."""
        if not isinstance(other, Point3D):
            return NotImplemented
        # Use small epsilon for float comparison
        epsilon = 1e-10
        return (
            abs(self.x - other.x) < epsilon
            and abs(self.y - other.y) < epsilon
            and abs(self.z - other.z) < epsilon
        )


@dataclass(frozen=True)
class Vector3D(Point3D):
    x: float
    y: float
    z: float

    def __post_init__(self):
        """Validates vector after initialization."""
        self.validate()

    def validate(self) -> None:
        """Validates vector is non-zero and has valid coordinates."""
        # Validate coordinates first
        for val in (self.x, self.y, self.z):
            if math.isnan(val) or math.isinf(val):
                raise ValidationError("Vector contains NaN or infinite values")

        # Validate non-zero
        if self.x == 0 and self.y == 0 and self.z == 0:
            raise ValidationError("Vector cannot be zero")


@dataclass
class Plane:
    point: Point3D
    normal: Vector3D


@dataclass
class IntersectionResult:
    success: bool
    points: List[Point3D]
