#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import libsbml
import numpy as np


def apply_perturbations(species_initial_conditions: np.ndarray,
                        species_names: np.ndarray,
                        perturbations: np.ndarray=None) -> np.ndarray:
    """Update species initial conditions according to a perturbation array

    Arguments:
        species_initial_conditions: The array containing the initial concentrations.
        species_names: The array containing the names of the species.
        perturbations: An array containing the perturbations to apply.

    Returns:
        The updated initial conditions array.
    """

    if perturbations is not None:
        for p in perturbations:
            species_initial_conditions[np.argwhere(species_names == p[0])] = p[1]
    return(species_initial_conditions)

