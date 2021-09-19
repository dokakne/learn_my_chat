from fastapi import FastAPI, Form, status, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer

from . import db, auth

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()
app.mount("/static", StaticFiles(directory="html"), name="static")

template = Jinja2Templates("app/templates")


@app.get("/", response_class=HTMLResponse)
def get_root():
    return RedirectResponse("/login")


@app.get("/login", response_class=HTMLResponse)
def get_login():
    return template.TemplateResponse("login.html", context={"request": {}})


@app.get("/chat", response_class=HTMLResponse)
def get_chat():
    return template.TemplateResponse(
        "chat.html",
        context={
            "request": {},
            "rooms": db.get_rooms(),
            "selected_room": db.EMPTY_ROOM,
        },
    )


@app.get("/chat/{room_id}/messages")
def get_chat_room_messages(room_id: int):
    return db.get_messages(room_id)


@app.get("/chat/{room_id}", response_class=HTMLResponse)
def get_chat_room(room_id: int):
    return template.TemplateResponse(
        "chat.html",
        context={
            "request": {},
            "rooms": db.get_rooms(),
            "selected_room": db.get_room(room_id),
        },
    )


def get_chat_response(email: str):
    response = RedirectResponse("/chat", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="email", value=auth.get_jwt_token_from_email(email))
    return response


def get_retry_response():
    return RedirectResponse("/login?error=True", status_code=status.HTTP_302_FOUND)


@app.get("/user")
def get_user(token: str = Depends(oauth2_scheme)) -> db.User:
    user = auth.get_user_from_jwt_token(token)
    if user == db.EMPTY_USER:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@app.post("/chat/message")
def post_message(message: db.Message, user: db.User = Depends(get_user)):
    db.set_message(message.copy(update={"user": user.email}))


@app.post("/chat/room")
def post_message(room: db.Room, user: db.User = Depends(get_user)):
    db.set_room(room.copy(update={"user": user.email}))


@app.post("/login")
def post_login(email: str = Form(...), password: str = Form(...)):
    return (
        get_chat_response(email)
        if auth.is_valid_user(email, password)
        else get_retry_response()
    )
