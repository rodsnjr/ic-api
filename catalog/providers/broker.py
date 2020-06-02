from aiokafka import AIOKafkaProducer
import asyncio
from .config import BrokerConfig
from json import loads


class BrokerClient:
    def __init__(self, broker_config: BrokerConfig):
        self.broker_config = broker_config

    def publish(self, queue: str, event: bytes, key: bytes = None):
        raise NotImplementedError('Abstract Method')


class MockBrokerClient(BrokerClient):
    def __init__(self, config):
        super(MockBrokerClient, self).__init__(config)
        self.queues = dict()

    def __decode(self, event):
        try:
            event_decoded = event.decode('utf8').replace("'", '"')
            return loads(event_decoded)
        except Exception as e:
            print(e)

    async def publish(self, queue: str, event: bytes, key: bytes = None):
        event = self.__decode(event)
        if queue in self.queues:
            if key is not None:
                self.queues[queue][key].append(event)
            else:
                self.queues[queue].append(event)
        else:
            if key is not None:
                self.queues[queue] = {
                    key: [event]
                }
            else:
                self.queues[queue] = [event]

    def clear(self):
        self.queues = dict()

    def get_queue(self, queue):
        return self.queues[queue]

    def get_any(self, queue, key=None):
        if isinstance(self.queues[queue], list):
            pick = self.queues[queue][0]
            return 0, pick
        elif isinstance(self.queues[queue], dict):
            if key is None:
                key, value = self.queues[queue].popitem()
                return key, value[0]
            else:
                key, value = self.queues[queue][key]
                return key, value[0]


class KafkaClient(BrokerClient):
    def __init__(self, broker_config: BrokerConfig):
        super().__init__(broker_config)
        self.loop = asyncio.get_event_loop()
        self.producer = AIOKafkaProducer(loop=self.loop,
                                         bootstrap_servers=self.broker_config.host)

    async def publish(self, queue: str, event: bytes, key: bytes = None):
        await self.producer.start()
        try:
            await self.producer.send_and_wait(topic=queue,
                                              value=event,
                                              key=key)
        except Exception as e:
            raise Exception('Error Producing Message')
        finally:
            await self.producer.stop()
