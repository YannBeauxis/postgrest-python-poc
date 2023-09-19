from typing import Any, Annotated, Optional

import typer
from rich.console import Console
from rich.table import Table

from herbaltea_classifier.entities.herbal_tea import HerbalTea
from herbaltea_classifier.use_cases.herbal_tea import HerbalTeaUseCase
from herbaltea_classifier.adapters.postgrest import PostgrestCrud


console = Console()

app = typer.Typer()
postgrest_client = PostgrestCrud("http://localhost:3001")


@app.command()
def find_herbal_teas(name_fr: Annotated[Optional[str], typer.Option()] = None) -> None:
    kwargs: dict[str, Any] = {}
    if name_fr is not None:
        kwargs["name_fr"] = name_fr
    herbal_teas: list[HerbalTea] = postgrest_client.herbaltea.read(**kwargs)

    table = Table("Vernacular Name", "Botanical Name")
    for herbal_tea in herbal_teas:
        if herbal_tea.name_fr is not None:
            table.add_row(herbal_tea.name_fr, herbal_tea.name_botanical)
    console.print(table)


@app.command()
def create_all() -> None:
    use_case = HerbalTeaUseCase(postgrest_client.herbaltea)
    use_case.create_herbal_teas()


if __name__ == "__main__":
    app()
