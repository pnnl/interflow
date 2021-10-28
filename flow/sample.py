import numpy as np
import pandas as pd


def add(x: float, y: float) -> float:
    """Return the sum of x and y.

    :param x:                       float value
    :type x:                        float value

    :param y:                       float value
    :type y:                        float value

    :return:                        sum of x and y as a float

    """

    if type(x) == str:
        msg = f"'x' must be numeric your type was {type(x)}"
        raise TypeError(msg)

    return x + y
