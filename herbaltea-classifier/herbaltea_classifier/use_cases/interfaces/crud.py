from typing import Generic, TypeVar, Any
from abc import ABC, abstractmethod

from pydantic import BaseModel

from herbaltea_classifier.entities.herbal_tea import (
    HerbalTea,
    HerbalTeaCreateCreateOrUpdate,
)
from herbaltea_classifier.entities.indication import (
    IndicationCreated,
    IndicationCreateOrUpdate,
)

READ_TYPE = TypeVar("READ_TYPE", bound=BaseModel)
CREATE_TYPE = TypeVar("CREATE_TYPE", bound=BaseModel)
UDPATE_TYPE = TypeVar("UDPATE_TYPE", bound=BaseModel)
RESSOURCE_TYPE = TypeVar("RESSOURCE_TYPE")


class CrudResource(Generic[READ_TYPE, CREATE_TYPE, UDPATE_TYPE], ABC):
    @abstractmethod
    def read(self, **kwargs: Any) -> list[READ_TYPE]:
        """Read resources"""

    @abstractmethod
    def create(self, data: CREATE_TYPE, **kwargs: Any) -> list[READ_TYPE]:
        """Create new resources"""

    @abstractmethod
    def update(self, data: UDPATE_TYPE, **kwargs: Any) -> list[READ_TYPE]:
        """Update resources"""


HerbalTeaResource = CrudResource[
    HerbalTea, HerbalTeaCreateCreateOrUpdate, HerbalTeaCreateCreateOrUpdate
]


IndicationResource = CrudResource[
    IndicationCreated, IndicationCreateOrUpdate, IndicationCreateOrUpdate
]


class Crud:
    Herbaltea: HerbalTeaResource
    indication: IndicationResource
