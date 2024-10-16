# SPARCED Benchmarking Pipeline

This tool serves as a mechanism to rapidly and systematically compare SPARCED model predictions to experimental data. The curated directories listed here encompass 13 validated benchmarks (previously called 'unit tests') that can be used to continuously inspect whether changes to the SPARCED model change previously predicted responses.

## Individual Benchmark Overview

Each benchmark contains 7 files: 6 tab-separated value (tsv) files, an SBML file, and a yaml file (.yml) that specifies the path to each file. Each of these files are formated according to PEtab standards, [of which can be located here](https://petab.readthedocs.io/en/latest/). Note, that we include an additional file, known as the 'model_specifications.tsv' and an associated entry within the yaml file, for specifying attributes of the SPARCED model that would otherwise breach PEtab formatting standards. We treat this as an addition to the PEtab-curated benchmarks.

In brief, the code framework uses the paths specified to load in the corresponding PEtab files, as well as an instance of the SPARCED model at the SBML path specified in the corresponding yaml file, to simulate each individual simulation experiment. If a user creates a new benchmark or instance of the SPARCED model, paths to the corresponding PEtab files must be included within the yaml file.

### Creating The Model Specifications File

The model_specifications.tsv file is a SPARCED-specific file needed for specifying SPARCED capabilities outside of PEtab's scope, such as the solver setting (deterministic or stochastic), multiple stochastic cells per simulation, and, starting stochastic cells with heterogeneous values from one another. A formatting guide is provided below to aid in creating new benchmarks:

| conditionID | flagD  | num_cells | heterogenize |
| ----------- | ------ | --------- | ------------ |
| STRING      | [BOOL] | [NUMERIC] | [NUMERIC]    |
| e.g.        |        |           |              |
| condition1  | 0      | 20        | 86400        |
| condition2  | 1      | 0         | 252400       |

#### Detailed field description

* `conditionId` [STRING, NOT NULL]
  Unique identifier for the simulation/experimental condition, to be referenced by the measurement table described below. Must consist only of upper and lower case letters, digits and underscores, and must not start with a digit.
* `flagD` [BOOL, OPTIONAL]
  Simulation setting for gene expression
* `num_cells` [NUMERIC, OPTIONAL]
  Number of cells to be simulated stochastically
* `heterogenize` [NUMERIC OR STRING, OPTIONAL]
  Time length for simulated cells to be ran in a serum starved state to enable diversity among initial conditions between stochastic cells. in the time unit specified in the SBML model.

## Usage

To validate a single model benchmark (i.e. 'Stochastic Expression'), users pass the coresponding yaml file path to the benchmarking operation script. For simplicity, the names of each benchmark have been also used as the names for each yaml file. To operate, simply iterate the following command (CLI) within the SPARCED/benchmarks directory:

```
mpiexec -n [CORES] python __main__.py -b [Path/To/benchmark.yaml]
```

This calls the `__main__.py` file, which interfaces with the benchmarking code located in benchmark_utils.

Users can also iterate over every benchmark to validate all model predictions. To do so, simply execute the following command in the benchmarks/benchmark_utils/simulation/ directory:

```
python model-benchmark-validation.py -c [CORES]
```

If users operate on a high-performance computer, or any system running the SLURM job scheduler, they can instead choose to use the included BASH scripts located in the SPARCED/benchmarks directory: `batch_benchmark.sh `and `model-benchmarking.sh`

To use the either script, vim or nano must be installed. To use `batch_benchmark.sh`, an individual benchmark yaml path must be specified at line 18. The `model-benchmarking.sh` script will need custom tailoring to the user's system.
