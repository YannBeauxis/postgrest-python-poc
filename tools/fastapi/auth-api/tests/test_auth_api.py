from pytest import MonkeyPatch
from fastapi.testclient import TestClient
from jose import jwt
from magic_admin.resources import User, Token

from auth_api import app, settings

client = TestClient(app)


def test_post_token(monkeypatch: MonkeyPatch) -> None:
    did_token = "fake_token"

    email = "dev@yannbeauxis.net"

    class MockedMagic:
        def __init__(self, _did_token: str) -> None:
            assert _did_token == did_token

        data = {"email": email}

    monkeypatch.setattr(Token, "validate", lambda self, x: None)
    monkeypatch.setattr(User, "get_metadata_by_token", MockedMagic)

    response = client.post("/token", json={"did_token": did_token})
    assert response.status_code == 200
    resp = response.json()
    encoded_jwt = resp["token"]
    assert jwt.decode(
        encoded_jwt, settings.secret_key, algorithms=[settings.algorithm]
    ) == {"role": settings.role}
