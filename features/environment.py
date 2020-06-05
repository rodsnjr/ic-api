from catalog.providers import cache_client, broker_client, file_client


def after_scenario(context, scenario):
    if 'dont_clear' not in scenario.tags:
        broker_client.clear()
        cache_client.clear()
        file_client.clear()

