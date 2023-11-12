import abc
import asyncio
import logging
import typing

from aio_pika import Channel
from aio_pika.abc import AbstractIncomingMessage
from pydantic import BaseModel

from cv_common_library.message_broker.base.connection import get_rabbitmq_channel
from cv_common_library.message_broker.congif import get_rabbitmq_settings

logger = logging.getLogger(__name__)


async def consume_events(
    queue_name: str,
    routing_keys: tuple[str, ...],
    callback: typing.Callable[[AbstractIncomingMessage], typing.Any],
    enable_x_dead_letter: bool,
) -> None:
    channel: Channel = await get_rabbitmq_channel()
    dlq_name = f"{queue_name}.dlq"

    await channel.set_qos(prefetch_count=get_rabbitmq_settings().channel_prefetch_count)  # type: ignore

    # Declare DLQ queue for failed letters
    await channel.declare_queue(
        dlq_name,
        durable=True,
        arguments={"x-max-length": get_rabbitmq_settings().dlq_max_length},
    )

    queue_dead_letter_params: dict[str, typing.Any] | None = None
    if enable_x_dead_letter:
        queue_dead_letter_params = _generate_queue_dead_letter_queue_params(queue_name)

    queue = await channel.declare_queue(
        queue_name, durable=True, arguments=queue_dead_letter_params
    )

    await asyncio.gather(
        *[
            queue.bind(  # type: ignore
                exchange=get_rabbitmq_settings().exchange_name, routing_key=key
            )
            for key in routing_keys
        ]
    )
    await queue.consume(callback)


def _generate_queue_dead_letter_queue_params(queue_name: str) -> dict[str, typing.Any]:
    return {
        "x-dead-letter-exchange": get_rabbitmq_settings().dlq_exchange_name,
        "x-dead-letter-routing-key": queue_name,
    }


MessageSchema = typing.TypeVar("MessageSchema", bound=BaseModel)


class BaseAsyncConsumer(typing.Generic[MessageSchema], metaclass=abc.ABCMeta):
    def __init__(
        self,
        queue_name: str,
        routing_keys: tuple[str, ...],
        enable_x_dead_letter: bool = True,
    ) -> None:
        self._queue_name = queue_name
        self._routing_keys = routing_keys
        self._enable_x_dead_letter = enable_x_dead_letter

    async def consume_events(self) -> None:
        """This method is entrypoint for consuming RMQ messages (consumers)."""
        await consume_events(
            queue_name=self._queue_name,
            routing_keys=self._routing_keys,
            callback=self._process_event,
            enable_x_dead_letter=self._enable_x_dead_letter,
        )

    async def _process_event(self, message: AbstractIncomingMessage) -> None:
        async with message.process(ignore_processed=True):
            try:
                message_schema: MessageSchema = await self._map_message_to_schema(
                    message
                )
                await self._do_staff(message_schema)
            except Exception as e:
                logger.exception(f"Error in {self._queue_name}: {e!s}")
                await message.nack(requeue=False)
            else:
                await message.ack()

    @abc.abstractmethod
    async def _map_message_to_schema(
        self, message: AbstractIncomingMessage
    ) -> MessageSchema:
        ...

    @abc.abstractmethod
    async def _do_staff(
        self, message_schema: MessageSchema, **kwargs: typing.Any
    ) -> typing.Any:
        ...
