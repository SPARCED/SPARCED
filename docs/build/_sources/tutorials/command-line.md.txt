# Command Line Interface (CLI)

The SPARCED package provides a convenient CLI tool to manage common tasks like compiling models, running simulations, benchmarking, and visualizing results.

This guide explains how to use the `sparced` CLI tool to streamline your workflows.

## Getting Started

Before using the CLI, ensure the following:

### Container Operation

Before running command line prompts, ensure the container is working by inspecting that the shell prompt, displayed within the terminal window, has changed from the default to the following:

**Docker:**

```
root@1607f217fffb:/SPARCED#
```

**Singularity:**

```
[user@hostname:/SPARCED]$
```

### Verify Installation

Run the following command to verify:

```bash
sparced --help
```

If installed correctly, this will display the help menu for the CLI.


## General Usage

Use the following syntax:

Example:

```bash
sparced <command> [options]
```

---

## Available Commands and Flags

### 1. `compile` Command

Compile a model.

```bash
sparced compile [options]
```

**Available Flags:**

* `-o, --output_parameters`: Desired name for the output parameters file. (Default: `out_Parameters.txt`)
* `-n, --name`: Desired name for the generated model.

---

### 2. `simulate` Command

Run a simulation.

```bash
sparced simulate [options]
```

**Available Flags:**

* `-n, --name`: Name of the input model.
* `-p, --population_size`: Desired cell population size for the simulation. (Default: `1`)
* `-t, --time`: Desired virtual duration of the simulation in hours. (Default: `1.0`)
* `-r, --results`: Directory where simulation results will be saved. (Default: `./results/New-Simulation/`)
* `-s, --simulation`: Desired name for the simulation output files. (Default: `GrowthStim`)
* `-x, --exchange`: Timeframe between modules for information exchange during the simulation. (Default: `30`)
* `-D, --deterministic`: Run the simulation in deterministic mode (default). Use the flag to disable.
* `-P, --perturbations`: Name of the perturbations file to use. Overrides the default.

---

### 3. `validate` Command

Benchmark a model.

```bash
sparced validate [options]
```

**Available Flags:**

* `-rs, --return_sedml`: Return the SED-ML file. (Default: `False`)
* `-r, --results`: Directory where benchmark results will be saved. (Default: `./../results/New-Benchmark/`)
* `-n, --name`: Name to save the benchmark results.
* `-b, --benchmark`: Name of the benchmark to be used. (Optional)
* `-c, --cores`: Number of cores to use for a parallel process. (Default: `1`)
* `-bd, --benchmark_description`: Description of the benchmark. (Optional)
* `-a, --run_all`: Run all benchmarks in the benchmarks directory. Overrides the `-b` flag. (Optional)
* `-O, --Observable`: Whether only the observable in `observables.tsv` is calculated (`1`) or the entire simulation is saved (`0`). (Default: `1`)

---

### 4. `visualize` Command

Visualize a dataset.

```bash
sparced visualize [options]
```

**Available Flags:**

* `-o, --output`: Output path to save the visualization.
* `-n, --name`: Name of the output file.
* `-f, --from_script`: Flag to indicate that the visualization is being run from a custom script.
* `--catchall, -c`: A JSON string containing additional arguments to pass to the custom script.

---

### Shared Flags

These flags can be used with any of the commands:

* `-v, --verbose`: Enable verbose output.
* `-y, --yaml`: YAML file with input configuration. (Default: `config.yaml`)
* `-i, --input_data`: Name of the subfolder containing SPARCED-formatted input files. (Default: `data/`)
* `-m, --model`: Relative path to the directory containing the model folders. (Default: `./models/`)
* `-w, --wild`: Running wild (without SPARCED hard-coded values/behaviors). *(Under Construction)*

---

## Examples

### Compile a Model

```bash
sparced compile -n MyModel -o parameters.txt
```

### Run a Simulation

```bash
sparced simulate -n SPARCED_standard -p 500 -t 48
```

### Benchmark a Model

```bash
sparced validate -b benchmark_file.yml -c 4
```

### Visualize Data

```bash
sparced visualize -n visualization_output -o ./visualizations/
```

---

For more information on specific commands and flags, use the `--help` flag with any command:

```bash
sparced <command> --help
```
