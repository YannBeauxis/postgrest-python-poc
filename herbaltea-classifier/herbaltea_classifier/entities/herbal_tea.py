from pydantic import AnyHttpUrl, Field, BaseModel


class HerbalTeaCreateCreateOrUpdate(BaseModel):
    name_botanical: str
    name_fr: str | None = None
    monograph_url: AnyHttpUrl | None = None
    indication_raw: str | None = None
    gbif_id: int | None = None
    indication_ids: list[int] = Field(default_factory=list)


class HerbalTea(HerbalTeaCreateCreateOrUpdate):
    id: int | None = None
