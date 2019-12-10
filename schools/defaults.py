from django.conf import settings

hash = {
    "SUPERUSER_ONLY": True,
}


def defaults(key: str):
    """Try to get a setting from project settings.
    If empty or doesn't exist, fall back to a value from defaults hash."""

    if hasattr(settings, key):
        val = getattr(settings, key)
    else:
        val = hash.get(key)
    return val
