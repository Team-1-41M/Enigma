from fastapi import APIRouter

from server.src.core.settings import AUTH_ROUTER_PREFIX, SIGN_UP_URL, SIGN_IN_URL, SIGN_OUT_URL, ME_URL

router = APIRouter(prefix=AUTH_ROUTER_PREFIX)


@router.post(SIGN_UP_URL)
async def sign_up():
    pass


@router.post(SIGN_IN_URL)
async def sign_in():
    pass


@router.post(SIGN_OUT_URL)
async def sign_out():
    pass


@router.get(ME_URL)
async def me():
    pass
