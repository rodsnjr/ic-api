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


def build_file_config() -> FileConfig:
    return FileConfig()


def build_cache_config() -> CacheConfig:
    return CacheConfig()


def build_broker_config() -> BrokerConfig:
    return BrokerConfig()


def build_queues() -> Queues:
    return Queues()
