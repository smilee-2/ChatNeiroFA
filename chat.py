from fastapi import APIRouter, Request, Form, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from gpt import gpt
from models import UserInput

from models import UserModel

router = APIRouter(prefix="/chat",tags=["chat"])

router.mount("/chat_page", StaticFiles(directory="chat_page"), name="style")

templates_chat = Jinja2Templates(directory="chat_page")


@router.post("")
async def request_gpt(request: Request, creds: UserModel = Form()):
    if creds.username == 'denis' and creds.password == "123":
        return templates_chat.TemplateResponse("index.html", {"request": request})
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect login or password")



@router.post('/ask')
async def request_gpt(us_input: UserInput) -> dict:
    print(us_input.user_input)
    return {'msg': await gpt(us_input.user_input)}