import abc
import logging
from typing import ClassVar

from confluent_kafka import Consumer, KafkaError, KafkaException, Message
from pydantic import BaseModel

from cv_common_library.message_brokers.kafka.base import (
    kafka_consumer_settings,
    kafka_global_settings,
)

logger = logging.getLogger(__name__)


class BaseKafkaConsumer(metaclass=abc.ABCMeta):
    """
    A basic Kafka consumer class.

    Attributes:
        topics (list[str]): A list of topics to subscribe to.
        consumer_state (bool): The state of the consumer. True if the consumer is running, False otherwise.

    Methods:
        start_consuming(): Starts consuming messages from the subscribed topics.

    Examples:
        topics = ["topic1", "topic2"]
        consumer_1 = BaseKafkaConsumer(
            group_id="m-consumer-group-1",
            auto_offset_reset="latest",
            topics_to_subscribe=topics,
        )
        await consumer_1.start_consuming()
    """

    _END_OF_PARTITION_EVENT_MESSAGE_TEMPLATE: ClassVar[
        str
    ] = "{topic} [{partition}] reached end at offset {offset}\n"

    def __init__(
        self,
        group_id: str,
        topics_to_subscribe: list[str],
        bootstrap_servers: str | None = None,
        auto_offset_reset: str | None = "latest",
    ) -> None:
        config = {
            "bootstrap.servers": bootstrap_servers
            or kafka_global_settings().bootstrap_servers,
            "group.id": group_id,
            "auto.offset.reset": auto_offset_reset
            or kafka_global_settings().consumer_default_auto_offset_reset,
        }
        self._kafka_consumer = Consumer(config)
        self._topics = topics_to_subscribe
        self._consumer_state: bool = True

    def __del__(self) -> None:
        if self._kafka_consumer:
            self._consumer_state = False
            self._kafka_consumer.close()

    @property
    def topics(self) -> list[str]:
        return self._topics

    @property
    def consumer_state(self) -> bool:
        return self._consumer_state

    async def start_consuming(self) -> None:
        """
        Starts consuming messages from the subscribed topics.

        The consumer will keep running until its state is set to False.
        """
        logger.info(f"Starting consuming messages from Kafka on topics: {self._topics}")
        self._kafka_consumer.subscribe(self._topics)

        while self._consumer_state:
            message: Message | None = self._kafka_consumer.poll(
                timeout=kafka_consumer_settings().default_poll_timeout
            )
            if message is None:
                continue

            if message.error():
                await self.handle_message_error(message)
                continue

            await self.process_message(message)

    async def handle_message_error(self, message):
        if message.error().code() == KafkaError._PARTITION_EOF:
            # End of partition event
            end_of_partition_message = (
                self._END_OF_PARTITION_EVENT_MESSAGE_TEMPLATE.format(
                    topic=message.topic(),
                    partition=message.partition(),
                    offset=message.offset(),
                )
            )
            logger.info(end_of_partition_message)
        elif message.error():
            raise KafkaException(message.error())

    @abc.abstractmethod
    async def process_message(self, message: Message) -> None:
        pass
