#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This script is an example of how to build and run the SPARCED model.
# Feel free to copy it to modify the behavior and run your own
# experiments.

from compilation.compilation import create_and_compile_model
from simulation.experiment import run_experiment

# 1. Compile the model
# You may also want to comment this section out and run a model that was
# previously built instead.
# Note that compiling the model may take several minutes.
model = create_and_compile_model()

# 2. Run an experiment
# An experiment consists into one or several simulations involving one
# or several cells.
run_experiment()
