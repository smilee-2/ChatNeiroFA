from pathlib import Path

from fastapi import APIRouter, Request, Form, HTTPException, status, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


from app.database import crud
from app.depends import gpts
from .models import UserInput, UserModel

BASE_DIR = Path(__file__).parent.parent.parent
router = APIRouter(prefix='/chat', tags=['chat'])
router.mount('/chat_page', StaticFiles(directory=f'{BASE_DIR}/chat_page'), name='style')

templates_chat = Jinja2Templates(directory=f'{BASE_DIR}/chat_page')

# TODO
@router.post('')
async def chat_page(request: Request, creds: UserModel = Form()):
    # username = await crud.user_exists_by_name(session=session, username=creds.username, password=creds.password)
    # password = await crud.user_exists_by_password(session=session, password=creds.password)
    if await crud.user_exists_by_name(username=creds.username, password=creds.password):
        return templates_chat.TemplateResponse("index.html", {"request": request})
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect login or password")


@router.post('/ask')
async def request_gpt(us_input: UserInput) -> dict:
    return {'msg': await gpts(us_input.user_input)}
