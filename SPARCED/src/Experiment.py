#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import importlib
import numpy as np

import constants as const
from Simulation import Simulation as SparcedSimulation

from compilation.amici_scripts.creation import amici_create_folder
from compilation.sbml_scripts.creation import build_sbml_model_path
from utils.data_handling import *
from utils.files_handling import *


# CUSTOM ERRORS

class NegativeNumberOfReplicates(ValueError):
    def __init__(self, message: str, nb_replicates: int):
        self.message = message
        self.nb_replicates = int(nb_replicates)

    def __str__(self):
        return("SPARCED ERROR: Negative number of replicates.\n"
             + f"Number of replicates: {self.nb_replicates}\n"
             + f"Error: {self.message}\n")

# EXPERIMENT

class Experiment:
    def __init__(self,
                 name: str,
                 experiments_directory: str | os.PathLike,
                 model_name: str,
                 model_path: str | os.PathLike,
                 simulation_files: dict[str, str]):
        # General settings
        self.name = name
        self.path = append_subfolder(experiments_directory, self.name)
        self.configuration = load_configuration_file(self.path,
                        self.name + const.DEFAULT_CONFIG_FILES_EXTENSION)
        # External data
        self.model_name = model_name
        self.amici_path = amici_create_folder(model_name, model_path)
        self.sbml_path = build_sbml_model_path(model_name, model_path)
        self.simulation_files = simulation_files
        # Configuration unpacking
        self.exchange = self.configuration[const.YAML_EXPERIMENT_EXCHANGE]
        self.nb_replicates = self.sanitize_nb_replicates(int(
                    self.configuration[const.YAML_EXPERIMENT_NB_REPLICATES]))
        # TODO: Add stamp to output_directory name if necessary
        self.output_directory = append_subfolder(self.configuration[
                                    const.YAML_EXPERIMENT_OUTPUT_DIRECTORY],
                                    self.name)
        self.verbose = self.configuration[const.YAML_EXPERIMENT_VERBOSE]

    def apply_perturbations(self,
                            species,
                            perturbations_file,
                            perturbations_id) -> dict[str, float]:
        perturbations = load_petab_conditions_file(perturbations_file,
                                                   perturbations_id)
        for p_name, p_value in perturbations.items():
            species[p_name] = p_value
        return(species)

    def extract_species_initial_conditions(self, species: dict[str, float]
                                            ) -> np.ndarray:
        initial_conditions = []
        for value in species.values():
            initial_conditions.append(value)
        return(initial_conditions)

    def load_model_module(self, model_name, amici_path, verbose):
        sys.path.insert(0, os.path.abspath(amici_path))
        # TODO: fix the import on the next line to avoid messing up with paths
        model_module = importlib.import_module(model_name)
        model = model_module.getModel()
        if verbose:
            print("SPARCED VERBOSE: Success loading model "
                + f"{self.model_name}.\n")
        return(model)

    def run(self):
        model = self.load_model_module(self.model_name,
                                       self.amici_path,
                                       self.verbose)
        model.setTimepoints(np.linspace(0, self.exchange, 2))
        species = load_species_from_sbml(self.sbml_path)
        cell_number = 1
        while cell_number <= self.nb_replicates:
            for step in self.configuration[const.YAML_EXPERIMENT_PROTOCOL]:
                protocol = step[1] # Skip step name
                simulation = SparcedSimulation(
                                protocol[const.YAML_PROTOCOL_NAME],
                                self.output_directory,
                                protocol[const.YAML_PROTOCOL_DURATION],
                                protocol[const.YAML_PROTOCOL_IS_DETERMINISTIC],
                                cell_number,
                                self.verbose)
                perturbations_file = append_subfolder(
                                self.path,
                                protocol[const.YAML_PROTOCOL_PERTURBATIONS])
                species = self.apply_perturbations(
                                species,
                                perturbations_file,
                                protocol[const.YAML_PROTOCOL_PERTURBATIONS_ID])
                initial_conditions = self.extract_species_initial_conditions(species)
                model.setInitialStates(initial_conditions)
                if self.verbose:
                    print("SPARCED VERBOSE: "
                        + f"{protocol[const.YAML_PROTOCOL_NAME]} "
                        + f"n°{cell_number} is now ready to run.\n")
                print(simulation)
                species = simulation.run(model, self.sbml_path, initial_conditions, self.simulation_files)
                del simulation
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

