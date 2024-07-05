#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thurs. 04/23/2024 9:00:00 - JRH

Script to automate model-benchmark comparison to prior validated results of
the SPARCED model.

Provide a path to the model directory and the script will run any benchmark
listed in the arguements benchmark list, outputing visual results to a 
'results' directory within the model directory for anlysis. 

Users are anticipated to compare simulation results to prior validated results.
"""

#-----------------------Package Import & Defined Arguements-------------------#
import sys
from benchmark_utils.run_benchmark import RunBenchmark

sys.path.append('benchmark_utils')

rb = RunBenchmark()

rb.run()

rb.observable_calculation()

rb.run_visualizer()
