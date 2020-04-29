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
            print(f"{varname} unset!")
            return False
    return value


def get_env_var_or_exit(env_var: str) -> str:
    """consumes a string corresponding to an environment variable. if the
environment variable is set, produces it as a string. if it's not,
sends the signal exit(1).

    """
    value = get_env_var_checked(env_var)
    try:
        assert value != False
    except AssertionError:
        print("terminating...")
        exit(1)
    return value
