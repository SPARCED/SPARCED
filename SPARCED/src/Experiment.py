#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import constants as const

from utils.files_handling import *


# EXPERIMENT

class Experiment:
    def __init__(self,
                 name: str,
                 experiments_directory: str | os.PathLike,
                 simulation_files: dict[str, str],
                 config_name: str
                 ):
        # General settings
        self.name = name
        self.path = append_subfolder(experiments_directory, self.name)
        if not config_name:
            config_name = self.name + const.EXPERIMENT_CONFIG_EXTENSION
        self.configuration = self.load_configuration(self.path, config_name)
        # TODO: add stamp to results folder
        self.output_directory = append_subfolder(self.configuration[const.OUTPUT_DIRECTORY, self.name)
        self.nb_replicates = self.configuration[const.NB_REPLICATES]
        self.exchange = self.configuration[const.EXCHANGE]
        self.verbose = self.configuration[const.VERBOSE]
        self.simulation_files = simulation_files
        # In the YAML config file too: model_name, amici_path, sbml_file
