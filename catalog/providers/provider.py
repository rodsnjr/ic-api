from .config import FileConfig, CacheConfig, BrokerConfig, Queues
from .config import (build_broker_config, build_file_config,
                     build_cache_config, build_queues)
from .file import FileClient, MockFileClient, S3Client
from .cache import CacheClient, MockCacheClient, RedisClient
from .broker import BrokerClient, MockBrokerClient, KafkaClient


class ConfigProvider:
    def __init__(self, context='mock'):
        self.context = context
        self.file_config: FileConfig = build_file_config(context)
        self.cache_config: CacheConfig = build_cache_config(context)
        self.broker_config: BrokerConfig = build_broker_config(context)
        self.queues: Queues = build_queues(context)


class Provider:
    CACHE_CLIENTS = dict(
        redis=RedisClient,
        mock=MockCacheClient
    )

    FILE_CLIENTS = dict(
        s3=S3Client,
        mock=MockFileClient
    )

    BROKER_CLIENTS = dict(
        kafka=KafkaClient,
        mock=MockBrokerClient
    )

    def __init__(self, config_provider):
        self.config_provider = config_provider
        self._file_client: FileClient = None
        self._cache_client: CacheClient = None
        self._broker_client: BrokerClient = None

    def file_client(self) -> FileClient:
        if self._file_client is None:
            file_config = self.config_provider.file_config
            if file_config.client in Provider.FILE_CLIENTS:
                file_client_cls = Provider.FILE_CLIENTS[file_config.client]
                self._file_client: FileClient = file_client_cls(file_config)
            else:
                raise NotImplementedError(f'FileClient {file_config.client} not Implemented')
        return self._file_client

    def cache_client(self) -> CacheClient:
        if self._cache_client is None:
            cache_config = self.config_provider.cache_config
            if cache_config.client in Provider.CACHE_CLIENTS:
                cache_client_cls = Provider.CACHE_CLIENTS[cache_config.client]
                self._cache_client: CacheClient = cache_client_cls(cache_config)
            else:
                raise NotImplementedError(f'CacheClient {cache_config.client} not Implemented')
        return self._cache_client

    def broker_client(self) -> BrokerClient:
        if self._broker_client is None:
            broker_config = self.config_provider.broker_config
            if broker_config.client in Provider.BROKER_CLIENTS:
                broker_client_cls = Provider.BROKER_CLIENTS[broker_config.client]
                self._broker_client = broker_client_cls(broker_config)
        return self._broker_client

    def queues(self):
        return self.config_provider.queues
