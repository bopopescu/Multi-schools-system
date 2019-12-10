from .defaults import defaults


def superuser_check(user):

    if defaults("SUPERUSER_ONLY"):
        return user.is_superuser
    else:
        return False
