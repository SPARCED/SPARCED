#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import numpy as np
import pandas as pd
from pathlib import Path
import yaml



def convert_excel_to_tsv(f_excel: str) -> None:
    """Convert an Excel file to TSV (SPARCED's standard input format)           

    This function creates a new .txt file at the same location than the passed  
    Excel file.

    Warning:
        This is some old code written four years ago, it hasn't been tested since.

    Arguments:
        f_excel: The Excel sheet path.

    Returns:
        Nothing.
    """

    data = pd.read_excel(f_excel, header=0, index_col=0)
    data.to_csv((f_excel.split("."))[0] + ".txt", sep="\t") 

def load_input_data_config(data_path: str | os.PathLike, yaml_name: str) -> dict[str, str | os.PathLike]:
    """Load input data files paths configuration

    Note:
        File structure is assumed to be organized as follow:
        > model folder
        > data subfolder containing a YAML configuration file describing input
        data organization
        > model compilation and simulation sub-subfolders containing the input
        data files

    Arguments:
        data_path: The input data files folder path.
        yaml_name: The YAML configuration file name.

    Returns:
        A dictionnary containing all the input data file paths.
    """

    # Load data and YAML paths
    yaml_path = append_subfolder(data_path, yaml_name, True)
    # Read input data files structure in YAML configuration file
    with yaml_path.open() as f:
        input_files_configuration = yaml.safe_load(f)
    return(input_files_configuration)

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

