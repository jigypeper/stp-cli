from src import read_file


def test_file_read_success():
    result = read_file("./random-shape.stp")
    assert result == (1, "File read successfully")


def test_file_read_non_existent():
    result = read_file("./random-shapes.stp")
    assert result == (2, "File cannot be found")


def test_file_read_wrong_format():
    result = read_file("./README.md")
    assert result == (3, "Incorrect file type, is this a step file?")
