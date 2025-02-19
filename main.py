import typer
from typing_extensions import Annotated
from src.fileio.reader import STEPReader
from src.geometry.engine import GeometryEngine
from src.fileio.writer import STEPWriter
from src.domain.model import Point3D, Vector3D, Plane
from src.exceptions import STPCliError


def main(
    in_step: Annotated[str, typer.Option(help="Path to the step file")],
    in_plane: Annotated[
        tuple[float, float, float, float, float, float],
        typer.Option(help="Coordinates and normal vector for plane (x,y,z,nx,ny,nz)"),
    ],
    output_file: Annotated[
        str, typer.Option(help="Path to output STEP file")
    ] = "intersection.stp",
):
    """CLI tool to find intersections between a STEP model and a plane."""
    try:
        # Create domain objects
        px, py, pz, nx, ny, nz = in_plane
        plane = Plane(point=Point3D(px, py, pz), normal=Vector3D(nx, ny, nz))
        plane.validate()

        # Read model
        model = STEPReader.read_model(in_step)

        # Find intersections
        engine = GeometryEngine(model)
        result = engine.find_intersections(plane)

        if result.success:
            # Write results
            STEPWriter.write_intersection_points(result.points, output_file)
            typer.echo(f"Intersections found and written to {output_file}")
            for i, point in enumerate(result.points, 1):
                typer.echo(f"Point {i}: ({point.x:.3f}, {point.y:.3f}, {point.z:.3f})")
        else:
            typer.echo("No intersections found")

    except STPCliError as e:
        typer.echo(f"Error: {str(e)}", err=True)
        raise typer.Exit(code=1)
    except Exception as e:
        typer.echo(f"Unexpected error: {str(e)}", err=True)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    typer.run(main)
