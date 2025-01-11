from fastapi import APIRouter, Request, Form, HTTPException, status, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import AsyncSession
from core import crud
from core.dbhelper import database
from gpt import gpts
from models import UserInput, UserModel
from authconfig import security


router = APIRouter(prefix="/chat",tags=["chat"])

router.mount("/chat_page", StaticFiles(directory="chat_page"), name="style")

templates_chat = Jinja2Templates(directory="chat_page")


@router.post("")
async def chat_page(request: Request, creds: UserModel = Form(), session: AsyncSession = Depends(database.session_depend)):
    # username = await crud.user_exists_by_name(session=session, username=creds.username, password=creds.password)
    # password = await crud.user_exists_by_password(session=session, password=creds.password)
    if await crud.user_exists_by_name(session=session, username=creds.username, password=creds.password):
        return templates_chat.TemplateResponse("index.html", {"request": request})
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect login or password")


@router.post('/ask')
async def request_gpt(us_input: UserInput) -> dict:
    print(us_input.user_input)
    return {'msg': await gpts(us_input.user_input)}