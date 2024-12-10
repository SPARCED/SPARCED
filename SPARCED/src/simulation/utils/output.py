#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import numpy as np
import pandas as pd
from utils.combine_results import combine_results


def save_simulation_output(model, simulation_name: str, simulation_number: int,
                           output_sim: str, xoutS_all: np.ndarray, 
                           xoutG_all: np.ndarray, tout_all: np.ndarray) -> None:
    """
    Save simulation output to a txt file

    Parameters:
    - model: model object
    - simulation_name (str): name of the simulation
    - simulation_number (int): number of the simulation
    - output_sim (str): path to the output directory
    - xoutS_all (np.ndarray): array of species values
    - xoutG_all (np.ndarray): array of gene values
    - tout_all (np.ndarray): array of time values

    Returns:
    - None
    """

    # ensure that the last character of the output_sim parameter is a dash,
    # otherwise if verbose ask the user if he meant to add one
    # Species
    assert output_sim[-1] == os.path.sep, f'The output directory must end with a "{os.path.sep}" character.'

    simulation_results = combine_results(model, xoutS_all, xoutG_all, tout_all)

    simulation_results.to_csv(output_sim + simulation_name + '_' + str(simulation_number) + '.txt', sep="\t")

