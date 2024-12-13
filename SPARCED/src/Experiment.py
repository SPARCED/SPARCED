#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import importlib
import numpy as np
import pandas as pd

import constants as const
from Simulation import Simulation as SparcedSimulation

from compilation.amici_scripts.create import amici_create_folder
from compilation.sbml_scripts.create import build_sbml_model_path
from utils.data_handling import *
from utils.files_handling import *


# CUSTOM ERRORS

class NegativeNumberOfReplicates(ValueError):
    def __init__(self, message: str, nb_replicates: int):
        self.message = message
        self.nb_replicates = int(nb_replicates)

    def __str__(self):
        return(f"SPARCED ERROR: Negative number of replicates.\n"
             + f"Number of replicates: {self.nb_replicates}\n"
             + f"Error: {self.message}\n")

# EXPERIMENT

class Experiment:
    def __init__(self,
                 name: str,
                 experiements_directory: str | os.PathLike,
                 model_name: str,
                 model_path: str | os.PathLike,
                 simulation_files: dict[str, str]):
        # General settings
        self.name = name
        self.path = append_subfolder(experiments_directory, self.name)
        self.configuration = self.load_configuration_file(self.path,
                            self.name + const.DEFAULT_CONFIG_FILES_EXTENSION)
        # External data
        self.model_name = model_name
        self.amici_path = amici_create_folder(model_name, model_path)
        self.sbml_path = build_sbml_model_path(model_name, model_path)
        self.simulation_files = simulation_files
        # Configuration unpacking
        self.exchange
        self.nb_replica = self.sanitize_nb_replicates(int(
                    self.configuration[const.YAML_EXPERIMENT_NB_REPLICATES])
        # TODO: Add stamp to output_directory name if necessary
        self.output_directory = append_subfolder(self.configuration[
                                    const.YAML_EXPERIMENT_OUTPUT_DIRECTORY,
                                    self.name])
        self.verbose = self.configuration[const.YAML_EXPERIMENT_VERBOSE]

    def run(self):
        sys.path.insert(0, os.path.abspath(self.amici_path))
        # TODO: fix the import on the next line to avoid messing up with paths
        model_module = importlib.import_module(experiment.model_name)
        model = model_module.getModel()
        if self.verbose:
            print(f"SPARCED VERBOSE: Success loading model {model_name}.\n")
        model.setTimepoints(np.linspace(0, self.exchange, 2))
        species_initial_conditions = load_species_from_sbml(self.sbml)
        cell_number = 1
        while cell_number <= self.nb_replica:
            for step in self.configuration[const.YAML_EXPERIMENT_PROTOCOL]:
                protocol = step[1] # Skip name
                print(protocol)
                #simulation = SparcedSimulation(NAME, self.output_directory, DURATION, IS_DETERMINISTIC, cell_number, self.verbose)

            
            # Apply perturbations
            # Create a Simulation that matches
            # Run that simulation
            # Store concentrations levels
        #del simulation
        cell_number += 1

    def sanitize_nb_replicates(self, nb_replicates: int) -> int:
        """Sanitize number of replicates

        Arguments:
            nb_replicates: The number of replicates.

        Returns:
            The corresponding sanitized number of replicates.
        """

        try:
            if int(nb_replicates) <= 0:
                raise NegativeNumberOfReplicates(
                                "Automatically setting to one replicate.\n",
                                nb_replicates)
        except NegativeNumberOfReplicates as error:
            print(error)
            nb_replicates = 1
        return(nb_replicates)

