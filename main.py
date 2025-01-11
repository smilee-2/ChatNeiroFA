import uvicorn
from fastapi import FastAPI, Request, Form, HTTPException, status, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import AsyncSession
from chat import router as router_chat
from core.dbhelper import database
from core.schemas import BaseSchemas
from core.crud import create_user
from models import UserModel
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with database.engine.begin() as connect:
        await connect.run_sync(BaseSchemas.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(
    router_chat,
)

app.mount("/auth_page", StaticFiles(directory="auth_page"), name="style")

templates_auth = Jinja2Templates(directory="auth_page")


@app.get("/", tags=['main'])
async def auth_page(request: Request):
    return templates_auth.TemplateResponse("index.html", {"request": request})


@app.post("/register")
async def register_new_user(user: UserModel, session: AsyncSession = Depends(database.session_depend)):
    return await create_user(session=session, user_input=user)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)