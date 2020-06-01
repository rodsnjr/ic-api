from .file import FileClient, S3Client, UploadInfo, DownloadInfo
from .cache import CacheClient, RedisClient
from .broker import BrokerClient, KafkaClient
from .config import FileConfig, CacheConfig, BrokerConfig, Queues
from .config import (build_broker_config, build_file_config,
                     build_cache_config, build_queues)


file_config = build_file_config()
cache_config = build_cache_config()
broker_config = build_broker_config()
queues = build_queues()


if file_config.client == 's3':
    file_client: FileClient = S3Client(file_config)
else:
    raise NotImplementedError(f'FileClient {file_config.client} not Implemented')

if cache_config.client == 'redis':
    cache_client: CacheClient = RedisClient(cache_config)
else:
    raise NotImplementedError(f'CacheClient {cache_config.client} not Implemented')

if broker_config.client == 'kafka':
    broker_client: BrokerClient = KafkaClient(broker_config)
else:
    raise NotImplementedError(f'BrokerClient {broker_config.client} not Implemented')
