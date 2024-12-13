#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import numpy as np
from yaml import safe_load

import constants as const

from utils.data_handling import load_input_data_file, load_configuration_file
from utils.files_handling import *


# CUSTOM ERRORS

class InvalidModelName(ValueError):
    def __init__(self, messagei: str, model_name: str):
        self.message = message
        self.model_name = model_name

    def __str__(self):
        return(f"SPARCED ERROR: Invalid model name.\n"
             + f"Name: {self.model_name}\n"
             + f"Error: {self.message}\n")

class EmptyModelName(InvalidModelName):
    pass


# MODEL

class Model:
    """Systems biology mathematical model definition as an object

    Attributes:
        name: The name of the model.
        path: The path to the folder containing the model definition.
        configuration: A dictionnary representing the configuration
                       of the model storage.
        data_location: The location of the folder containing all the
                       input data files.
        compilation_config: A subset of the configuration dictionnary
                            dedicated to compilation.
        compilation_data_path: The location of the folder containing
                               all the input data files required for
                               compilation.
        compilation_files: A dictionnary containing all the input files
                           required for compilation.
        compartments: An array containing the compartments names,
                      volumes and annotations.

        Methods:
            load_configuration()
            load_compartments()
            load_compilation_files()
            sanitze_name()
            set_name()
            validate_name()
    """

    def __init__(self,
                 name=const.DEFAULT_MODEL_NAME,
                 models_directory=const.DEFAULT_MODELS_DIRECTORY,
                 config_name=const.DEFAULT_CONFIG_FILE):
        # General settings
        self.name = self.set_name(name)
        self.path = append_subfolder(models_directory, self.name)
        self.configuration = self.load_configuration(self.path, config_name)
        self.data_location = append_subfolder(self.path,
                                self.configuration[const.YAML_DATA_LOCATION])
        # Compilation
        self.compilation_config = \
                            self.configuration[const.YAML_COMPILATION_KEYWORD]
        self.compilation_data_path = append_subfolder(
                self.data_location,
                self.compilation_config[const.YAML_COMPILATION_DATA_LOCATION])
        check_path_existence(self.compilation_data_path)
        self.compilation_files = self.load_files_path(
                    self.compilation_data_path,
                    self.compilation_config[const.YAML_COMPILATION_FILES])
        self.compartments = self.load_compartments(
                            self.compilation_files[const.YAML_COMPARTMENTS])
        # Simulation (Optional)
        if const.YAML_SIMULATION_KEYWORD in self.configuration:
            self.simulation_config = \
                            self.configuration[const.YAML_SIMULATION_KEYWORD]
            self.simulation_data_path = append_subfolder(
                self.data_location,
                self.simulation_config[const.YAML_SIMULATION_DATA_LOCATION])
            check_path_existence(self.simulation_data_path)
            self.simulation_files = self.load_files_path(
                        self.simulation_data_path,
                        self.simulation_config[const.YAML_SIMULATION_FILES])
        # Experiments (Optional)
        if const.YAML_EXPERIMENTS_KEYWORD in self.configuration:
            self.experiments_config = \
                            self.configuration[const.YAML_EXPERIMENTS_KEYWORD]
            self.experiments_data_path = append_subfolder(
                self.data_location,
                self.experiments_config[const.YAML_EXPERIMENTS_DATA_LOCATION])
            check_path_existence(self.experiments_data_path)
            # Experiment name (Optional)
            if const.YAML_EXPERIMENT_NAME in self.experiments_config:
                self.experiment_name = \
                    self.experiments_config[const.YAML_EXPERIMENT_NAME]

    def load_compartments(self, path: str | os.PathLike) -> np.ndarray:
        """Load compartments from a PEtab file

        Note:
            Compartments' file structure is expected to be as follow:
            > First row: header
            > First column: compartments names.
            > Second column: compartments volumes.
            > Third column: compartments annotation.

        Arguments:
            path: The path towards the compartments input file,
                  structured as specified in the __Note__.

        Returns;
            An array representing contents of the input compartments
            file.
        """

        check_path_existence(path)
        compartments = load_input_data_file(path)
        return(compartments)

    def load_files_path(self, path: str | os.PathLike, files: dict[str, str]
                        ) -> dict[str, str | os.PathLike]:
        """Load input file paths

        Note:
            Dictionnary structure is expected to be key: file type /
            value: file name
            For example: species -> my_species.txt

        Arguments:
            path: The path towards the input data files.
            files: A dictionnary structured as stated in the __Note__
                   section.

        Returns:
            The same dictionnary structured as key: file type / value:
            file path.
        """

        # TODO: adjust for multiple files
        for file_type, file_name in files.items():
            if file_name != None:
                files[file_type] = append_subfolder(path, file_name)
                # Do not check existence of files that will be created upon
                # compilation TODO: change to a list to handle several files
                if file_type != const.YAML_OUTPUT_PARAMETERS:
                    check_path_existence(files[file_type])
        return(files)

    def sanitize_name(self, name: str) -> str:
        """ Sanitize model name

        Note:
            Model name cannot be empty.
            Model name should not contain a dash '-' character. This is
            because Antimony cannot handle this character.

        Warning:
            The replacement of dash '-' characters by underscore '_'
            characters might result into breakage of some further
            functionalities.

        Arguments:
            name: The name.

        Returns:
            The corresponding sanitized name.
        """

        try:
            if not name:
                raise EmptyModelName("No model name provided.\n", name)
            elif '-' in name:
                raise InvalidModelName("Dash '-' character not supported.\n", name)
        except EmptyModelName as error:
            print(error)
            sys.exit(0)
        except InvalidModelName as error:
            print(error)
            name = name.replace('-', '_')
        return(name)

