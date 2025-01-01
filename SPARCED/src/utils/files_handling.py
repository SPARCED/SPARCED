#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import pandas as pd
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

def convert_excel_to_tsv(f_excel: str) -> None:
    """Convert an Excel file to TSV (SPARCED's standard input format)

    This function creates a new .txt file at the same location than the
    passed Excel file.

    Warning:
        This is some old code written four years ago, it hasn't been
        tested since.

    Arguments:
        f_excel: The Excel sheet path.

    Returns:
        Nothing.
    """

    data = pd.read_excel(f_excel, header=0, index_col=0)
    data.to_csv((f_excel.split("."))[0] + ".txt", sep="\t")

