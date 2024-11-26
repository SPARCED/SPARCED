#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import antimony

from utils.arguments import parse_args
from compilation.antimony_scripts.antimony_write_IC import *


import numpy as np

import constants as const
import SparcedModel

from compilation.antimony_script.antimony_write import *
from utils.data_handling import load_input_data_file
from utils.files_handling import append_subfolder


def antimony_create_file(model: SparcedModel.Model, is_SPARCED: bool,
                         verbose: bool): # TODO specify type returned
    """Generate an Antimony file corresponding to a SparcedModel.Model
    object

    Arguments:
        model: A SparcedModel.model object.
        is_SPARCED: Use SPARCED hard-coded values/behaviors.
        verbose: Verbose.

    Returns:
        Antimony_file_path & species.
    """

    antimony_file_name = const.ANTIMONY_FILE_PREFIX + model.name \
                         + const.ANTIMONY_FILE_SUFFIX
    antimony_file_path = append_subfolder(model.path, antimony_file_name)
    species = antimony_write_file(model, antimony_file_path, is_SPARCED)
    return(antimony_file_path, species)

def antimony_write_file(model: SparcedModel.Model,
                        antimony_file_path: str | os.PathLike,
                        is_SPARCED: bool) -> tuple[np.ndarray, np.ndarray]:
    with antimony_file_path.open(mode="w") as file:
        # Header
        file.write(f"# {const.ANTIMONY_HEADER}\n")
        file.write(f"model {model.name} ()\n")
        # Compartments
        antimony_write_compartments_names(file, model.compartments)
        # Species TODO: handle several species files
        species = load_input_data_file(model.compilation_files["species"])
        antimony_write_species_names(f, species)
        # Reactions
        param_names, param_values = antimony_write_reactions(file, model)

         # Reactions
        param_names, param_vals = antimony_write_reactions(f, str(input_files["ratelaws"]),
                                  str(input_files["stoicmat"]), f_output_parameters)



def antimony_write_model(model_name: str, f_antimony: str | os.PathLike,
                         input_files: dict[str, str | os.PathLike],
                         f_output_parameters: str | os.PathLike,
                         is_SPARCED: bool) -> tuple[np.ndarray, np.ndarray]:
    """Generate an Antimony file

    Provided an empty Antimony file and paths to the SPARCED formatted input
    data files, generate the content of the Antimony file.

    Note:
        This process also creates a parameters file as an output.

    Arguments:
        f_antimony: The path of the empty Antimony file to write in.
        input_files: The dictionnary containing the input data files paths.
        f_output_parameters: The name of the output parameters file.
        is_SPARCED: A flag to raise SPARCED specific behavior or not.

    Returns:
        The contents of the compartments and species files.
    """

    with f_antimony.open(mode='w') as f:
        # Compartments
        compartments = load_input_data_file(str(input_files["compartments"]))
        antimony_write_compartments_names(f, compartments)
        # Species
        species = load_input_data_file(str(input_files["species"]))
        antimony_write_species_names(f, species)
        # Reactions
        param_names, param_vals = antimony_write_reactions(f, str(input_files["ratelaws"]),
                                  str(input_files["stoicmat"]), f_output_parameters)
        # Initial conditions
        antimony_write_compartments_IC(f, compartments)
        antimony_write_species_IC(f, species)
        antimony_write_reactions_IC(f, param_names, param_vals)
        # Declare compartments as constant variables
        if (is_SPARCED):
            antimony_write_constant_variables(f, compartments[:,0][1:])
        # Unit definitions
        antimony_write_unit_definitions(f)
        f.write("\nend") 
    return(compartments, species)

