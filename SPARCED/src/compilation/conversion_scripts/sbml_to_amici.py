#!/usr/bin/env python
# -*- coding: utf-8 -*-

import amici
import libsbml
import numpy as np

import SparcedModel

from compilation.amici_scripts.creation import amici_create_folder


def convert_sbml_to_amici(sbml_file_path: str, model_name: str, model_path: str | os.PathLike,
                          verbose: bool) -> str | os.PathLike:
    """Convert an SBML file into an AMICI model

    Note:
        The generated AMICI folder is saved into the model's directory.

    Warning:
        To speed up compilation duration, all the rate parameters are
        set as constants.

    Arguments:
        sbml_file_path: The path towards the SBML file.
        model_name: The name of the model.
        model_path: THe path towards the model's directory.
        verbose: Verbose.

    Returns:
        The path towards the generated AMICI model folder.
    """

    amici_folder_path = amici_create_folder(model_name, model_path)
    importer = amici.SbmlImporter(sbml_file_path)
    # Speed up compilation by setting all the rate parameters
    # as constants
    reader = libsbml.SBMLReader()
    document = reader.readSBML(sbml_file_path)
    sbml_model = document.getModel()
    constant_parameters = [parameters.getId() \
                           for parameters in sbml_model.getListOfParameters()]
    # Compilation
    sbml_importer.sbml2amici(model_name, amici_folder_path, verbose=verbose)
    if verbose:
        print(f"SPARCED VERBOSE: Finished to convert SBML file of model " +
              f"{model_name} to AMICI folder.\n")

    return(amici_folder_path)

