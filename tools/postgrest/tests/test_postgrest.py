import pytest

from requests.exceptions import HTTPError

from herbaltea_classifier.adapters.postgrest import HmpcCrud
from herbaltea_classifier.entities.indication import (
    IndicationCreateOrUpdate,
    IndicationCreated,
)


def test_get_anon_success(client_anon: HmpcCrud) -> None:
    assert client_anon.indication.get() == []


def test_post_anon_error(client_anon: HmpcCrud) -> None:
    with pytest.raises(HTTPError):
        client_anon.indication.post(IndicationCreateOrUpdate(name="test"))


def test_patch_anon_error(client_anon: HmpcCrud) -> None:
    with pytest.raises(HTTPError):
        client_anon.indication.patch(IndicationCreateOrUpdate(name="test"))


@pytest.fixture
def indication_test_item(client_editor: HmpcCrud) -> IndicationCreated:
    data = IndicationCreateOrUpdate(name="test")
    # TODO: fix type error
    return client_editor.indication.post(data)[0]  # type: ignore


def test_post_editor_success(
    client_anon: HmpcCrud, indication_test_item: IndicationCreateOrUpdate
) -> None:
    resp = client_anon.indication.get()
    assert len(resp) == 1
    assert resp[0].name == "test"


def test_patch_editor_success(
    client_editor: HmpcCrud, indication_test_item: IndicationCreateOrUpdate
) -> None:
    client_editor.indication.patch(IndicationCreateOrUpdate(name="test2"))
    resp = client_editor.indication.get()
    assert len(resp) == 1
    assert resp[0].name == "test2"
