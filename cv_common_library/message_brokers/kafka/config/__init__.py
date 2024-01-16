from functools import cache

from cv_common_library.message_brokers.kafka.config.settings import ApacheKafkaGlobalSettings


@cache
def get_kafka_global_settings() -> ApacheKafkaGlobalSettings:
    return ApacheKafkaGlobalSettings()


@cache
def get_kafka_global_settings() -> ApacheKafkaGlobalSettings:
    return ApacheKafkaGlobalSettings()
