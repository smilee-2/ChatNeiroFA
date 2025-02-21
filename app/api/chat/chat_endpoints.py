from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Request, HTTPException, status, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBearer

from app.depends import gpts, depends
from app.api.models import UserInput

BASE_DIR = Path(__file__).parent.parent.parent.parent
http_bearer = HTTPBearer()

router = APIRouter(prefix='/chat', tags=['Chat'])
router.mount('/chat_page', StaticFiles(directory=f'{BASE_DIR}/chat_page'), name='style')

templates_chat = Jinja2Templates(directory=f'{BASE_DIR}/chat_page')


@router.post('/')
def chat_page(user: Annotated[str, Depends(depends.get_current_user)], request: Request):
    if user:
        return templates_chat.TemplateResponse('index.html', {'request': request})
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect login or password')


@router.post('/ask')
async def request_gpt(user: Annotated[str, Depends(depends.get_current_user)], us_input: UserInput) -> dict:
    return {'msg': await gpts(us_input.user_input)}
