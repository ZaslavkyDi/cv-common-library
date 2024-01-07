from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ApacheKafkaGlobalSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="kafka_global_")

    bootstrap_servers: str = Field(
        default="localhost:9094",
        description="Kafka servers: inout format 'localhost1:9092, localhost2:9092'",
    )


class ApacheKafkaConsumerSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="kafka_consumer_")

    default_auto_offset_reset: Literal["earliest", "latest", None] = Field(
        default="latest",
        description="""
            'earliest': automatically reset the offset to the earliest offset
            'latest': automatically reset the offset to the latest offset
        """,
    )
    default_poll_timeout: float = Field(
        default=1.0, description="""How often message will be polled, in seconds."""
    )
    default_min_commit_count: int = Field(
        default=1, description="""How often message consumer commits message."""
    )
