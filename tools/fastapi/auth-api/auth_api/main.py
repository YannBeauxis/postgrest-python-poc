from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from jose import jwt
from pydantic import BaseModel
from magic_admin import Magic

from .config import settings


app = FastAPI()
magic = Magic(
    retries=5,
    timeout=5,
    backoff_factor=0.01,
)

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PostTokenInput(BaseModel):
    did_token: str


class PostTokenOutput(BaseModel):
    token: str


@app.post("/token")
async def post_token(data: PostTokenInput) -> PostTokenOutput:
    magic.Token.validate(data.did_token)
    magic.User.get_metadata_by_token(data.did_token).data
    encoded_jwt = jwt.encode(
        # {"role": user_metadata["email"]}, SECRET_KEY, algorithm=ALGORITHM
        {"role": settings.role},
        settings.secret_key,
        algorithm=settings.algorithm,
    )
    return PostTokenOutput(token=encoded_jwt)
