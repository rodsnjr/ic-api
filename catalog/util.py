from uuid import uuid4


def generate_uid() -> str:
    return str(uuid4())


def clean_null_terms(d):
    return {
        k: v
        for k, v in d.items()
        if v is not None
    }
