#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import constants as const
import SparcedModel

from compilation.antimony_scripts.creation import antimony_create_file
from compilation.conversion_scripts.antimony_to_sbml import convert_antimony_to_sbml
from compilation.sbml_scripts.annotations import sbml_annotate_model
from utils.arguments import parse_args
from utils.files_handling import append_subfolder


def create_model(model_name=const.DEFAULT_MODEL_NAME,
                 models_directory=const.DEFAULT_MODELS_DIRECTORY,
                 config_name=const.DEFAULT_CONFIG_FILE) -> SparcedModel.Model:
    """Create a SparcedModel.Model object

    Arguments:
        model_name: The name of the model.
        models_directory: The path of the directory where the model is
                          stored.
        config_name: The name of the model's configuration file.

    Returns:
        A SparcedModel.Model object.
    """

    model = SparcedModel.Model(model_name, models_directory, config_name)
    return(model)

def create_and_compile_model(model_name=const.DEFAULT_MODEL_NAME,
                             models_directory=const.DEFAULT_MODELS_DIRECTORY,
                             config_name=const.DEFAULT_CONFIG_FILE
                             ) -> SparcedModel.Model:
    """Create a SparcedModel.Model object and compile it

    Note:
        Command-line arguments override passed arguments.

    Arguments:
        model_name: The name of the model.
        models_directory: The path of the directory where the model is
                          stored.
        config_name: The name of the model's configuration file.

    Returns:
        A SparcedModel.Model object.
    """

    args = parse_args()
    # Command line arguments override coded arguments
    if args.name:
        model_name = args.name
    if args.model:
        models_directory = args.model
    if args.yaml:
        config_name = args.yaml
    model = create_model(model_name, models_directory, config_name)
    # If it is not wild then it's SPARCED
    is_SPARCED = not args.wild # TODO: read YAML file?
    verbose = args.verbose
    compile_model(model, is_SPARCED, verbose)
    return(model)

def compile_model(model: SparcedModel.Model, is_SPARCED: bool, verbose:bool
                  ) -> None: 
    """Generate Antimony, SBML and AMICI models corresponding to a
    SparcedModel.Model object

    Arguments:
        model: A SparcedModel.model object.
        is_SPARCED: Use SPARCED hard-coded values/behaviors.
        verbose: Verbose.

    Returns:
        Nothings.
    """

    if model == None:
        raise ValueError("No model provided.")
    try:
        antimony_file_path, species = antimony_create_file(model)
        sbml_file_path = convert_antimony_to_sbml(antimony_file_path,
                                                  model.name,
                                                  model.path,
                                                  verbose)
    except RuntimeError as error:
        print(f"SPARCED ERROR: {error}\n")
        sys.exit(0)
    sbml_annotate_model(str(sbml_file_path), species)


if __name__ == '__main__':
    create_and_compile_model()

