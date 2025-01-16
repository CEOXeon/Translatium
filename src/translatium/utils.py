import functools
import warnings
from typing import TypeAlias, Union

############################################################
#                 # DEPRECTATION DECORATOR                 #
############################################################

def deprecated(message, version):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            warnings.warn(
                f"{func.__name__} is deprecated and will be removed in {version}. {message}",
                DeprecationWarning,
                stacklevel=2
            )
            return func(*args, **kwargs)
        return wrapper
    return decorator


############################################################
#                      # TYPE ALIASES                      #
############################################################

TranslationsType: TypeAlias = dict[str, Union[str, "TranslationsType"]]

ConfigType: TypeAlias = dict[str, Union[str, bool]]
