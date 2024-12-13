#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from dataclasses import dataclass
import numpy as np
import pandas as pd

import constants as const

from simulation.RunSPARCED import RunSPARCED
from utils.combine_results import combine_results
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

    def run(self, model, sbml_file: str, initial_conditions, simulation_files: dict[str, str]
            ) -> np.ndarray:
        """
        Run the simulation
        """

        # TODO: handle the case when no simulation files are provided
        # TODO: pass content of those simulation files, we could load this only once
        genes_file = pd.read_csv(simulation_files[const.YAML_GENES_REGULATION], header=0, index_col=0, sep='\t')
        omics_file = pd.read_csv(simulation_files[const.YAML_OMICS_DATA], header=0, index_col=0, sep='\t')
        species_levels, genes_levels, time = RunSPARCED(self.is_deterministic,
                                                        self.duration,
                                                        initial_conditions,
                                                        [],
                                                        sbml_file,
                                                        model,
                                                        genes_file,
                                                        omics_file)
        if self.verbose:
            print(f"SPARCED VERBOSE: {self.name} n°{self.number} " +
                   "is now over. Saving results, do not exit.\n")
        self.save(model, species_levels, genes_levels, time)
        if self.verbose:
            print(f"SPARCED VERBOSE: {self.name} n°{self.number} " +
                   "is successfully saved.\n")
        return(species_levels)

    def save(self, model, species_levels: np.ndarray,
             genes_levels: np.ndarray, time: np.ndarray) -> None:
        """
        Save simulation output to a csv file

        Arguments:
            model: The open model file.
            species_levels: The species concentrations to save.
            genes_levels: The genes concentrations to save.
            time: The timepoints corresponding to the measures.

        Returns:
            Nothing.
        """

        file_name = self.name + '_' + str(self.number) + const.DEFAULT_OUTPUT_FILE_EXTENSION
        if not Path.exists(self.output_directory):
            Path(self.output_directory).mkdir(parents=True)
        file_path = append_subfolder(self.output_directory, file_name)
        simulation_results = combine_results(model,
                                             species_levels, genes_levels, time)
        simulation_results.to_csv(file_path, sep='\t')

