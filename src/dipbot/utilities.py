# -*- coding: utf-8 -*-
"""encapsulates helper functions for dipbot

"""

import os
from typing import Union


def get_env_var_checked(
    varname: str, default: Union[str, bool] = False
) -> Union[str, bool]:
    """gets the value of an environment variable. raises an exception and
returns False if the variable is not set, unless the optional veriable
default has been set, in which case it returns that instead.

    """
    value = os.getenv(varname)
    try:
        assert value != None and value != ""
    except AssertionError:
        if default != False:
            return default
        else:
            print(f"{varname} unset! terminating...")
            return False
    return value
