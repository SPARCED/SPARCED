#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from benchmark_utils.run_benchmark import RunBenchmark

sys.path.append('benchmark_utils')

rb = RunBenchmark()

rb.run()

rb.observable_calculation()

rb.run_visualizer()
