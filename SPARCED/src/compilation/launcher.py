#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import sparced_model

from utils.arguments import parse_args



def launch_model_creation(model_name="SPARCED_standard", models_directory="./../models/", config_name="config.yaml") -> None:
    """Launch model creation function

    Small routine to process the parsed arguments and call create_model()

    Arguments:
        None.
    
    Returns:
        Nothing.
    """

    args = parse_args()
    
    # Command line arguments override coded arguments
    if args.name:
        model_name = args.name
    if args.model:
        model_path = args.model
    if args.yaml:
        config_name = args.yaml
    # Create model
    model = sparced_model.SparcedModel(model_name, model_path, config_name)
    # Runtime booleans
    is_SPARCED = not args.wild # if it's not wild then it's SPARCED //  TODO: read YAML file?
    verbose = args.verbose

    return(model, is_SPARCED, verbose)

if __name__ == '__main__':
    launch_model_creation()

