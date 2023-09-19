from typing import Any, Callable, get_args, Type, Generic, TypeVar, Tuple

from pytest import fixture
from pydantic import BaseModel

from herbaltea_classifier.entities.herbal_tea import (
    HerbalTea,
    HerbalTeaCreateCreateOrUpdate,
)
from herbaltea_classifier.entities.indication import (
    Indication,
    IndicationCreateOrUpdate,
)
from herbaltea_classifier.use_cases.scrapers import plant_url_scraper


def make_get_result_similar_mocked() -> Callable[[str], list[str]]:
    original_function = plant_url_scraper.get_result_similar
    called_once = [False]

    def get_result_similar_mocked(url: str) -> list[str]:
        if called_once[0]:
            return []
        called_once[0] = True
        return list(original_function(url))[:2]

    return get_result_similar_mocked


plant_url_scraper.get_result_similar = make_get_result_similar_mocked()


# class CrudResource(Generic[READ_TYPE, CREATE_TYPE, UDPATE_TYPE], ABC):

READ_TYPE = TypeVar("READ_TYPE", bound=BaseModel)
CREATE_TYPE = TypeVar("CREATE_TYPE", bound=BaseModel)
UDPATE_TYPE = TypeVar("UDPATE_TYPE", bound=BaseModel)


class ResourceMocked(
    Generic[READ_TYPE, CREATE_TYPE, UDPATE_TYPE],
    # CrudResource[READ_TYPE, CREATE_TYPE, UDPATE_TYPE],
):
    def __init__(self) -> None:
        self._resources: dict[int, READ_TYPE] = {}

    def read(self, **kwargs: Any) -> list[READ_TYPE]:
        if kwargs:
            return self._filter_resources(**kwargs)
        return list(self._resources.values())

    def create(self, data: CREATE_TYPE, **kwargs: Any) -> list[READ_TYPE]:
        herbal_tea_id = len(self._resources)
        resource = self._read_model(**data.dict(), id=herbal_tea_id)
        self._resources[herbal_tea_id] = resource
        return [resource]

    def update(self, data: UDPATE_TYPE, **kwargs: Any) -> list[READ_TYPE]:
        resources = self._filter_resources(**kwargs)
        for resource in resources:
            for key, value in data:
                setattr(resource, key, value)
        return resources

    def _filter_resources(self, **kwargs: Any) -> list[READ_TYPE]:
        return [
            resource
            for resource in self._resources.values()
            if all(getattr(resource, key) == value for key, value in kwargs.items())
        ]

    @property
    def _annotated_classes(
        self,
    ) -> Tuple[Type[READ_TYPE], Type[CREATE_TYPE], Type[UDPATE_TYPE]]:
        return get_args(self.__orig_class__)  # type: ignore

    @property
    def _read_model(self) -> Type[READ_TYPE]:
        return self._annotated_classes[0]


HerbalTeaResourceMocked = ResourceMocked[
    HerbalTea, HerbalTeaCreateCreateOrUpdate, HerbalTeaCreateCreateOrUpdate
]


@fixture
def herbal_tea_resource() -> HerbalTeaResourceMocked:
    return HerbalTeaResourceMocked()


IndicationResourceMocked = ResourceMocked[
    Indication, IndicationCreateOrUpdate, IndicationCreateOrUpdate
]


@fixture
def indication_resource() -> IndicationResourceMocked:
    return IndicationResourceMocked()
