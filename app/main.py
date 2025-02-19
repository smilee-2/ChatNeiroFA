from pathlib import Path
from contextlib import asynccontextmanager

import uvicorn
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request

from app.config.config import engine
from app.database.schemas import BaseSchemas
from app.api import router_chat, router_auth, router_users


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connect:
        await connect.run_sync(BaseSchemas.metadata.create_all)
    yield


BASE_DIR = Path(__file__).parent.parent

app = FastAPI(lifespan=lifespan)
app.include_router(router_chat)
app.include_router(router_auth)
app.include_router(router_users)

app.mount('/auth_page', StaticFiles(directory=f'{BASE_DIR}/auth_page'), name='style')

templates_auth = Jinja2Templates(directory=f'{BASE_DIR}/auth_page')


@app.get('/', tags=['main'])
async def auth_page(request: Request):
    return templates_auth.TemplateResponse('index.html', {'request': request})


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
