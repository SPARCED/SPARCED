#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import constants as const
from utils.files_handling import append_subfolder


def amici_create_folder(
    model_name: str, model_path: str | os.PathLike
) -> str | os.PathLike:
    """Generate the AMICI folder path corresponding to a
    SparcedModel.Model object

    Arguments:
        model_name: The name of the model.
        model_path: The path towards the model's folder.

    Returns:
        The AMICI folder path.
    """

    amici_folder_name = const.AMICI_FOLDER_PREFIX + model_name
    amici_folder_path = append_subfolder(model_path, amici_folder_name)
    return amici_folder_path
