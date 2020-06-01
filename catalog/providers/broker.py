from aiokafka import AIOKafkaProducer
from catalog.event import JSonEvent
import asyncio
from .config import BrokerConfig


class BrokerClient:
    def __init__(self, broker_config: BrokerConfig):
        self.broker_config = broker_config

    def publish(self, queue: str, event: JSonEvent):
        raise NotImplementedError('Abstract Method')


class KafkaClient(BrokerClient):
    def __init__(self, broker_config: BrokerConfig):
        super().__init__(broker_config)
        self.loop = asyncio.get_event_loop()
        self.producer = AIOKafkaProducer(loop=self.loop,
                                         bootstrap_servers=self.broker_config.host)

    async def publish(self, queue: str, event: JSonEvent):
        await self.producer.start()
        try:
            await self.producer.send_and_wait(queue,
                                              event.serialize())
        except Exception as e:
            raise Exception('Error Producing Message')
        finally:
            await self.producer.stop()
