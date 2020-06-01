from features import fixture as fxt


def after_scenario(context, scenario):
    if 'dont_clear' not in scenario.tags:
        fxt.BROKER_CLIENT.clear()
        fxt.CACHE_CLIENT.clear()
        fxt.FILE_CLIENT.clear()
