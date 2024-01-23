from cv_common_library.message_brokers.kafka.base.consumer import BaseKafkaConsumer
from cv_common_library.registry.registry import Registry

consumers: Registry[str, BaseKafkaConsumer] = Registry()
