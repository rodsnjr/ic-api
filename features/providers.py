from typing import Iterable

from catalog.event import JSonEvent
from catalog.providers import (CacheClient, FileClient,
                               BrokerClient, DownloadInfo, UploadInfo)


class MockCacheClient(CacheClient):
    def __init__(self):
        super(MockCacheClient, self).__init__(None)
        self.objects = {}

    async def add(self, key: str, value: dict):
        self.objects[key] = value
        return value

    async def add_many(self, keys: Iterable[str], values: Iterable[dict]):
        for k, v in zip(keys, values):
            await self.add(k, v)

    async def get(self, key: str) -> dict:
        return self.objects[key]

    def clear(self):
        self.objects = {}


class MockFileClient(FileClient):
    def __init__(self):
        super(MockFileClient, self).__init__(None)
        self.uploads = {}

    async def upload_bytes(self, upload_info):
        self.uploads[upload_info.dst_file_name] = upload_info.buffer
        return True

    async def upload_file(self, upload_info: UploadInfo):
        pass

    async def download_bytes(self, download_info):
        return self.uploads[download_info.src_file_name]

    async def download_file(self, download_info: DownloadInfo):
        pass

    def clear(self):
        self.uploads = {}


class MockBrokerClient(BrokerClient):
    def __init__(self):
        super(MockBrokerClient, self).__init__(None)
        self.events = {}

    async def publish(self, queue: str, event: JSonEvent):
        if queue in self.events:
            self.events[queue].append(event)
        else:
            self.events[queue] = [event]

    def clear(self):
        self.events = {}
