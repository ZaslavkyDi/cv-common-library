from aio_pika import Channel, Connection, ExchangeType, connect

from cv_common_library.message_brokers.rabbitmq.congif import get_rabbitmq_settings

__CONNECTION: Connection | None = None
__CHANNEL: Channel | None = None


async def get_rabbitmq_connection() -> Connection:
    global __CONNECTION
    await __init_connection()

    return __CONNECTION


async def get_rabbitmq_channel() -> Channel:
    await __init_channel()
    return __CHANNEL


async def setup_connection() -> None:
    await __init_connection()
    await __init_channel()


async def teardown_connection() -> None:
    global __CONNECTION, __CHANNEL

    if __CHANNEL:
        await __CHANNEL.close()
        __CHANNEL = None

    if __CONNECTION:
        await __CONNECTION.close()
        __CONNECTION = None


async def __init_connection() -> None:
    global __CONNECTION
    if not __CONNECTION or __CONNECTION.is_closed:
        __CONNECTION = await connect(get_rabbitmq_settings().message_broker_url)


async def __init_channel() -> None:
    global __CHANNEL
    if __CHANNEL:
        return

    connection = await get_rabbitmq_connection()
    __CHANNEL = await connection.channel()

    __CHANNEL.default_exchange = await __CHANNEL.declare_exchange(
        name=get_rabbitmq_settings().exchange_name,
        type=ExchangeType.TOPIC,
        durable=True,
    )
    __CHANNEL.dlq_default_exchange = await __CHANNEL.declare_exchange(
        name=get_rabbitmq_settings().dlq_exchange_name,
        type=ExchangeType.TOPIC,
        durable=True,
    )
