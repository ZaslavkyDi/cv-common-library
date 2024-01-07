import logging
import socket
from typing import Any, Self

from confluent_kafka import Producer

from cv_common_library.message_brokers.kafka.base import kafka_global_settings

logger = logging.getLogger(__name__)


class KafkaProducer:
    """
    A basic Kafka producer class.

    Attributes:
        _kafka_producer (Producer): The Kafka producer instance.
        _topic (str): The topic to produce messages to.

    Methods:
        create_instance(cls, topic: str, client_id: str | None = None): Factory method for Kafka producer.
        send(value: str | bytes, key: str | None = None): Sends a message to the topic.

    Examples:
        producer = KafkaProducer.create_instance(topic="topic1")
        producer2 = KafkaProducer.create_instance(topic="topic2")
        producer.send("1")
        producer2.send("1")
    """

    def __init__(self, bootstrap_servers: str, client_id: str, topic: str) -> None:
        config = {
            "bootstrap.servers": bootstrap_servers,
            "client.id": client_id,
        }
        self._kafka_producer = Producer(config)
        self._topic = topic

    def __del__(self) -> None:
        # push all queued messages to topic
        if self._kafka_producer:
            self._kafka_producer.flush()

    @classmethod
    def create_instance(cls, topic: str, client_id: str | None = None) -> Self:
        """
        Factory method for Kafka producer.

        Args:
            topic (str): Topic to send the message to.
            client_id (str, optional): If None the "socket.gethostname()" will be provided.

        Returns:
            KafkaProducer: A new KafkaProducer instance.
        """
        return cls(
            bootstrap_servers=kafka_global_settings().bootstrap_servers,
            client_id=client_id or socket.gethostname(),
            topic=topic,
        )

    def send(
        self,
        value: str | bytes,
        key: str | None = None,
    ) -> None:
        """
        Sends a message to the topic.

        Args:
            value (str | bytes): The message to send.
            key (str, optional): The key associated with the message.
        """
        self._kafka_producer.produce(
            self._topic, key=key, value=value, on_delivery=self._ack_message_on_delivery
        )

    @staticmethod
    def _ack_message_on_delivery(message: Any | None, err: Any | None) -> None:
        if err is not None:
            logger.warning(err)
        else:
            logger.info(message)
