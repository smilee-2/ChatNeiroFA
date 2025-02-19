from pathlib import Path

from fastapi import APIRouter, Request, Form, HTTPException, status, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


from app.database import crud
from app.depends import gpts
from app.api.models import UserInput, UserModel

BASE_DIR = Path(__file__).parent.parent.parent.parent

router = APIRouter(prefix='/chat', tags=['chat'])
router.mount('/chat_page', StaticFiles(directory=f'{BASE_DIR}/chat_page'), name='style')

templates_chat = Jinja2Templates(directory=f'{BASE_DIR}/chat_page')

# TODO
@router.post('')
async def chat_page(request: Request, creds: UserModel = Form()):
    user = await crud.get_user_by_name(username=creds.username)
    if user:
        return templates_chat.TemplateResponse("index.html", {"request": request})
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect login or password")


@router.post('/ask')
async def request_gpt(us_input: UserInput) -> dict:
    return {'msg': await gpts(us_input.user_input)}
