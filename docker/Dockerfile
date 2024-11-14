# Build from root directory, not docker folder

FROM ubuntu:20.04

SHELL ["/bin/bash", "-c"]

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update -qq -y && \
	apt-get upgrade -qq -y && \
	apt-get install -qq -y \
		bash curl build-essential git-all libatlas-base-dev swig \
		libgl1-mesa-glx libegl1-mesa libxrandr2 libxrandr2 libxss1 libxcursor1 libxcomposite1 libasound2 libxi6 libxtst6 && \
	apt-get autoremove && \
	apt-get clean -y

# Create a working directory called /app
WORKDIR /app
ADD . /app
VOLUME /app/logs

# Anaconda
RUN curl -O https://repo.anaconda.com/archive/Anaconda3-2024.10-1-Linux-x86_64.sh && \
	shasum -a 256 Anaconda3-2024.10-1-Linux-x86_64.sh && \
	bash ./Anaconda3-2024.10-1-Linux-x86_64.sh -b && \
	source ~/anaconda3/etc/profile.d/conda.sh

RUN conda update --all && \
	conda env create -f environment.yml && \
	conda activate sparced && \
	conda install gcc_linux-64 && \
	conda install gxx_linux-64 && \
	conda install -c conda-forge openmpi && \
	export BLAS_LIBS=-lopenblas && \
	pip install swig==4.0.0 && \
	pip install -Iv antimony==2.12.0.1 && \
	conda install -c conda-forge openmpi && \
	export BLAS_LIBS=-lopenblas && \
	pip install amici==0.11.12

CMD bash
