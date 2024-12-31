#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import IO

import numpy as np


def set_compartments_ic(file: IO[str], compartments: dict[str, str]) -> None:
    """Write compartments initial conditions in the given Antimony file

    Note:
        First row is considered as a header, and hence it is skipped.
        First column of the array should contain compartments name.
        Second column of the array should contain compartments concentrations.

    Arguments:
        file: The open Antimony file.
        compartments: Content of the input compartments file structured
                      as specified in the __Note__ section.

    Returns:
        Nothing.
    """

    file.write("# Compartments initialization:\n")
    for i, value in enumerate(compartments[1:]):
        file.write(f"{value[0]} = {np.double(value[1]):.6e};\n")
        file.write(f"{value[0]} has volume;\n")

    file.write("\n")


def set_reactions_ic(
    file: IO[str], p_names: np.ndarray, p_values: np.ndarray
) -> None:
    """Write reactions parameters initial conditions in the given
       Antimony file

    Warning:
        TODO use only one array for the parameters instead of taking
        the risk to separate names from values.

    Arguments:
        file: The open Antimony file.
        p_names: The parameters names.
        p_values: The parameters values.

    Returns:
        Nothing.
    """

    file.write("# Parameters initialization:\n ")
    for count, name in enumerate(p_names):
        file.write(f"{name} = {np.double(p_values[count]):.6e};\n")
    file.write("\n")


def set_species_ic(file: IO[str], species: np.ndarray) -> None:
    """Write species initial concentrations in the given Antimony file

    Note:
        First row is considered as a header, and hence it is skipped.
        First column of the array should contain species names.
        Third column of the array should contain species concentrations.

    Arguments:
        file: The open Antimony file.
        species: Content of the input species file.

    Returns:
        Nothing.
    """

    file.write("# Species initialization:\n")
    for i, value in enumerate(species[1:]):
        file.write(f"{value[0]} = {np.double(value[2]):.6e};\n")
    file.write("\n")
