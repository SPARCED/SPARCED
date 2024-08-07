#!/bin/bash
###############################################################################
# Script Name: setup.sh
# Author: Jonah R. Huggins
# Date:08-06-2024
# Version: 1.0
#
# Description:
# This script installs Anaconda, clones the SPARCED repository, installs
# necessary system packages, configures git, creates and activates a conda
# environment, and installs additional conda and Python packages.
#
# Usage:
# ./setup.sh
#
# This script assumes you have sudo privileges and an internet connection.
# Make sure to run this script in a directory where you have write permissions.
#
# Change Log:
# v1.0 - Initial version
#
###############################################################################


# Exit immediately if a command exits with a non-zero status.
set -e

# Defining anaconda installer function in case not present on system

install_anaconda() {

	# Download and install Anaconda
	ANACONDA_URL="https://repo.anaconda.com/archive/Anaconda3-latest-Linux-x86_64.sh"
    	echo "Downloading Anaconda..."
    	curl -O $ANACONDA_URL

    	echo "Installing Anaconda..."
    	bash Anaconda3-latest-Linux-x86_64.sh -b

	# Initialize conda
	eval "$($HOME/anaconda3/bin/conda shell.bash hook)"
	
	}

# Step 1: Check if Anaconda is installed on the current system:
if ! command -v conda &> /dev/null; then
	echo "Anaconda package manager not found, installing Anaconda"
	install_anaconda
else
	echo "Anaconda already installed"
	eval "$($(dirname $(which conda))/../bin/conda shell.bash hook)"
fi

# Step 2: Clone the SPARCED repository
# echo "Cloning SPARCED repository..."
# sudo git clone https://github.com/SPARCED/SPARCED.git
# sudo git checkout lineage-paper

# Step 3: Install necessary system packages
echo "Installing system packages..."
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install -y libgl1-mesa-glx libegl1-mesa libxrandr2 libxss1 \
			libxcursor1 libxcomposite1 libasound2 libxi6 \
			libxtst6 libatlas-base-dev libopenmpi-dev

# Step 4: Configure git directory
git config --global --add safe.directory "$(pwd)"

# Step 5: Create and activate the conda environment
echo "Creating conda environment..."
conda env create -f environment.yml

# Step 6: Append BLAS_LIBS to .bashrc
echo "Exporting BLAS_LIBS..."
echo "export BLAS_LIBS=-lopenblas" >> ~/.bashrc
source ~/.bashrc

# Step 7: Install Python packages
echo "Installing Python packages..."
# pip install swig==4.0.0
# pip install amici==0.11.12
# pip install antimony==2.12.0.2

completion=$(cat <<END
SPARCED Anaconda environment installed successfully!



To activate, call 'conda activate test' prior to running
END
)

echo "$completion"
