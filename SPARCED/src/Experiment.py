#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import constants as const

from utils.data_handling import load_configuration_file
from utils.files_handling import *


# EXPERIMENT

class Experiment:
    def __init__(self,
                 name: str,
                 experiements_directory: str | os.PathLike,
                 model_name: str,
                 amici_path: str | os.PathLike,
                 sbml_path: str | os.PathLike,
                 simulation_files: dict[str, str]):
    # General settings
    self.name = name
    self.path = append_subfolder(experiments_directory, self.name)
    self.configuration = self.load_configuration_file(self.path,
                            self.name + const.DEFAULT_CONFIG_FILES_EXTENSION)
    # External data
    self.model_name = model_name
    self.amici_path = amici_path
    self.sbml_path = sbml_path
    self.simulation_files = simulation_files
    # Configuration unpacking
    self.exchange
    self.nb_replica = int(
                      self.configuration[const.YAML_EXPERIMENT_NB_REPLICATES])
    # TODO: Add stamp to output_directory name if necessary
    self.output_directory = append_subfolder(self.configuration[
                                    const.YAML_EXPERIMENT_OUTPUT_DIRECTORY,
                                    self.name])
    self.verbose = self.configuration[const.YAML_EXPERIMENT_VERBOSE]

