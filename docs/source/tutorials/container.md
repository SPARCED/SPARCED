# Container Operation

This guide explains how to build and interact with the SPARCED-tools Docker and Singularity containers.

---

## Docker

This section primarily describes logging into and out of the interactive docker container. This assumes the container is installed. If not, navigate to [the SPARCED-tools Installation Guide](../installation-guide.md).

### Logging In

```
docker run --rm -it -v <path/to/SPARCED/>:/SPARCED jonahrileyhuggins/sparced-tools:latest
```

### Exiting

```
exit
```

## Singularity

### Building the Container

#### 1. Prerequisites

Ensure you have Singularity installed on your system. You can check by running:

```bash
singularity --version
```


If not installed, refer to the [Singularity Installation Guide](https://sylabs.io/guides/) for detailed instructions.

#### 2. Clone the SPARCED Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/JonahRileyHuggins/SPARCED.git
cd SPARCED
```

#### 3. Build the Container

Use the following command to build the container from the provided definition file:

```bash
singularity build --fakeroot container/sparced.sif container/sparced.def
```

This will create the `sparced.sif` file in the `container/` directory.

> **Note:** Ensure the `SPARCED/` directory does not include unnecessary files (e.g., `.git`) by excluding them in the definition file or using a cleanup process.

---

### Running The Container

#### 1. Shell into the Container

To access an interactive shell within the container:

```bash
singularity shell container/sparced.sif
```

This drops you into the container environment where you can navigate and run commands.

**Example Command:**

```bash
sparced -h
```

#### 2. Run the Container Directly

To execute the default command defined in the container (e.g., running `sparced`):

```bash
singularity run container/sparced.sif
```

#### 3. Bind Directories (Optional)

To ensure the container can read/write files on your host system, use the `--bind` flag:

```bash
singularity shell --bind /path/to/SPARCED:/SPARCED container/sparced.sif
```

This binds the `SPARCED` directory on your host to the container, allowing full access during execution.

#### 4. Execute Specific Commands

Use the `exec` command to run specific commands in the container:

```bash
singularity exec container/sparced.sif sparced compile -n Basic_model
```

This runs the `sparced` tool directly inside the container.

---

## Tips

* Use `--cleanenv` if you want to isolate the container environment from your host machine’s variables.
* Always verify permissions for bound directories to ensure proper read/write access.

For additional support or troubleshooting, refer to the [Singularity Documentation](https://apptainer.org/user-docs/2.5/index.html).
