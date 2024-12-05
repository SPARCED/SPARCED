#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

import constants as const
import Sparced.Simulation

from utils.files_handling import *


def save_simulation_data_to_csv(simulation: Sparced.Simulation,
                                content_type: str, data) -> None:
    """
    Save data to CSV format

    Warning:
        This function's purpose is highly targeted for some specific
        cases. Using it beyond the scope it was designed for may result
        in unexpected behabior.
        In case of modifications, please make sure to remain fully
        compatible with the save_simulation_output() function.

    Note:
        Supported `content_type` values are: "GENES", "SPECIES", and
        "TIME". Any other value will result in an error.

    Arguments:
        simulation: The Sparced.Simulation instance associated to the
                    data.
        content_type: The type of the data. See the __Note__ section
                      for the supported strings.
        dataframe: The data to save.

    Returns:
        Nothing.
    """

    file_indicator = ""
    file_extension = ""
    match content_type:
        case "GENES":
            file_indicator = const.GENES_FILE_INDICATOR
            file_extension = const.GENES_FILE_EXTENSION
        case "SPECIES":
            file_indicator = const.SPECIES_FILE_INDICATOR
            file_extension = const.SPECIES_FILE_EXTENSION
        case "TIME":
            file_indicator = const.TIME_FILE_INDICATOR
            file_extension = const.TIME_FILE_EXTENSION
        case _:
            raise ValueError("Unknown content type.")
    file_name = simulation.name + file_indicator + str(simulation.number) \
                + file_extension
    file_path = append_subfolder(simulation.output_directory, file_name)
    if content_type == "TIME": # np.ndarray
        np.savetxt(file_path, data, newline='\t', fmt='%s')
    else: # pd.DataFrame
        data.to_csv(file_path, sep='\t')
    check_path_existence(species_file_path)

def save_simulation_output(model,
                           simulation: Sparced.Simulation,
                           species_levels: np.ndarray,
                           genes_levels: np.ndarray,
                           time: np.ndarray) -> None:
    """
    Save simulation results

    Arguments:
        model: The open model file.
        simulation: The Sparced.Simulation instance.
        species_levels: The species concentrations to save.
        genes_levels: The genes concentrations to save.
        time: The timepoints corresponding to the levels measures.

    Returns:
        Nothing.
    """
    # Time
    save_simulation_dataframe_to_csv(simulation, "TIME", time)
    # Species
    species_columns = [specie_id for specie_id in model.getStateIds()]
    species_dataframe = pd.DataFrame(data=species_levels,
                                     columms=species_columns)
    save_simulation_data_to_csv(simulation, "SPECIES", species_dataframe)
    # Genes
    genes_columns = [specie for _, specie in enumerate(species_columns) \
                    if 'm_' in specie]
    genes_colums = genes_colums[1:] # Skip header
    activated = [gene.replace('m_', 'ag_') for gene in genes_columns]
    inactivated = [gene.replace('m_', 'ig_') for gene in genes_columns]
    genes_columns  np.concatenate((activated, inactivated), axis=None)
    genes_dataframe = pd.DataFrance(data=genes_levels, columns=genes_columns)
    save_simulation_data_to_csv(simulation, "GENES", genes_dataframe)

