import os

import typer
from rich.console import Console
from rich.table import Table

from .codegen import Deployment, QuixWrap

cli = typer.Typer()

apps = typer.Typer()
cli.add_typer(apps, name="apps")
console = Console()

config_file = os.getenv("CONFIG_FILE", "quix.yaml")
yaml_variables_file = os.getenv("YAML_VARIABLES_FILE", ".quix.yaml.variables")


def expand(item: Deployment):
    res = []
    for var in item.info.variables:
        res.append(
            (
                item.info.name,
                var.name,
                var.type,
                "Y" if var.required else "N",
                str(var.default),
            )
        )
    return res


@apps.command(
    help="Returns a single deployment metadata and allows to generate a python wrapper code from it."
)
def get(
    name: str = typer.Argument(..., help="Name of the application"),
    as_py: bool = typer.Option(
        False,
        help="Flag controlling whether the application spec should be converted to python code.",
    ),
    standalone: bool = typer.Option(
        True,
        help="Flag controlling whether the generate code base code should be included in full or imported.",
    ),
):
    qx = QuixWrap(config_file, yaml_variables_file)
    item = qx.deployment(name=name)
    if as_py:
        typer.echo(item.as_py(standalone=standalone))
        return
    table = Table("Application", "Variable", "Type", "Required", "Default")
    for row in expand(item):
        table.add_row(*row)
    console.print(table)


@apps.command(help="Returns deployment(s) metadata found in a given yaml file.")
def list(name: str = typer.Argument(None, help="Name of the application")):
    qx = QuixWrap(config_file, yaml_variables_file)
    table = Table("Application", "Variable", "Type", "Required", "Default")
    for item in qx.deployments(name=name):
        for row in expand(item):
            table.add_row(*row)
    console.print(table)


if __name__ == "__main__":
    cli()
