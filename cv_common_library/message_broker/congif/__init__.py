from functools import lru_cache

from app.message_broker.congif.settings import RabbitMQSettings


@lru_cache
def get_rabbitmq_settings() -> RabbitMQSettings:
    return RabbitMQSettings()
