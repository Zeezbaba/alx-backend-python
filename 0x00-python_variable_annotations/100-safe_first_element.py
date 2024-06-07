#!/usr/bin/env python3
"""Module that return the first element of a list"""

from typing import Sequence, Any, Union


def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    """return first element"""
    if lst:
        return lst[0]
    else:
        return None
