#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from dataclasses import dataclass
import numpy as np
import pandas as pd

import constants as const

from simulation.modules.RunSPARCED import RunSPARCED
from utils.files_handling import *


# SIMULATION

@dataclass
class Simulation:
    name: str
    output_directory: str | os.PathLike
    duration: float
    is_deterministic: bool = True
    number: int = 0
    verbose: bool = False

    def run(self, model, sbml_file: str, simulation_files: dict[str, str]
            ) -> np.ndarray:
        """
        Run the simulation
        """

        model.setInitialStates(self.initial_conditions)
        if self.verbose:
            print(f"SPARCED VERBOSE: {self.name} n°{self.number}" +
                   " is now ready to run.\n")
        # TODO: handle the case when no simulation files are provided
        genes_file = pd.read_csv(simulation_files[YAML_GENES_REGULATION], header=0, index_col=0, sep='\t')
        omics_file = pd.read_csv(simulation_files[YAML_OMICS_DATA], header=0, index_col=0, sep='\t')
        species_levels, genes_levels, time = RunSPARCED(self.is_deterministic,
                                                        self.duration,
                                                        self.initial_conditions,
                                                        [],
                                                        sbml_model,
                                                        model,
                                                        genes_file,
                                                        omics_file)
        if self.verbose:
            print(f"SPARCED VERBOSE: {self.name} n°{self.number}" +
                   "is now over. Saving results, do not exit.\n")
        self.save(model, species_levels, genes_levels, time)
        if self.verbose:
            print(f"SPARCED VERBOSE: {self.name} n°{self.number}" +
                   "is successfully saved.\n")
        return(species_level)

    def save(self, model, species_levels: np.ndarray,
             genes_levels: np.ndarray, time: np.ndarray) -> None:
    """
    Save results

    Arguments:
        model: The open model file.
        species_levels: The species concentrations to save.
        genes_levels: The genes concentrations to save.
        time: The timepoints corresponding to the measures.

    Returns:
        Nothing.
    """

    # Time
    self._write_data_to_csv("TIME", time)
    # Species
    species_columns = [specie_id for specie_id in model.getStateIds()]
    species_dataframe = pd.DataFrame(data=species_levels,
                                     columms=species_columns)
    self._write_data_to_csv("SPECIES", species_dataframe)
    # Genes
    genes_columns = [specie for _, specie in enumerate(species_columns) \
                    if 'm_' in specie]
    genes_colums = genes_colums[1:] # Skip header
    activated = [gene.replace('m_', 'ag_') for gene in genes_columns]
    inactivated = [gene.replace('m_', 'ig_') for gene in genes_columns]
    genes_columns  np.concatenate((activated, inactivated), axis=None)
    genes_dataframe = pd.DataFrance(data=genes_levels, columns=genes_columns)
    self._write_data_to_csv("GENES", genes_dataframe)

    def _write_data_to_csv(self, content_type: str, data) -> None:
    """
    Write data in CSV format

    Warning:
        This function's purpose is highly targeted for some specific
        cases. Using it beyond the scope it was designed for may result
        in unexpected behabior.
        In case of modifications, please make sure to remain fully
        compatible with the save() function of this class.

    Note:
        Supported `content_type` values are: "GENES", "SPECIES", and
        "TIME". Any other value will result in an error.

    Arguments:
        content_type: The type of the data. See the __Note__ section
                      for the supported strings.
        data: The data to save.

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
    # TODO: handle no number
    file_name = self.name + file_indicator + str(self.number) + file_extension
    file_path = append_subfolder(self.output_directory, file_name)
    if content_type == "TIME": # np.ndarray
        np.savetxt(file_path, data, newline='\t', fmt='%s')
    else: # pd.DataFrame
        data.to_csv(file_path, sep='\t')
    check_path_existence(file_path)

