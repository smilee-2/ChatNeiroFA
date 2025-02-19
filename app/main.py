from pathlib import Path
from contextlib import asynccontextmanager

import uvicorn
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import crud
from app.config.config import engine
from app.database.schemas import BaseSchemas
from app.endpoints.endpoints_chat import router as router_chat
from app.database.depends import user_by_id
from app.endpoints.models import UserModel


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connect:
        await connect.run_sync(BaseSchemas.metadata.create_all)
    yield


BASE_DIR = Path(__file__).parent.parent

app = FastAPI(lifespan=lifespan)
app.include_router(router_chat)
app.mount('/auth_page', StaticFiles(directory=f'{BASE_DIR}/auth_page'), name='style')

templates_auth = Jinja2Templates(directory=f'{BASE_DIR}/auth_page')


@app.get('/', tags=['main'])
async def auth_page(request: Request):
    return templates_auth.TemplateResponse('index.html', {'request': request})


@app.get('/get_user/{user_id}', tags=['main'])
async def get_user(user: UserModel = Depends(user_by_id)):
    return user


@app.post('/register', tags=['main'])
async def register_new_user(user: UserModel):
    return await crud.create_user(user_input=user)


@app.delete('/delete/{user_id}', tags=['main'], status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user: UserModel = Depends(user_by_id)):
    await crud.delete_user(user=user)


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
