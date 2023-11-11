from pydantic_settings import BaseSettings, SettingsConfigDict


class RabbitMQSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="rabbitmq_")

    host: str = "localhost"
    port: int = 5672
    user_name: str = "guest"
    user_password: str = "guest"

    exchange_name: str = "global_topic"
    dlq_exchange_name: str = "global_topic_dlx"
    channel_prefetch_count: int = 5
    dlq_max_length: int = 50

    @property
    def message_broker_url(self) -> str:
        return f"amqp://{self.user_name}:{self.user_password}@{self.host}:{self.port}/"
