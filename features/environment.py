from features import fixture as fxt


def after_scenario(context, scenario):
    if 'dont_clear' not in scenario.tags:
        fxt.broker_client.clear()
        fxt.cache_client.clear()
        fxt.file_client.clear()
