#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thurs. 07/18/2024 2:00pm - JRH

Creates a new benchmark given a name 

- potential to add more features in the future

"""

#-----------------------Package Import & Defined Arguements-------------------#
import os
import shutil
import datetime
from typing import Dict, List
from pathlib import Path
from arguements import parse_args
args = parse_args()

#-----------------------Function Definition-----------------------------------#
class BenchmarkCreator:
    """
    Class containing functions to create a new benchmark
    """
    def create_new_benchmark() -> dict[str, list[str]]:
        """
        Creates a new benchmark given a name
        """

        assert os.path.basename(os.getcwd()) == 'benchmark_utils', \
              "Please run this script from the benchmark_utils directory"

        # Get the name of the benchmark
        assert args.name is not None, "Please provide a name for the benchmark \
using the --name or -n argument"
        
        name = args.name

        project_dir = Path(f"../{name}")
        project_dir.mkdir(parents=True, exist_ok=True)

        # List of files to create
        files_to_create = [
            "README.md",
            "conditions.tsv",
            "measurements.tsv",
            "observables.tsv",
            "parameters.tsv",
            "model_specification.tsv",
            f"{name}.yml"
        ]

        # Create each file in the project directory
        for file_name in files_to_create:
            file_path = project_dir / file_name
            file_path.touch()

        curated_decision = input("Would you like to create a curated benchmark? (y/n): ")
        if curated_decision == "y":
            BenchmarkCreator.curated_benchmark_creator()

        else:

            if args.benchmark_description and os.path.isfile(args.benchmark_description):
                with open(f"../{name}/README.md", "w") as f:
                    f.write(args.benchmark_description)
            else:
                with open(f"../{name}/README.md", "w") as f:
                    f.write(f"# {name}\n\nThis is a new benchmark created by the benchmark_utils package")

            BenchmarkCreator.populate_yml_file(f"../{name}/{name}.yml")

        print(f"Created new benchmark: {name}")
        return {"name": [name]}


    def curated_benchmark_creator() -> dict[str, list[str]]:
        """
        if prompted by the user; walks through a series of prompts to create a
        curated benchmark based on the user's input.

        Returns:
            dict[str, list[str]]: A dictionary containing the name of the benchmark
            and the list of files created 
        """
        
        # Get the name of the benchmark
        name = args.name

        # Create the benchmark
        project_dir = Path(f"../{name}")
        project_dir.mkdir(parents=True, exist_ok=True)

        # List of files to create
        files_to_create = [
            "README.md",
            "conditions.tsv",
            "measurements.tsv",
            "observables.tsv",
            "parameters.tsv",
            "model_specification.tsv",
            f"{name}.yml"
        ]

        # Create each file in the project directory
        for file_name in files_to_create:
            file_path = project_dir / file_name
            file_path.touch()

        ReadMe_decision = input("Would you like to add a README file to the benchmark? (y/n): ")
        if ReadMe_decision == "y":
            BenchmarkCreator.readme_generator()
        else:
            pass

        Measurements_decision = input("Would you like to add a measurements file to the benchmark? (y/n): ")
        if Measurements_decision == "y":
            BenchmarkCreator.measurements_uploader()
        else:
            pass

        yaml_decision = input("Would you like to add a YAML file to the benchmark? (y/n): ")
        if yaml_decision == "y":
            BenchmarkCreator.populate_yml_file(f"../{name}/{name}.yml")
        else:
            pass

        condition_decision = input("Lets create some conditions, do you have a defined conditions file? (y/n): ")
        if condition_decision == "y":
            conditions = input("Enter the path to the conditions file: ")
            shutil.copy(conditions, f"../{name}/conditions.tsv")
        else:
            manual_conditions = input("Would you like to manually create a conditions file? (y/n): ")
            if manual_conditions == "y":
                BenchmarkCreator.user_prompted_conditions_file()
            else:
                pass

        model_specs_decision = input("Would you like to add a model specification file to the benchmark? (y/n): ")
        if model_specs_decision == "y":
            BenchmarkCreator.user_prompted_model_specs_file()
        else:
            pass

        print(f"Created new benchmark: {name}")


    def readme_generator() -> Dict[str, List[str]]:
        """
        Generates a README file for the benchmark with metadata including
        date created and author.
        """
        # Get the author information
        author = input("Enter the author of the benchmark: ")

        # Get the description of the benchmark
        benchmark_description = input("Enter the description of the benchmark: ")

        # Get the current UTC date and time
        date_created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")

        # Define the content for the README file
        readme_content = f"""# Benchmark README

    **Date Created:** {date_created}

    **Author:** {author}

    ## Benchmark Description

    {benchmark_description}
    """

        # Write the content to the README file
        with open(f"../{args.name}/README.md", "w") as f:
            f.write(readme_content)


    def measurements_uploader() -> dict[str, list[str]]:
        """
        Generates a measurements file for the benchmark
        """
        # Get the path to the measurements file
        measurements = input("Enter the path to the measurements file: ")
        
        # verify that the measurements file is a list of measurements
        with open(measurements, "r") as f:
            measurement_data = f.readlines()
        
            # Write the measurements to the measurements file under the
            # measurements column of the tsv file
            with open(f"../{args.name}/measurements.tsv", "w") as f:
                f.write("measurements\n")
                for line in measurement_data:
                    f.write(line)


    def populate_yml_file(file_path) -> None:
        """
        Opens an existing YAML file and populates it with specified information.

        :param file_path: Path to the existing YAML file
        :param sbml_file_path: Path to the SBML file to be included
        """
        
        import yaml

        # Define the data to be added
        data = {
            'format_version': 1,
            'parameter_file': 'parameters.tsv',
            'problems': [
                {
                    'condition_files': ['conditions.tsv'],
                    'model_specification_files': ['model_specification.tsv'],
                    'measurement_files': ['measurements.tsv'],
                    'observable_files': ['observables.tsv'],
                    'sbml_files': ['{path}']
                }
            ]
        }

        # Read the existing content of the YAML file if it exists
        file = Path(file_path)
        if file.is_file():
            with open(file_path, 'r') as f:
                existing_data = yaml.safe_load(f) or {}
        else:
            existing_data = {}

        # Update the existing content with new data
        existing_data.update(data)

        # Write the updated content back to the YAML file
        with open(file_path, 'w') as f:
            yaml.safe_dump(existing_data, f, default_flow_style=False)


    def user_prompted_conditions_file() -> None:
        """
        Prompts the user to input a series of conditions and writes them to a
        conditions file.

        """

        # Populate the first two column headers: conditionId and conditionName
        conditions = "conditionId\tconditionName\t"

        # Prompt for what species/parameter/gene (s) are being modified
        perturbants = input("Enter the species/parameter(s)/gene(s) being modified: \
(separate by commas) ")

        # check how many perturbants are being modified
        perturbants_list = perturbants.split(",")
        perturbants_len = len(perturbants_list)

        # Add the perturbant names to the conditions string 
        for perturbant in perturbants_list:
            perturbant = perturbant.strip()
            conditions += f"{perturbant}"
            # I need to set the last perturbation to \n for a newline. 
            if perturbant == perturbants_list[-1]:
                conditions += "\n"
            else:   
                conditions += "\t"

        # Prompt the user to input the condition and description 
        def condition_input(conditions: str) -> None:    
            condition_id = input("Enter the condition ID: ")
            condition_name = input("Enter the condition's description: ")

            # Add the first condition to the conditions string
            conditions += f"{condition_id}\t{condition_name}\t"

            for perturbant in perturbants_list:
                perturbant_value = input(f"Enter the value of {perturbant} \
                                        for {condition_id}: ")
                conditions += f"{perturbant_value}"

                if perturbant == perturbants_list[-1]:
                    conditions += "\n"
                else:
                    conditions += "\t"

            return conditions
        # Prompt the user to input the conditions
        conditions = condition_input(conditions=conditions)

        # Prompt the user to input more conditions
        more_conditions = input("Would you like to add more conditions? (y/n): ")
        if more_conditions == "y":
            while more_conditions == "y":
                conditions = condition_input(conditions=conditions)
                more_conditions = input("Would you like to add more conditions? (y/n): ")

        # Write the conditions to the conditions file
        with open(f"../{args.name}/conditions.tsv", "w") as f:
            f.write(conditions)

        print("Conditions file created")


    def user_prompted_model_specs_file() -> None:
        """ Creates a model specification file based on user input. Model specifications
        Not listed in PEtab only pertain to SPARCED. Specific functionalities include
        defining whether the simulation will be determinisitic (default, 1) or stochastic (0), 
        as well as if a heterogeneous pre-existing population is to be used (default, none), and
        the number of cells to be generated if the stochastic option is chosen. 
        Input for heterogeneous populations should be an integer value in seconds for the duration
        of the heterogenization simulation. 

        """

        # Obtain the conditionId's from the conditions.tsv file
        with open(f"../{args.name}/conditions.tsv", "r") as f:
            conditions = f.readlines()
            condition_ids = [line.split("\t")[0] for line in conditions[1:]]

        # Create the column headers for the model specification file
        model_specs = "conditionId\tflagD\tnum_cells"

        # Request if the user would like to add a heterogeneous population
        heterogeneous = input("Would you like to add a heterogeneous population? (y/n): ")
        if heterogeneous == "y":
            model_specs += "\theterogenize\n"
        else:
            model_specs += "\n"

        for condition in condition_ids:
            
            model_specs += f"{condition}\t"

            print(f"Model specification for condition: {condition}")
            # Request if the simulation will be deterministic or stochastic
            flagD = input(f"Enter 1 for deterministic simulation or 0 for stochastic simulation: ")

            model_specs += f"{flagD}\t"

            # Request the number of cells to be generated
            cell_num = input("Enter the number of cells to be generated: ")
            model_specs += f"{cell_num}\t"

            # Request the duration of the heterogeneous simulation
            if heterogeneous == "y":
                heterogenize = input("Enter the duration of the heterogeneous simulation in seconds: ")
                model_specs += f"{heterogenize}\n"
            else:
                model_specs += "\n"
            
        # Write the model specifications to the model specification file
        with open(f"../{args.name}/model_specification.tsv", "w") as f:
            f.write(model_specs)

        print("Model specification file created")

    def user_prompted_observables_file() -> None:
        pass

    def user_prompted_measurement_file() -> None:
        """
        Prompts the user to input a series of materials and writes them to a
        measurements file.
        """
        pass



#-----------------------Main Function-----------------------------------------#
# Create the new benchmark, comment out if you want to run the unit test
if __name__ == "__main__":
    BenchmarkCreator.create_new_benchmark()




#-----------------------Unit Test Function-----------------------------------#
def remove_directory(name):
    project_dir = Path(f"../{name}")
    if project_dir.exists() and project_dir.is_dir():
        shutil.rmtree(project_dir)

def test_create_new_benchmark():
    """
    Tests the create_new_benchmark function
    """
    name = args.name

    # Remove the directory if it exists
    remove_directory(name)

    # Ensure the directory has been removed
    assert not os.path.isdir(f"../{name}"), f"{name} directory should not exist before test"

    # Create the new benchmark
    BenchmarkCreator.create_new_benchmark()

    # Ensure the directory has been created
    assert os.path.isdir(f"../{name}"), f"{name} directory should exist after creation"

    # Remove the directory again
    remove_directory(name)

    # Ensure the directory has been removed
    assert not os.path.isdir(f"../{name}"), f"{name} directory should not exist after cleanup"

    print("create_new_benchmark function passed")


# -----------------------Unit Test Function-----------------------------------#
# Uncomment this function to run the unit test
# if __name__ == "__main__":
#     test_create_new_benchmark()