===============================================================================
Using the SPARCED Command Line Interface (CLI)
===============================================================================

The SPARCED package provides a convenient CLI tool to manage common tasks like 
compiling models, running simulations, benchmarking, and visualizing results.

This guide explains how to use the `sparced` CLI tool to streamline your workflows.

Getting Started
===============================================================================

Before using the CLI, ensure the following:

1. **SPARCED Installed as a CLI Tool**:
   The `sparced` CLI tool is installed and available in your environment. If not, 
   install it using the requirements file in the project directory:
   ::
      chmod +x requirements.txt
      ./requirements.txt

2. **Verify Installation**:
   Run the following command to verify:
   ::
      sparced --help

   If installed correctly, this will display the help menu for the CLI.

Common Commands
===============================================================================

The `sparced` CLI supports several commands for different operations:

General Usage
-------------------------------------------------------------------------------
Use the following syntax:
::
   sparced <command> [options]

Example:
::
   sparced simulate --name SPARCED_standard

Available Commands
-------------------------------------------------------------------------------

1. **Compile Models**:
   Compile an Antimony or SBML model:
   ::
      sparced compile --name <model_name> --output <output_directory>

   - `--input`: Path to the Antimony or SBML model file.
   - `--output`: Directory to save the compiled model.

   Example:
   ::
      sparced compile --name SPARCED_standard --output compiled_models/

2. **Run Simulations**:
   Execute simulations using a specified model and condition file:
   ::
      sparced simulate --name <model_name> --condition <condition_file>

   - `--model`: Name of the model (e.g., `SPARCED_standard`).
   - `--condition`: Path to the condition file.

   Example:
   ::
      sparced simulate --name SPARCED_standard --condition data/simulation/standard_GeneReg.txt

   - `--benchmark`: Name of the benchmark.
   - `--Observable`: Boolean flag for whether the validation pipeline returns all results (False) \
   or only the observable results (True).

4. **Validate Benchmarks**:
   Compare a model's output to a benchmark:
   ::
      sparced validate --benchmark <benchmark_file>

   - `--benchmark`: Path to the benchmark YAML file. 

   Example:
   ::
      sparced validate --benchmark benchmarks/TRAIL-response.yml

Advanced Options
===============================================================================

To view all options for a specific command, use the `--help` flag:
::
   sparced <command> --help

For example:
::
   sparced simulate --help

This will display detailed information about the `simulate` command and its options.

Examples
===============================================================================

Here are a few example workflows:

1. **Compile and Run a Model**:
   ::
      sparced compile --name SPARCED_standard
      sparced simulate --name SPARCED_standard 

2. **Validate a Benchmark**:
   ::
      sparced validate --benchmark benchmarks/TRAIL-response/TRAIL-response.yml

MPI Support
===============================================================================
The SPARCED CLI supports MPI for parallel processing for (only) the validate function.
 To enable MPI, call the `mpiexec` command before the `sparced` command:
   ::
      mpiexec -n <num_processes> sparced validate [options]

For example:
   ::
      mpiexec -n 4 sparced simulate --benchmark benchmarks/TRAIL-response/TRAIL-response.yml


Troubleshooting
===============================================================================

If you encounter issues while using the CLI tool, check the following:

1. **Environment**:
   Ensure the CLI tool is installed in your environment and accessible via the `sparced` command.

2. **Dependencies**:
   Verify the command line Interface was installed properly:
   ::
      pipx list
   The output should include `sparced`.

3. **Log Files**:
   Some commands may produce log files for debugging. Check the output directory for logs.

For additional help, use:
::
   sparced --help
