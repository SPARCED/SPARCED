===============================================================================
SPARCED Hands-On Primer Tutorial
===============================================================================

Welcome to the SPARCED Hands-On Primer Tutorial! This guide walks you through 
how to run the Python files in the SPARCED package for tasks like model compilation, 
simulations, benchmarking, and visualizations.

Prerequisites
===============================================================================

Before running the Python files, ensure you have the following installed:

1. **Python 3.10+**
2. Required dependencies from `requirements.txt`:
   Run:
   ::
        chmod +x requirements.txt
        ./requirements.txt

3. SPARCED source code properly cloned or installed.

Running Python Scripts
===============================================================================

The SPARCED package provides various utilities for simulations, benchmarks, 
and data visualization. Below are the key Python files and their purposes.

Model Compilation
-------------------------------------------------------------------------------

To compile a model using Antimony or SBML, use the following script:

.. code-block:: bash

    python src/compilation/create_model.py --input <path/to/model/file> --output <path/to/output>

Replace `<path/to/model/file>` with the location of your Antimony or SBML model and `<path/to/output>` with the desired output path.

Simulation Execution
-------------------------------------------------------------------------------

Run a simulation using pre-defined models and conditions:

.. code-block:: bash

    python src/simulation/run_model.py --model SPARCED_standard --condition <condition_file>

- `--model`: Specify the model name (e.g., `SPARCED_standard`).
- `--condition`: Path to the condition file for the simulation.

For example:

.. code-block:: bash

    python src/simulation/run_model.py --model SPARCED_standard --condition data/simulation/standard_GeneReg.txt

Benchmark Generation
-------------------------------------------------------------------------------

To generate a benchmark, use:

.. code-block:: bash

    python src/benchmarking/creation/new-benchmark-generator.py --output benchmarks/new_benchmark.yml

This will create a new benchmark YAML file in the specified location.

Benchmark Validation
-------------------------------------------------------------------------------

To validate a model against a benchmark:

.. code-block:: bash

    python src/benchmarking/simulation/model-benchmark-validation.py --benchmark benchmarks/new_benchmark.yml

Visualization
-------------------------------------------------------------------------------

Visualize simulation results using:

.. code-block:: bash

    python src/benchmarking/visualization/visualization.py --input <path/to/results> --output <path/to/visualization>

This script processes the results and generates graphical outputs.

Key Examples
===============================================================================

Here are some hands-on examples to get you started:

1. **Running a Simple Model Simulation**:
   .. code-block:: bash

       python src/simulation/run_model.py --model SPARCED_standard --condition data/simulation/standard_GeneReg.txt

2. **Validating a Model Against Benchmarks**:
   .. code-block:: bash

       python src/simulation/model-benchmark-validation.py --benchmark benchmarks/TRAIl_percent-death.yml

3. **Generating a Custom Visualization**:
   .. code-block:: bash

       python src/visualization/visualization.py --input results/New-Simulation/Control --output figures/Control_Visualization.png

Additional Resources
===============================================================================

- For more details, refer to the **SPARCED Documentation**.
- Check out the Jupyter notebooks in the `examples/notebooks` directory for interactive tutorials.

Questions or Issues?
===============================================================================

If you encounter any issues, feel free to open an issue on the GitHub repository 
or contact the SPARCED support team.
