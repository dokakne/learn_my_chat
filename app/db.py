from typing import Any, Union
from pydantic import BaseModel
import datetime


class User(BaseModel):
    id: int = -1
    name: str = ""
    email: str
    password: str


class Room(BaseModel):
    id: int = -1
    name: str
    user: str
    messages: int = 0


class Message(BaseModel):
    id: int = -1
    room_id: int
    user: str
    message: str
    when: datetime.datetime = datetime.datetime.now()


LONG_TEXT = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."
MEDIUM_TEXT = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a "
SMALL_TEXT = "Lorem Ipsum is simply dummy text of the printing and"

EMPTY_USER = User(email="", password="")
EMPTY_ROOM = Room(name="", user="")
EMPTY_MESSAGE = Message(room_id=-1, user="", message="")

USERS: list[User] = []
ROOMS: list[Room] = []
MESSAGES: list[Message] = []

Item = Union[User, Message, Room]


def get_next_id(items: list[Item]) -> int:
    return items[-1].id + 1 if items else 0


def set_item(items: list[Item], item: Item) -> None:
    items.append(item.copy(update={"id": get_next_id(items)}))


def set_message(message: Message) -> None:
    return set_item(MESSAGES, message)


def set_room(room: Room) -> None:
    return set_item(ROOMS, room)


def get_rooms() -> list[Room]:
    return ROOMS


def set_user(user: User) -> None:
    set_item(USERS, user)


def get_item(items: list[Item], item_id: int, default_item: Item):
    return next((item for item in items if item.id == item_id), default_item)


def get_room(room_id: int) -> list[Room]:
    return get_item(ROOMS, room_id, EMPTY_ROOM)


def get_user(email: str) -> User:
    return next((item for item in USERS if item.email == email), EMPTY_USER)


def get_messages(room_id: int) -> list[Message]:
    return (message for message in MESSAGES if message.room_id == room_id)
