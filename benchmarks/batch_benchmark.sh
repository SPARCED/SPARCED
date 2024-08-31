#!/bin/bash

#SBATCH --job-name standard_validation
#SBATCH --output=mpi_job_output.txt  # Output file
#SBATCH --error=mpi_job_error.txt    # Error file
#SBATCH --nodes=8                    # Number of nodes
#SBATCH --ntasks=160                 # Total number of MPI tasks (cores)
#SBATCH --ntasks-per-node=20	     # Number of MPI tasks per node, balancing load across nodes
#SBATCH --cpus-per-task=1            # Number of CPUs per task (usually 1 for MPI)
#SBATCH --mem-per-cpu=20gb 	     # Memory alloted to each node
#SBATCH --time 47:59:00 	     # Time
module load anaconda3
module load openmpi

source activate sparced
cd /home/jrhuggi/projects/SPARCED/benchmarks/

mpiexec -n 100 python __main__.py -b stochastic-expression
