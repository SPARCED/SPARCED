#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import antimony


from compilation.sbml_scripts.creation import build_sbml_model_path


def convert_antimony_to_sbml(antimony_file_path: str | os.PathLike,
                             model_name: str,
                             model_path: str | os.PathLike,
                             verbose: bool) -> str | os.PathLike:
    """Convert an Antimony file into an SBML file

    Note:
        The generated SBML file is saved into the model's directory.

    Arguments:
        antimony_file_path: The path towards the Antimony file.
        model_name: The name of the model.
        model_path: The path towards the model's directory.
        verbose: Verbose.

    Returns:
        The path towards the generated SBML model file.
    """

    # Create the SBML file path
    sbml_file_path = build_sbml_model_path(model_name, model_path)
    # Load the Antimony file
    if antimony.loadFile(str(antimony_file_path)) == -1:
        if verbose:
            print(antimony.getLastError())
        raise RuntimeError("Failed to load Antimony file of model " +
                           f"{model_name}.\n")
    elif verbose:
            print("SPARCED VERBOSE: Successfully loaded Antimony file of " +
                  f"model {model_name}.\n")
    # Convert the Antimony file into an SBML model
    if antimony.writeSBMLFile(str(sbml_file_path), model_name) == 0:
        if verbose:
            print(antimony.getLastError())
        raise RuntimeError("Failed to convert Antimony file of model " +
                           f"{model_name} to SBML format.\n")
    elif verbose:
        print("SPARCED VERBOSE: Successfully converted Antimony file of " +
              f"model {model_name} to SBML format.\n")
    return(sbml_file_path)

