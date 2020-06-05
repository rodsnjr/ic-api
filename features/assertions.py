from catalog.providers import file_client, cache_client, broker_client

_FILTER_KEYS = ['colors', 'detections', 'scenes', 'objects']


def has_uploaded(keys):
    for key in keys:
        assert key in file_client.uploads


def has_cached(keys):
    for key in keys:
        assert key in cache_client.objects


def has_filters(catalog):
    all_filters = []
    for k in _FILTER_KEYS:
        all_filters.append(catalog.get(k, None) is None)
    assert any(all_filters)


def has_events(queue, key, size=0,
               events_assertions: callable = None):
    events = broker_client.get_queue(queue)
    for event_key, events_in_key in events.items():
        assert key == event_key
        assert len(events_in_key) == int(size)
        for event in events_in_key:
            events_assertions(event)
