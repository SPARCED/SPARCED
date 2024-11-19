#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from pathlib import Path



def append_subfolder(folder_path: str | os.PathLike, subfolder_name: str) -> str | os.PathLike:
    """Append a subfolder to a folder path

    Arguments:
        folder_path: The folder path.
        subfolder_name: The subfolder name.

    Returns:
        The subfolder's path.
    """

    folder = Path(folder_path)
    check_path_existence(folder)

    subfolder_path = folder / subfolder_name
    return(subfolder_path)

def check_path_existence(path: str | os.PathLike) -> None:
    try:
        if not path.exists():
            raise FileNotFoundError(f"Path not found: {path}")
    except FileNotFoundError as error:
        print(error)
        sys.exit(0)

