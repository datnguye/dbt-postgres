from typing import Any
from fastapi import APIRouter
from schemas import token

router = APIRouter()

@router.post("/login/access-token", response_model=token.Token)
def login_access_token() -> Any:
    """
    [Not Implemented] OAuth2 compatible token login, get an access token for future requests
    """
    pass