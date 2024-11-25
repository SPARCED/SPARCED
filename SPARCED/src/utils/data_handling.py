#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import numpy as np
import pandas as pd
import petab


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

def load_input_data_file(f_input: str | os.PathLike) -> np.ndarray:
    """Load the given input data file

    Load an input data file structured as tab separated.

    Arguments:
        f_input: The input data file.

    Returns:
        A numpy array containing the data.
    """

    data = np.array([np.array(line.strip().split("\t"))
                    for line in open(f_input)], dtype="object")
    return(data)

def load_petab_conditions_file(file: str | os.PathLike, condition_id: str) -> dict[str, str]:
    """Load a PEtab conditions file for a specific condition

    Arguments:
        file: The path to the PEtab conditions file.
        condition_id: The ConditionId of the row to load.

    Returns:
        A dictionnary structured as key: parameter / value: value.
    """

    # ConditionId is mandatory
    if not condition_id:
        raise ValueError("Missing ConditionId.")
        return(None)
    raw_data = petab.v1.get_condition_df(file)
    try:
        petab.v1.check_condition_df(raw_data)
    except AssertionError as error:
        print(error)
        return(None)
    data = {}
    for k in raw_data.keys():
        if k != "conditionName":
            data[k] = raw_data[k][condition_id]
    return(data)

