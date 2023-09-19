from __future__ import annotations

from typing import TypeVar, Any, Union, Type, get_args, Tuple
import urllib

import requests
from pydantic import BaseModel
from jose import jwt

from herbaltea_classifier.entities.herbal_tea import (
    HerbalTea,
    HerbalTeaCreateCreateOrUpdate,
)
from herbaltea_classifier.entities.indication import (
    IndicationCreated,
    IndicationCreateOrUpdate,
)
from herbaltea_classifier.use_cases.interfaces.crud import (
    CrudResource,
    Crud,
)

from pydantic import BaseSettings


class PostgrestSettings(BaseSettings):
    secret_key: Union[str, None] = None
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    role: str = "editor"

    class Config:
        env_prefix = "postgrest_client_"


settings = PostgrestSettings()


class CustomRequests:
    def __init__(self) -> None:
        self._headers: dict[str, Any] = {}
        self.add_token_to_headers()

    def get(self, *args: Any, **kwargs: Any) -> requests.Response:
        self.update_headers(kwargs)
        return requests.get(*args, **kwargs)

    def post(self, *args: Any, **kwargs: Any) -> requests.Response:
        self.update_headers(kwargs)
        return requests.post(*args, **kwargs)

    def patch(self, *args: Any, **kwargs: Any) -> requests.Response:
        self.update_headers(kwargs)
        return requests.patch(*args, **kwargs)

    def update_headers(self, kwargs: dict[str, Any]) -> None:
        kwargs.setdefault("headers", {}).update(self._headers)

    def add_token_to_headers(self) -> None:
        if settings.secret_key:
            token = jwt.encode(
                {"role": settings.role},
                settings.secret_key,
                algorithm=settings.algorithm,
            )
            self._headers["Authorization"] = f"Bearer {token}"


GET_TYPE = TypeVar("GET_TYPE", bound=BaseModel)
POST_TYPE = TypeVar("POST_TYPE", bound=BaseModel)
PATCH_TYPE = TypeVar("PATCH_TYPE", bound=BaseModel)


class PostgrestResource(CrudResource[GET_TYPE, POST_TYPE, PATCH_TYPE]):
    def __set_name__(self, owner: PostgrestCrud, name: str) -> None:
        self.name = name

    def __get__(
        self,
        obj: PostgrestCrud | None,
        objtype: Union[Type[Crud], None] = None,
    ) -> (
        CrudResource[GET_TYPE, POST_TYPE, PATCH_TYPE]
        | PostgrestResource[GET_TYPE, POST_TYPE, PATCH_TYPE]
    ):
        if obj:
            self.api_url = obj.api_url
            self._requests = obj._requests
        return self

    def read(self, *args: str, **kwargs: Any) -> list[GET_TYPE]:
        url = f"{self.api_url}/{self.name}" + self._get_filters(*args, **kwargs)
        response = self._requests.get(url)
        response.raise_for_status()
        data = self._format_response(response)
        return data

    def create(
        self, data: POST_TYPE, *args: str, **kwargs: dict[str, Any]
    ) -> list[GET_TYPE]:
        response = self._requests.post(
            f"{self.api_url}/{self.name}",
            json=data.dict(),
            headers=self.mutation_headers,
        )
        response.raise_for_status()
        return self._format_response(response)

    def update(
        self, data: PATCH_TYPE, *args: str, **kwargs: dict[str, Any]
    ) -> list[GET_TYPE]:
        data_dict = self._patch_model(**data.dict()).dict()
        url = f"{self.api_url}/{self.name}" + self._get_filters(*args, **kwargs)
        response = self._requests.patch(
            url, json=data_dict, headers=self.mutation_headers
        )
        response.raise_for_status()
        return self._format_response(response)

    @staticmethod
    def _get_filters(*args: str, **kwargs: Any) -> str:
        if args or kwargs:
            filters = "&".join(
                f"{key}=eq.{urllib.parse.quote_plus(str(value))}"
                for key, value in kwargs.items()
            )
            filters += "&".join(args)
            return "?" + filters
        return ""

    @property
    def mutation_headers(self) -> dict[str, str]:
        return {"prefer": "return=representation"}

    @property
    def _get_model(self) -> Type[GET_TYPE]:
        return self._annotated_classes[0]

    @property
    def _patch_model(self) -> Type[PATCH_TYPE]:
        return self._annotated_classes[2]

    @property
    def _annotated_classes(
        self,
    ) -> Tuple[Type[GET_TYPE], Type[POST_TYPE], Type[PATCH_TYPE]]:
        return get_args(self.__orig_class__)  # type: ignore

    def _format_response(self, response: requests.Response) -> list[GET_TYPE]:
        return [self._get_model(**data) for data in response.json()]


class PostgrestCrud(Crud):
    def __init__(self, url: str):
        self.api_url = url
        self._requests = CustomRequests()

    herbaltea = PostgrestResource[
        HerbalTea, HerbalTeaCreateCreateOrUpdate, HerbalTeaCreateCreateOrUpdate
    ]()
    indication = PostgrestResource[
        IndicationCreated, IndicationCreateOrUpdate, IndicationCreateOrUpdate
    ]()
