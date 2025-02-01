import functools
import warnings
from typing import TypeAlias, Union

############################################################
#                       # DECORATORS                      #
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

def convert_error_type(std_error, custom_error, **decorator_kwargs):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except std_error as e:
                # Merge decorator_kwargs and kwargs, with kwargs taking precedence
                error_kwargs = {**decorator_kwargs, **kwargs}
                raise custom_error(e, **error_kwargs)
        return wrapper
    return decorator

############################################################
#                      # TYPE ALIASES                      #
############################################################

TranslationsType: TypeAlias = dict[str, Union[str, "TranslationsType"]]

ConfigType: TypeAlias = dict[str, Union[str, bool]]
