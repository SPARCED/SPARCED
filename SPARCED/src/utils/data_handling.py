#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import libsbml
import numpy as np
import petab
from yaml import safe_load

from utils.files_handling import *


def load_configuration_file(self, path: str | os.PathLike, config_name: str):
        """Load configuration from a YAML file

        Arguments:
            path: The path towards the folder with the configuration..
            config_name: The name of the configuration file.

        Returns:
            A dictionnary representing the content of the YAML
            configuration file.
        """

        config_path = append_subfolder(path, config_name)
        check_path_existence(config_path)
        with config_path.open() as config_file:
            configuration = safe_load(config_file)
        return(configuration)

def load_input_data_file(f_input: str | os.PathLike) -> np.ndarray:
    """Load the given input data file

    Load an input data file structured as tab separated.

    Arguments:
        f_input: The input data file.

    Returns:
        A numpy array containing the data.
    """

    data = np.array([np.array(line.strip().split("\t"))
                    for line in open(f_input)], dtype="object")
    return(data)

def load_petab_conditions_file(file: str | os.PathLike, condition_id: str) -> dict[str, str]:
    """Load a PEtab conditions file for a specific condition

    Arguments:
        file: The path to the PEtab conditions file.
        condition_id: The ConditionId of the row to load.

    Returns:
        A dictionnary structured as key: parameter / value: value.
    """

    # ConditionId is mandatory
    if not condition_id:
        raise ValueError("Missing ConditionId.")
        return(None)
    raw_data = petab.v1.get_condition_df(file)
    try:
        petab.v1.check_condition_df(raw_data)
    except AssertionError as error:
        print(error)
        return(None)
    data = {}
    for k in raw_data.keys():
        if k != "conditionName":
            data[k] = raw_data[k][condition_id]
    return(data)

def load_species_from_sbml(sbml_path: str | os.PathLike
                           ) -> dict[str, float]:
    """Load species initial concentrations from an SBML file

    Load species names and initial concentrations from the given SBML
    file.

    Arguments:
        sbml_path:  The path to the SBML model.

    Returns:
        A dictionnary structured as key: name / value: initial
        concentration.
    """

    # Load the SBML model
    reader = libsbml.SBMLReader()
    document = reader.readSBML(sbml_path)
    model = document.getModel()
    # Read species
    species = {}
    for specie_id in range(0, model.getNumSpecies()):
        specie = model.getSpecies(specie_id)
        name = specie.getId()
        initial_concentration = specie.getInitialConcentration()
        if name:
            species[name] = float(initial_concentration)
    # Any concentration bellow 1e-6 is considered as zero (0)
    # species_initial_conditions[np.argwhere(species_initial_conditions <= 1e-6)] = 0.0
    return(species)

