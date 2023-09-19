from sqlalchemy import MetaData
from sqlalchemy.dialects import postgresql
from sqlmodel import (
    SQLModel,
    Field,
    Column,
    String,
)

from herbaltea_classifier.entities.herbal_tea import HerbalTea as HerbalTeaEntity
from herbaltea_classifier.entities.indication import Indication as IndicationEntity

metadata = MetaData(schema="api")


class BaseModel(SQLModel):
    metadata = metadata

    id: int | None = Field(default=None, primary_key=True)


class Indication(BaseModel, IndicationEntity, table=True):
    pass


class HerbalTea(BaseModel, HerbalTeaEntity, table=True):
    indication_ids: list[int] = Field(
        default_factory=list, sa_column=Column(postgresql.ARRAY(String()))
    )
