# The SPARCED Installation Guide for Absolute Beginners

_Written by Aurore Amrit_ *and Jonah R. Huggins*

Hi! 🌄

If you are new to SPARCED and wish to get a working environment setup on Ubuntu, then you are at the right place! This document was started by Aurore while she was a summer intern at the Birtwistle lab to make the process easier for newcomers like you 🙂

## Environment

Kinetic models are often reliant on Ordinary Differential Equation solvers to perform the simulated 'heavy-lifting'. Given the Large-scale nature of the SPARCED model, we use [AMICI (v0.11.12)](https://amici.readthedocs.io/en/v0.11.12/), an ODE solver specifically made for large-scale kinetic modeling. However, AMICI's reliance on C/C++ solvers as well as BLAS, complicate straightforward installation outside of Ubuntu. Therefore, we have tried to be as accomodating as possible to the broad community in enabling cross-platform support.

SPARCED runs seamlessly on **Ubuntu 22.04 LTS** , either as a virtual machine (i.e. **VirtualBox**), a container (**Singularity** or **Dockerfile**), or on **Windows-Subsystem for Linux.** This guide should work even if you are using another hypervisor than VirtualBox or that you are running Ubuntu directly on your computer. With a few arrangements, the described steps should also work for other versions of Ubuntu or any Debian-based Linux distribution.

⚠️ Make sure you have enough disk space (30 GB is a minimum) ⚠️

## Command Line Interface Installation

The ` requirements.txt` file provided in the project root directory is an executable BASH script designed to install SPARCED dependencies in Ubuntu 22.04. For cross-platform compatibility on Linux, MacOS, Windows, and Linux-based High-Performance Computing (HPC), instructions have been provided (including Docker and Singularity).

Links to [Docker](https://docs.docker.com/get-started/get-docker/), [Singularity](https://docs.sylabs.io/guides/3.0/user-guide/installation.html), and [VirtualBox](https://www.virtualbox.org/wiki/Downloads) installations are provided below for convenience.

### Ubuntu 22.04 and Windows-Subsystem for Linux (WSL2)

Installation is seamless when using the BASH-executable `requirements.txt` file, which is reliant on a [PEP 621 - adherent](https://peps.python.org/pep-0621/) `pyproject.toml` file located adjacently in the project root directory.

To install, execute the following commands within the SPARCED root directory:

```bash
chmod +x ./requirements.txt # provides authorized installation access
./requirements.txt # Installation command
```

After installation is complete, restart your shell for the changes to take effect.

### MacOS, Windows, HPC, and Non-Root Users: Installation via Containers

#### Docker

For MacOS and Windows, we strongly recommend installing the Docker container.

```
# If you haven't done so already:
docker login 
# Pull the container:
docker pull jonahrileyhuggins/sparced-tools:latest
```

Alternatively, the Docker container can be built locally:

```
docker buildx build -t sparced-tools -f /path/to/SPARCED/container/Dockerfile .
```

Operating inside of the container enables the use of the SPARCED toolset without having to install the python dependencies.

```
docker run sparced-tools
```

Further, users are able to bind their local SPARCED directory with the container's SPARCED directory, allowing for native, local modifications on the host system:

```
docker run -it --rm -v C:\Users\<username>\path\to\SPARCED:/SPARCED sparced-tools
```

**Flags:**

**`--rm`**

* **Stands for:** *Remove*
* **Function:** Automatically removes the container when it stops
* **Why use it**
  * Prevents the accumulation of stopped containers that would otherwise take up system resources.
  * Useful for temporary containers where you don't need to persist the container itself after it has run.

**`-i`**

* **Stands for:** *Interactive*
* **Function:** Keeps the standard input (`stdin`) open, even if not attached to a terminal.
* **Why use it?**
  * Allows the container to accept input from the user during runtime.
  * Especially useful when paired with `-t` for running an interactive shell session.

**`-t`**

* **Stands for:** *TTY (teletypewriter)*
* **Function:** Allocates a pseudo-terminal for the container.
* **Why use it?**
  * Allows for better interactivity, like being able to run `bash` or `sh` inside the container and see a command prompt.
  * Often paired with `-i` for fully interactive sessions.

#### **Singularity**

Singularity is a containerization platform designed specifically for high-performance computing (HPC) and research environments. It allows users to create, distribute, and execute portable, reproducible containers across different systems. Unlike Docker, Singularity focuses on usability in environments where users don't have root access, such as shared HPC clusters.

**Key Features:**

1. **Rootless Execution:** Users don't need root privileges to run containers, enhancing security.
2. **File System Binding:** Provides seamless integration with the host system by binding directories into the container.
3. **Portability:** Containers can be moved and executed across different platforms without modification.
4. **Support for MPI:** Well-suited for parallel computing environments, allowing easy integration with MPI libraries.

---

##### **Building the Singularity Container from a Definition File**

To build a container using the `sparced.def` file, execute the following command from the project root directory:

```bash
singularity build --fakeroot container/sparced.sif container/sparced.def
```

* **`sparced.sif`:** The output file, a Singularity Image File (SIF).
* **`sparced.def`:** The definition file that specifies the container's environment and setup.
* **`--fakeroot`:** Flag for building the singularity container without root access

To verify that the container is successfully built, execute the following:

```bash
singularity inspect container/sparced.sif
```

---

##### **How to Shell into and Interact with the Singularity Container While Binding the Host SPARCED Directory**

1. **Bind the Host Directory:**
   Use the `--bind` option to link a host directory into the container.
2. **Run the Container:**
   To open a shell inside the container with the `SPARCED` directory bound:

   ```bash
   singularity shell --bind /path/to/host/SPARCED:/SPARCED container/sparced.sif
   ```

   * **`/path/to/host/SPARCED`:** Replace this with the absolute path to your host's SPARCED directory.
   * **`/SPARCED`:** This is the directory inside the container where the host directory will be accessible.
3. **Operate Within the Container:**
   Once inside the container, you’ll see a prompt. Run commands as if you’re working on a standalone system:

   ```bash
   sparced compile -n Basic_model
   ```
4. **Exit the Container:**
   Type `exit` to leave the container.

---


If successful, the below configurations are not necessary. This is a conda-free installation.

### Installation verification

After installation is complete, test the installation via:

```bash
sparced -h
```

⚠️ Note: Ubuntu users might have to restart their shell session for the changes to take effect. ⚠️

Correct installation should output the following help information:

```
usage: SPARCED [-h] {compile,simulate,validate} ...

SPARCED CLI tool.

positional arguments:
  {compile,simulate,validate}
                        Subcommands: compile, simulate, benchmark
    compile             Compile a model.
    simulate            Run a simulation.
    validate            Benchmark a model.

options:
  -h, --help            show this help message and exit
```

## OpenMPI on Windows

_If you are not going to use parallel computation on your computer,
skip this section._

If you want to run some parallel code on your computer (for example to debug on
your own machine some code intented to run parallely on Palmetto), then you
will need to install OpenMPI.

:coin: **Tip:** Starting with the OpenMPI installation will prevent you from
starting everything from scratch again in case of failure (as it happened to me).

First, download the latest stable version of OpenMPI from the
[openmpi.org](https://www.open-mpi.org//software/ompi/v4.1/) website. You want
the ``.tar.gz`` extension.
Then run the following commands in your terminal (some can take a few minutes
and be very verbose, so get a ☕):

```bash
mkdir openmpi
cd openmpi
cp ~/Downloads/openmpi-{version number}.tar.gz . # with {version number} being the version number
tar -xzvf openmpi-{version number}.tar.gz # with {version number} being the version number
cd openmpi-{version number} # with {version number} being the version number
./configure --prefix=$HOME/openmpi # do not add any flag related to C++ (cxx) as they are no longer supported
make install
export PATH=$HOME/openmpi/bin:$PATH
export LD_LIBRARY_PATH=$HOME/openmpi/lib:$LD_LIBRARY_PATH
```

You can check if the installation process worked using:

```bash
mpirun --version
```

If you get an error involving Fortran during this process and you find a way to
fix it without having to reinstall everything, please notify me! 🙏

## Git, GitHub & SSH

### Git

```bash
sudo apt install git-all
```

You can use the following commands to set your username and your user's email.

```bash
git config --global user.name {username}
git config --global user.email {email}
```

### SSH for GitHub

I assume that you already have an account on [GitHub](https://github.com/).

```bash
ssh-keygen -t ed25519 -C "{email}" # with {email} being your email for GitHub
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

:coin: **Tip:** Just press ``[enter]`` to use the default file in which to
save the key.

Print your SSH key in the terminal using:

```bash
cat ~/.ssh/id_ed25519.pub
```

Copy it. The in your GitHub settings, create a new SSH key and paste it.

Run the following command to test your SSH connexion:

```bash
ssh -T git@github.com
```

## Anaconda

Download the
[Anaconda installer for Linux](https://www.anaconda.com/products/distribution#linux),
then run the following commands in your terminal:

```bash
sudo apt-get install libgl1-mesa-glx libegl1-mesa libxrandr2 libxrandr2 libxss1 libxcursor1 libxcomposite1 libasound2 libxi6 libxtst6
bash ~/Downloads/Anaconda3-{version-number}-Linux-x86_64.sh # with {version-number} being your version number
```

Then follow the instructions of the installer. Make sure it initializes
Anaconda3 by running conda init (type "yes" when asked for).

Once the installation is over, you need to restart your terminal (close and
reopen it or type ``source ~/.bashrc``).

Conda will automatically activate your ``base`` environment when launching
the terminal. If you want to disable this behavior, enter:

```bash
conda config --set auto_activate_base False # set it according to your preferences
```

Finally, verify your installation using:

```bash
conda list
```

To make sure Anaconda is up to date, run:

```bash
conda update --all
```

### Environment

Create a new Anaconda environment using the following commands:

```bash
conda create -n sparced # Creates an environment named "sparced"
source activate sparced # Activates the "sparced" environment
```

Unless you decide to set it otherwise, you will have to manually activate the
"sparced" environment each time you reopen your terminal.

### Python Packages

```bash
conda install matplotlib pandas scipy
pip install python-libsbml==5.18.0
pip install -Iv antimony==2.12.0.1 # WARNING: antimony >= 2.13.0 doesn't work with SPARCED
```

### The Amici Package

```bash
sudo apt install libatlas-base-dev swig
pip install amici==0.11.12 # WARNING: newer versions don't work with SPARCED
```

You might get an error about the CBLAS library (this happens mostly on
Palmetto), to fix it run:

```bash
conda install -c conda-forge openblas
export BLAS_LIBS=-lopenblas
```

### The mpi4py Package

_If you are not going to use parallel computation, skip this section._

```bash
conda remove compilers # if the compilers package is missing then don't install it!
conda install -c forge mpi4py # if you encounter any dependency version failure, try downgrading to Python 3.11 by typing 'conda install python=3.11'
conda install -c conda-forge compilers
python -m pip install gmx_MMPBSA
```

## SPARCED 🎆

This is only a setup suggestion:

```bash
cd ~/Documents
mkdir birtwistle-lab ; cd birtwistle-lab
git clone --recursive ssh://git@github.com/birtwistlelab/SPARCED.git # The official SPARCED repository
cd ..
git clone --recursive ssh://git@github.com/{username}/SPARCED.git # with {username} being your username on GitHub, assuming that you already forked SPARCED
```

## Clean

Remove all unused packages that were installed by dependencies during the setup:

```bash
sudo apt-get autoremove
```

Congratulations! You now have a full setup of SPARCED! 🦠
