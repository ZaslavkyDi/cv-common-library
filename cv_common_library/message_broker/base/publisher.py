import asyncio
import json
from typing import Any

import aio_pika
from pydantic import BaseModel

from app.message_broker.base.connection import get_rabbitmq_channel


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


async def main() -> None:
    message = {"1": "2"}

    await publish_message(message=message, routing_key="test_r")

    print(" [x] Sent ")


if __name__ == "__main__":
    asyncio.run(main())
