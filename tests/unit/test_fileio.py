import pytest
import os
from src.fileio.reader import STEPReader
from src.fileio.writer import STEPWriter
from src.domain.model import Point3D
from src.exceptions import FileOperationError


def test_validate_nonexistent_file():
    """Test validation of non-existent file."""
    with pytest.raises(FileOperationError) as exc_info:
        STEPReader.validate_file("nonexistent.stp")
    assert "File does not exist" in str(exc_info.value)


def test_validate_wrong_extension():
    """Test validation of file with wrong extension."""
    with pytest.raises(FileOperationError) as exc_info:
        STEPReader.validate_file("test.txt")
    assert "Invalid file format" in str(exc_info.value)


def test_write_intersection_points(output_file):
    """Test writing intersection points to file."""
    points = [Point3D(1.0, 2.0, 3.0), Point3D(4.0, 5.0, 6.0)]

    STEPWriter.write_intersection_points(points, output_file)
    assert os.path.exists(output_file)
    assert os.path.getsize(output_file) > 0
