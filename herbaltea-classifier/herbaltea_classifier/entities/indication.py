from pydantic import BaseModel


class IndicationCreateOrUpdate(BaseModel):
    name: str
    description: str | None = None


class Indication(IndicationCreateOrUpdate):
    id: int | None


class IndicationCreated(Indication):
    id: int
