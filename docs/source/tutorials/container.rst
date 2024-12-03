===============================================================================
Building and Running the SPARCED Singularity Container
===============================================================================

This section explains how to build and interact with the SPARCED Singularity 
container for deploying and running the SPARCED pipeline.

===============================================================================

**Building the Container**
===============================================================================
To build the SPARCED Singularity container, follow these steps:

1. **Prerequisites**  
---------------------------------------------------------------------------
   Ensure you have Singularity installed on your system. You can check by running:  
   ```bash
   singularity --version
   ```  
   If not installed, refer to the [Singularity Installation Guide](https://sylabs.io/guides/) for detailed instructions.

2. **Clone the SPARCED Repository**  
---------------------------------------------------------------------------
   Clone the repository to your local machine:  
   ```bash
   git clone https://github.com/JonahRileyHuggins/SPARCED.git
   cd SPARCED
   ```

3. **Build the Container**  
---------------------------------------------------------------------------
   Use the following command to build the container from the provided definition file:  
   ```bash
   singularity build dist/sparced.sif container/sparced.def
   ```  
   This will create the `sparced.sif` file in the `dist/` directory.

   **Note:** Ensure the `SPARCED/` directory does not include unnecessary files (e.g., `.git`) by excluding them in the definition file or using a cleanup process.

===============================================================================

** Running or Shelling into the Container**

1. **Shell into the Container**  
---------------------------------------------------------------------------
   To access an interactive shell within the container:  
   ```bash
   singularity shell dist/sparced.sif
   ```  
   This drops you into the container environment where you can navigate and run commands.

   **Example Command:**  
   ```bash
   sparced -h
   ```

2. **Run the Container Directly**  
----------------------------------------------------------------
   To execute the default command defined in the container (e.g., running `sparced`):  
   ```bash
   singularity run dist/sparced.sif
   ```  

3. **Bind Directories (Optional)**  
----------------------------------------------------------------
   To ensure the container can read/write files on your host system, use the `--bind` flag:  
   ```bash
   singularity shell --bind /path/to/SPARCED:/SPARCED dist/sparced.sif
   ```  
   This binds the `SPARCED` directory on your host to the container, allowing full access during execution.

4. **Execute Specific Commands**  
----------------------------------------------------------------
   Use the `exec` command to run specific commands in the container:  
   ```bash
   singularity exec dist/sparced.sif sparced compile -n Basic_model
   ```  

   This runs the `sparced` tool directly inside the container.

===============================================================================

**Tips**
- Use `--cleanenv` if you want to isolate the container environment from your host machine’s variables.  
- Always verify permissions for bound directories to ensure proper read/write access.  

For additional support or troubleshooting, refer to the [Singularity Documentation](https://apptainer.org/user-docs/2.5/index.html).