from typing import Annotated
from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from src.dependencies import get_msg_brocker_connection
from .config import settings

from pika.adapters.blocking_connection import BlockingChannel


router = APIRouter()

templates = Jinja2Templates(directory=settings.index_templates_dir)


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context={"name": "username"}
    )

@router.get("/send_to_mq")
async def index(msg_broker: Annotated[BlockingChannel, Depends(get_msg_brocker_connection)]):
    msg_broker.basic_publish(
        exchange="",
        routing_key="tasks",
        body="body payload"
    )
    return "sended"


def clb(ch, method, properties, body):
    print(f"RECEIVED {body}")

@router.get("/receive")
async def index(msg_broker: Annotated[BlockingChannel, Depends(get_msg_brocker_connection)]):
    # msg_broker.basic_consume(
    # queue="tasks",
    #  auto_ack=True,
    #   on_message_callback=clb
    #)
    result = msg_broker.basic_get(
        queue="tasks",
        auto_ack=True,
    )
    print(result)
    return result if result else "NO"

