#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse


def parse_args():
    """Retrieve and parse arguments necessary for model creation

    Arguments:
        None

    Returns:
        A namespace populated with all the attributes.
    """
    
    parser = argparse.ArgumentParser()
    
    # Compilation
    parser.add_argument('-o', '--output_parameters',
                        help="desired name for the output parameters file")
    
    # Compilation & simulation
    parser.add_argument('-i', '--input_data',
                        help="name of the model subfolder containing the \
                              SPARCED formated input files")
    parser.add_argument('-m', '--model',
                        help="relative path to the directory containing the \
                              models folders")
    parser.add_argument('-n', '--name',
                        help="name of the model\nCompilation: desired name for \
                              the generated model (should be identical to \
                              model's folder name).\nSimulation: name of the \
                              input model.")
    parser.add_argument('-v', '--verbose',
                        help="don't display additional details during execution")
    parser.add_argument('-w', '--wild',
                        help="UNDER CONSTRUCTION\nrunning wild (without SPARCED \
                              hard-coded values/behaviors")
    parser.add_argument('-y', '--yaml',
                        help="name of the YAML file with all the input file names")

    # Simulation
    # -- Uppercase
    parser.add_argument('-D', '--deterministic',
                        help="don't run simulation in deterministic mode")
    parser.add_argument('-P', '--perturbations',
                        help="name of the perturbations file to use (will \
                              override default)")
    # -- Lowercase
    parser.add_argument('-p', '--population_size',
                        help="desired cell population size for the simulation")
    parser.add_argument('-r', '--results',
                        help="relative  path to the directory where simulation \
                              results will be saved")
    parser.add_argument('-s', '--simulation',
                        help="desired name for the simulation output files")
    parser.add_argument('-t', '--time',
                        help="desired virtual duration of the simulation (h)")
    parser.add_argument('-x', '--exchange',
                         help="timeframe between modules information exchange \
                               during the simulation")

    return(parser.parse_args())

