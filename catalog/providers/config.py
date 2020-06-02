class FileConfig:
    def __init__(self, client='s3'):
        self.client = client


class CacheConfig:
    def __init__(self, client='redis'):
        self.client = client
        self.host = None


class BrokerConfig:
    def __init__(self, client='kafka', host=None):
        self.client = client
        self.host = host


class Queues:
    def __init__(self, catalog='catalog'):
        self.catalog = catalog


def build_file_config(context) -> FileConfig:
    if context == 'mock':
        return FileConfig(client=context)
    return FileConfig()


def build_cache_config(context) -> CacheConfig:
    if context == 'mock':
        return CacheConfig(client=context)
    return CacheConfig()


def build_broker_config(context) -> BrokerConfig:
    if context == 'mock':
        return BrokerConfig(client=context)
    return BrokerConfig()


def build_queues(context) -> Queues:
    if context == 'mock':
        return Queues()
    return Queues()
