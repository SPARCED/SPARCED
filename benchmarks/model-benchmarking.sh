#!/bin/bash
###############################################################################
# Script Name:  model-benchmarking.sh
# Description:  Iterate over every prepared benchmark sequentially within the 
#		within the benchmarks directory
# Author:       Jonah R. Huggins
# Created:      2024-08-29
# Version:      1.0
#
# Usage:        ./model-benchmarking.sh [options] [arguments]
#
# Options:      
#
# Arguments:    -m | Model in question to be validated via the benchmarking 
# 		     pipeline. Provide full path from current directory 
#                    (Example: -m ../SPARCED/models/SPARCED_standard)
#
# Requirements: anaconda3
#               openmpi
#
# Notes:        Additional notes or references
###############################################################################
#SBATCH --job-name model_validation
#SBATCH --output=mpi_job_output.txt  # Output file
#SBATCH --error=mpi_job_error.txt    # Error file
#SBATCH --nodes=6                    # Number of nodes
#SBATCH --ntasks=60                  # Total number of MPI tasks (cores)
#SBATCH --ntasks-per-node=10         # Number of MPI tasks per node, balancing load across nodes
#SBATCH --cpus-per-task=1            # Number of CPUs per task (usually 1 for MPI)
#SBATCH --mem-per-cpu=20gb           # Memory alloted to each node
#SBATCH --time 47:59:00              # Time

# Initialize variables
model=""

# Parse options
while getopts "m:" opt; do
  case $opt in
    m)
      model="$OPTARG"
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done

# Shift off the options and optional --
shift $((OPTIND-1))

# List of directories to skip
skip_dirs=("benchmark_utils" "LINCS-RPPA" "LINCS-RNAseq")

# Function to check if a directory is in the skip list
should_skip() {
    local dir="$1"
    for skip in "${skip_dirs[@]}"; do
        if [ "$dir" == "$skip" ]; then
            return 0 # Return 0 (true) if the directory should be skipped
        fi
    done
    return 1 # Return 1 (false) if the directory should not be skipped
}

# Loop over all directories in the current directory
for dir in */; do
    # Remove the trailing slash from the directory name
    dir="${dir%/}"

    # Check if the directory should be skipped
    if should_skip "$dir"; then
        continue
    fi

    # Check if it is a directory
    if [ -d "$dir" ]; then
        echo "Running Benchmark: $dir"
        
        mpiexec -n 60 python __main__.py -m ${model} -b ${dir}
    fi
done
