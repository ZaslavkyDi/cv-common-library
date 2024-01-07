from functools import lru_cache

from cv_common_library.message_brokers.rabbitmq.congif.settings import RabbitMQSettings


@lru_cache
def get_rabbitmq_settings() -> RabbitMQSettings:
    return RabbitMQSettings()
