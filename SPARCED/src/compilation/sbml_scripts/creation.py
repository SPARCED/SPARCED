#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import constants as const
import SparcedModel

from utils.files_handling import append_subfolder

# EXPLANATIONS --------------------------------------------------------
# The existence of two functions is on purpose and intends to cover
# several usecases:
#   1. Build the path towards an SBML file independently from a model,
#      for example if you want to convert an Antimony file into the
#      SBML format regardless of the SPARCED pipeline.
#   2. Build the path towards an SBML file that corresponds to a model,
#      for example if you want to find where a model's SBML file should
#      be located based on the informations passed into this model.
# Hence, despite the apparent redundancy of those two functions, please
# do not remove them as they are complementary.
# ---------------------------------------------------------------------


def build_sbml_model_path(model_name: str, model_path: str | os.PathLike
                         ) -> str | os.PathLike:
    """Reconstruct the path towards an SBML file

    Arguments:
        model_name: The name of the SBML model.
        model-path: The path towards the SBML model's directory.

    Returns:
        The path of the corresponding SBML file.
    """

    sbml_file_name = const.SBML_FILE_PREFIX + model_name \
                   + const.SBML_FILE_SUFFIX
    sbml_file_path = append_subfolder(model_path, sbml_file_name)
    return(sbml_file_path)

def get_sbml_model_path(model: SparcedModel.Model) -> str|os.PathLike:
    """Generate the path for an SBML file corresponding to a
    SparcedModel.Model object

    Arguments:
        model: A SparcedModel.Model object.

    Returns:
        The path of the corresponding SBML file.
    """

    return(build_sbml_model_path(model.name, model.path))

