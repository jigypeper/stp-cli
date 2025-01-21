import typer
from typing_extensions import Annotated
from typing import Optional, Tuple
from src import read_file, read_plane
from OCC.Core.STEPControl import STEPControl_Reader


def main(
    in_step: Annotated[str, typer.Option(help="Path to the step file")],
    in_plane: Annotated[
        tuple[float, float, float, float, float, float],
        typer.Option(
            help="Coordinates and normal vector for plane (x,y,z,nx,ny,nz). "
            "Note: must be entered as 6 space seperated numbers"
        ),
    ],
    output_file: Annotated[
        str, typer.Option(help="Path to output STEP file")
    ] = "intersection.stp",
):
    """
    CLI tool to find intersections between a STEP model and a plane.

    Args:
        in_step: Path to input STEP file
        in_plane: Tuple of plane coordinates (x,y,z) and normal vector (nx,ny,nz)
        output_file: Path to output STEP file for intersections
    """
    # Read the STEP file
    status, message = read_file(in_step)
    typer.echo(f"STEP file read status: {message}")
    if status != 1:
        raise typer.Exit(code=1)

    # Load the model and check for intersections
    step_reader = STEPControl_Reader()
    step_reader.ReadFile(in_step)

    typer.echo("Checking for intersections...")
    try:
        success, points = read_plane(step_reader, in_plane, output_file)

        if success:
            typer.echo(f"Intersections found and written to {output_file}")
            typer.echo("Intersection points:")
            for i, point in enumerate(points, 1):
                typer.echo(
                    f"  Point {i}: ({point[0]:.3f}, {point[1]:.3f}, {point[2]:.3f})"
                )
        else:
            typer.echo("No intersections found. No output STEP file created.")
            raise typer.Exit(code=1)

    except ValueError as e:
        typer.echo(f"Error: {str(e)}", err=True)
        raise typer.Exit(code=1)
    except Exception as e:
        typer.echo(f"Unexpected error: {str(e)}", err=True)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    typer.run(main)
