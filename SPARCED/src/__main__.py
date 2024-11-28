#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This script is an example of how to build and run the SPARCED model.
# Feel free to copy it to modify the behavior and run your own
# experiments.

from compilation.compilation import create_and_compile_model
# from simulation.launchers import launch_experiment_simulation

# 1. Compile the model 
# You may also want to comment this section out and run a model that was
# previously built instead.
# Note that compiling the model may take several minutes.
create_and_compile_model()

# Finally you can run an experiment, i.e. one or several cell simulations
# within the given initial conditions.
# launch_experiment_simulation() # Process parsed arguments and launch experiment
