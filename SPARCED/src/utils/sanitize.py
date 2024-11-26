#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys


def sanitize_popsize(popsize: int, abort_on_error: bool=False) -> int:
    """Ensure validity of population size

    Arguments:
        popsize: The population size.

    Returns:
        The population size if valid.
    """

    try:
        assert int(popsize) > 0
    except:
        print("ERROR: Cell population size should be superior to zero (0). \
                Current population size is: {size}."
              .format(size = popsize))
        if abort_on_error:
            print("Aborting now.")
            sys.exit(0)
        else:
            print("Setting automatically population size to one (1).")
            popsize = 1
    return(int(popsize))

