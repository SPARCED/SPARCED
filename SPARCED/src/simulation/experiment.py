#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import importlib
import numpy as np

from Experiment import Experiment as SparcedExperiment
from Model import Model as SparcedModel

from utils.arguments import parse_args


def create_experiment(model: SparcedModel=None) -> SparcedExperiment:
    if model:
        experiment = create_experiment_from_model(model)
    else:
        experiment = create_experiment_from_command_line()
    return(experiment)

def create_experiment_from_command_line() -> SparcedExperiment:
    """Create an Experiment object from a Model instance"""
    
    args = parse_args()
    experiment = SparcedExperiment(args.simulation,
                                   args.input_data,
                                   args.name,
                                   args.model,
                                   [])
    return(experiment)

def create_experiment_from_model(model: SparcedModel=None) -> SparcedExperiment:
    """Create an Experiment object from a Model instance"""

    experiment = SparcedExperiment(model.experiment_name,
                                   model.experiments_data_path,
                                   model.name,
                                   model.path,
                                   model.simulation_files)
    return(experiment)

def run_experiment(model: SparcedModel=None) -> None:
    experiment = create_experiment(model)
    experiment.run()
