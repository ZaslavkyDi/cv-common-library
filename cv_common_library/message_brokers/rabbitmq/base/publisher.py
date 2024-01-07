import asyncio
import json
from typing import Any

import aio_pika
from pydantic import BaseModel

from cv_common_library.message_brokers.rabbitmq.base.connection import (
    get_rabbitmq_channel,
)


async def publish_message(
    routing_key: str,
    message: dict[str, Any] | BaseModel,
) -> None:
    if isinstance(message, dict):
        message = json.dumps(message)
    elif isinstance(message, BaseModel):
        message = message.model_dump_json()
    else:
        raise ValueError(f"Get not send unknown RMQ message type: {type(message)}")

    channel = await get_rabbitmq_channel()
    return await channel.default_exchange.publish(
        message=aio_pika.Message(body=message.encode()),
        routing_key=routing_key,
    )
