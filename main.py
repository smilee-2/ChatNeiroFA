import uvicorn
from fastapi import FastAPI, Request, Form, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from authconfig import security

from chat import router as router_chat

app = FastAPI()
app.include_router(
    router_chat,
)

app.mount("/auth_page", StaticFiles(directory="auth_page"), name="style")

templates_auth = Jinja2Templates(directory="auth_page")


@app.get("/")
async def read_root(request: Request):
    return templates_auth.TemplateResponse("index.html", {"request": request})



if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)