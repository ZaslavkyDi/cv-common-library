from functools import cache

from cv_common_library.message_brokers.kafka.config.settings import (
    ApacheKafkaGlobalSettings,
    ApacheKafkaConsumerSettings,
)


@cache
def kafka_global_settings() -> ApacheKafkaGlobalSettings:
    return ApacheKafkaGlobalSettings()


@cache
def kafka_consumer_settings() -> ApacheKafkaConsumerSettings:
    return ApacheKafkaConsumerSettings()
