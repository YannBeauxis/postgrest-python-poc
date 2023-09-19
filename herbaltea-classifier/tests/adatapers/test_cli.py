from typing import Any

from rich.console import Console
from requests_mock import Mocker

from herbaltea_classifier.entities.herbal_tea import HerbalTea
from herbaltea_classifier.adapters.cli import find_herbal_teas
from herbaltea_classifier.use_cases.interfaces.crud import HerbalTeaResource


printed = []


def mock_console_print(self: Any, arg: Any) -> Any:
    printed.append(arg)


Console.print = mock_console_print  # type: ignore


def test_find_herbal_teas(
    herbal_tea_resource: HerbalTeaResource, requests_mock: Mocker
) -> None:
    data = [
        HerbalTea(
            name_botanical="Rhodiolae roseae rhizoma et radix", name_fr="Rodhiole"
        ).dict()
    ]
    requests_mock.get(
        "http://localhost:3001/herbaltea",
        json=data,
    )
    find_herbal_teas()
    assert len(printed[0].rows) == len(data)
