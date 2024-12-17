#!/usr/bin/env python
# -*- coding: utf-8 -*-



import constants as const
from Experiment import Experiment as SparcedExperiment
from Model import Model as SparcedModel

from utils.arguments import parse_args


def create_experiment(model_name = const.DEFAULT_MODEL_NAME,
                      models_directory = const.DEFAULT_MODELS_DIRECTORY,
                      config_name = const.DEFAULT_CONFIG_FILE,
                      model: SparcedModel=None) -> SparcedExperiment:
    # Command-line arguments override model specifications
    args = parse_args()
    if not model:
        if args.name:
            model_name = args.name
        if args.model:
            models_directory = args.model
        if args.yaml:
            config_name = args.yaml
        model = SparcedModel(model_name, models_directory, config_name)
    if args.simulation:
        model.experiment_name = args.simulation
    if args.input_data:
        model.experiment_data_path = args.input_data
    experiment = SparcedExperiment(model.experiment_name,
                                   model.experiments_data_path,
                                   model.name,
                                   model.path,
                                   model.simulation_files)
    return(experiment)

def run_experiment(model_name = const.DEFAULT_MODEL_NAME,
                   models_directory = const.DEFAULT_MODELS_DIRECTORY,
                   config_name = const.DEFAULT_CONFIG_FILE,
                   model: SparcedModel=None) -> None:
    experiment = create_experiment(model_name,
                                   models_directory,
                                   config_name,
                                   model)
    experiment.run()

