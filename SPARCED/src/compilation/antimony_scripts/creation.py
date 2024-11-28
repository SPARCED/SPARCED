#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import antimony
import numpy as np

import constants as const
import SparcedModel

import compilation.antimony_scripts as antimony_script
from utils.data_handling import load_input_data_file
from utils.files_handling import append_subfolder


def antimony_create_file(model: SparcedModel.Model) -> (str, np.ndarray):
    """Generate an Antimony file corresponding to a SparcedModel.Model
    object

    Arguments:
        model: A SparcedModel.Model object.

    Returns:
        Antimony_file_path & species.
    """

    antimony_file_name = const.ANTIMONY_FILE_PREFIX + model.name \
                         + const.ANTIMONY_FILE_SUFFIX
    antimony_file_path = append_subfolder(model.path, antimony_file_name)
    species = antimony_write_file(model, antimony_file_path)
    return(antimony_file_path, species)

def antimony_write_file(model: SparcedModel.Model,
                        antimony_file_path: str | os.PathLike
                        ) -> np.ndarray:
    """Generate an Antimony file

    Note:
        This process also creates a parameters file as an output.

    Arguments:
        model: A SparcedModel.Model object
        antimony_file_path: The path of the Antimony file to write in.

    Returns:
        The content of the species file.
    """

    with antimony_file_path.open(mode="w") as file:
        # Header
        file.write(f"# {const.ANTIMONY_HEADER}\n")
        file.write(f"model {model.name}()\n")
        # Compartments
        antimony_script.define_compartments(file, model.compartments)
        # Species
        species = load_input_data_file(
                model.compilation_files[const.YAML_SPECIES])
        antimony_script.define_species(file, species)
        # Reactions
        param_names, param_values = antimony_script.write_reactions(
                        file,
                        model.compilation_files[const.YAML_RATELAWS],
                        model.compilation_files[const.YAML_OUTPUT_PARAMETERS])
        # Initial conditions
        antimony_script.set_compartments_ic(file, model.compartments)
        antimony_script.set_species_ic(file, species)
        antimony_script.set_reactions_ic(file, param_names, param_values)
        # Units definition
        antimony_script.define_units(file)
        file.write("\nend") 
    return(species)


if __name__ == '__main__':
    model = SparcedModel.Model(const.DEFAULT_MODEL_NAME,
                               const.DEFAULT_MODELS_DIRECTORY,
                               const.DEFAULT_CONFIG_FILE)
    antimony_create_file(model)

