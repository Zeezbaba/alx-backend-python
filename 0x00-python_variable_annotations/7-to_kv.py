#!/usr/bin/env python3
"""a type-annotated function to_kv that takes a string k and
an int OR float v as arguments and returns a tuple.
"""

from typing import Union, Tuple


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """returns a string as first element and second
    element will be the square of the int/float v
    and should be annotated as a float.
    """
    return (k, float(v ** 2))
