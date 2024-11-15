#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
script name: builders.py
Created on Mon. Oct. 28th 23:15 2024
Author: Jonah R. Huggins

Description: Series of functions for constructing elements, classes, and \
objects critical towards constructing a SED-ML file from PEtab files.

Output: a SED-ML file.

"""
# ------------------------------package import----------------------------------#
import os
import sys
import xml.etree.ElementTree as ET
import yaml
import phrasedml
import pandas as pd
from lxml import etree

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from sedml.loader import file_loader
import sedml.extractors as extractors


# ------------------------------function definitions---------------------------#
def build_simulation(conditions_df: pd.DataFrame, measurements_df: pd.DataFrame) -> str:
    """
    Builds a string for the SED-ML listOfSimulations element for all \
    simulation conditions.

    Parameters
    - conditions_df (pd.DataFrame): The conditions dataframe.
    - measurements_df (pd.DataFrame): The measurements dataframe.
    - model_id (str): The metaid of the model.

    TODO: convert method in model_specifications into KISAO-defined algorithm, 
    and add to the simulation string. Placeholder is currently KISAO:0000019.
    """
    simulation = ""
    for _, condition in conditions_df.iterrows():
        simulation_times = extractors.extract_simulation_times(
            condition_id=condition["conditionId"], measurements_df=measurements_df
        )

        simulation += f"""{condition["conditionId"]} = simulate uniform(\
{simulation_times['initialTime']}, \
{simulation_times['outputEndTime']}, {simulation_times['numberOfSteps']})\n"""

    return simulation


def build_tasks(model_id: str, conditions_df: pd.DataFrame) -> str:
    """
    Builds a string for the SED-ML AbstractTask element in PhraSED-ML by \
        creating separate models per task.
    
    Parameters
    - model_id (str): The ID of the model.
    - conditions_df (pd.DataFrame): The conditions dataframe.
    
    Returns
    - task_string (str): The string for the SED-ML AbstractTask element.
    """
    phrasedml_task_string = ""

    for i, condition in conditions_df.iterrows():
        # Create a unique model for each task with parameter perturbations
        condition_id = condition["conditionId"]
        perturbed_model_id = f"{model_id}_{condition_id}"

        # Start defining the model with specific parameter values
        model_definition = f"{perturbed_model_id} = model model1 with"

        # Add perturbations as parameter overrides in the model definition
        perturbations = condition.index[2:]
        values = condition[2:]

        for perturbation in perturbations:
            model_definition += f" {perturbation} = {values[perturbation]},"

        # Remove final comma and add line break
        model_definition = model_definition[:-1] + "\n"

        # Define the task using the newly created perturbed model
        task = f"task{i+1} = run {condition['conditionId']} on {perturbed_model_id}\n"

        # Add model definition and task to the output string
        phrasedml_task_string += model_definition + task

    return phrasedml_task_string


def build_data_generators(
    sedml_file: os.PathLike, observables_df: pd.DataFrame
) -> etree.Element:
    """
   Function to build SED-ML data generators as XML elements.

   Parameters
       - observables_df (pd.DataFrame): DataFrame containing observables and \
        their expressions.

    Returns:
    - sedml_root (etree.Element): Root element of the SED-ML structure.
    """
    # Instantiate the SED-Ml model from the prior built PhraSED-ML file
    phrased_xml = etree.parse(sedml_file)
    root = phrased_xml.getroot()

    # 1. Define Data Generators for Observables
    for _, row in observables_df.iterrows():
        obs_id = row["observableId"]
        obs_formula = row["observableFormula"]

        if "observableName" in row:
            name = row["observableName"]
        else:
            name = f"{obs_id}_gen"

        # Each observable now needs a data generator element
        data_gen = etree.SubElement(root, "DataGenerator", id=obs_id, name=name)

        var = etree.SubElement(
            data_gen,
            "variable",
            id=f"{obs_id}_var",
            taskReference="task1",
            symbol="urn:sedml:symbol:time",
        )

        # Define the math element
        math = etree.SubElement(
            data_gen, "math", xmlns="http://www.w3.org/1998/Math/MathML"
        )

        ci = etree.SubElement(math, "ci")
        ci.text = obs_formula

        root.append(data_gen)

    ET.indent(root, space="    ")

    # Write back the modified SED-ML document
    phrased_xml.write(sedml_file, xml_declaration=True, encoding="UTF-8")

    print(f"Added DataGenerator to {sedml_file}")

    return sedml_file


def build_data_descriptions(
    sedml_file: os.PathLike, measurement_df: pd.DataFrame, yaml_file: os.PathLike
) -> os.PathLike:
    """
    Use the extractors.extract_data function to build the data generator
    string for the SED-ML file.

    Parameters
    - sedml_file (os.PathLike): The path to the SED-ML file to modify.
    - measurement_df (pd.DataFrame): The measurements dataframe.
    - yaml_file (os.PathLike): Path to the YAML file with configuration info.

    Returns
    - sedml_file (os.PathLike): The path to the modified SED-ML file.
    """
    # Load the existing SED-ML XML document
    phrased_xml = ET.parse(sedml_file)
    root = phrased_xml.getroot()

    # Create a new DataDescription element
    data_description = ET.Element("dataDescription")

    with open(yaml_file, encoding="utf=8", mode="r") as file:
        yaml_data = yaml.safe_load(file)

        measurements_path = os.path.join(
            os.getcwd(), yaml_data["problems"][0]["measurement_files"][0]
        )

    # Add necessary attributes to the DataDescription
    data_description.set("id", "DataDescription1")  # Set a unique ID
    data_description.set("source", measurements_path)  # Set the source
    data_description.set("name", "Measurement Data")  # Name it as needed
    data_description.set("format", "urn:sedml:format:csv")  # Specify CSV format

    # Create unique data sources for each observable and condition pair
    unique_pairs = measurement_df[
        ["observableId", "simulationConditionId"]
    ].drop_duplicates()

    for _, row in unique_pairs.iterrows():
        observable_id = row["observableId"]
        condition_id = row["simulationConditionId"]

        # Create a DataSource for each unique condition-observable pair
        data_source = ET.SubElement(data_description, "dataSource")
        data_source.set("id", f"{observable_id}_{condition_id}")

        # Add slices for observable and condition filtering
        list_of_slices = ET.SubElement(data_source, "listOfSlices")

        # Slice by observableId
        slice_observable = ET.SubElement(list_of_slices, "slice")
        slice_observable.set("reference", "observableId")
        slice_observable.set("value", observable_id)

        # Slice by simulationConditionId
        slice_condition = ET.SubElement(list_of_slices, "slice")
        slice_condition.set("reference", "simulationConditionId")
        slice_condition.set("value", condition_id)

    # Append the DataDescription to the SED-ML root
    root.append(data_description)

    ET.indent(root, space="    ")

    # Write back the modified SED-ML document
    phrased_xml.write(sedml_file, xml_declaration=True, encoding="UTF-8")

    print(f"Added DataDescription to {sedml_file}")

    return sedml_file


def build_output(visualization_df: pd.DataFrame, sedml_file: os.PathLike) -> None:
    """
    Builds the output for the SED-ML file.

    Parameters
    - visualization_df (pd.DataFrame): The visualization dataframe.
    - sedml_file (os.PathLike): The path to the SED-ML file.

    Returns
    - SED-ML file with the output elements.
    """
    # Load the existing SED-ML XML document
    phrased_xml = ET.parse(sedml_file)
    root = phrased_xml.getroot()

    # Create a new Output element
    output = ET.Element("Output")

    # create unique plots for all instances in visualization_df['plotId']
    for plot_id, plot_data in visualization_df.groupby("plotId"):
        plot_name = plot_data["plotName"].iloc[0]

        # Create a Plot2D element for each plot
        plot2d = ET.SubElement(output, "Plot2D", id=plot_id, name=plot_name)

        # Add each curve to the plot
        for _, row in plot_data.iterrows():
            curve_id = row["datasetId"]
            curve_name = row["legendEntry"]
            x_data_gen_id = row["xValues"]
            y_data_gen_id = row["yValues"]

            # Create a Curve element within Plot2D
            curve = ET.SubElement(plot2d, "Curve", id=curve_id, name=curve_name)

            # Set attributes for xDataReference and yDataReference
            curve.set("xDataReference", x_data_gen_id)
            curve.set("yDataReference", y_data_gen_id)

    # Append the DataDescription to the SED-ML root
    root.append(output)

    ET.indent(root, space="    ")

    # Write back the modified SED-ML document
    phrased_xml.write(sedml_file, xml_declaration=True, encoding="UTF-8")

    print(f"Added Output to {sedml_file}")

    return sedml_file


def build_sedml_file(yaml_file: os.PathLike) -> None:
    """
    Combines the elements of the SED-ML file into a single string, converting \
    the string to a SED-ML file using PhraSED-ML.

    Parameters
    - yaml_file (os.PathLike): The path to the YAML file.

    Returns
    - None
    """
    petab_files = file_loader(yaml_file)

    phrasedml_str = f"""model1 = model "{petab_files['sbml file']}"\n"""

    model_id = extractors.get_model_id(petab_files["sbml file"])

    phrasedml_str += build_simulation(
        petab_files["conditions"], petab_files["measurements"]
    )

    phrasedml_str += build_tasks(model_id, petab_files["conditions"])

    # Convert the PhraSED-ML string to SED-ML
    sedml_output = phrasedml.convertString(phrasedml_str)

    if sedml_output is None:
        raise ValueError(f"Error converting to SED-ML: {phrasedml.getLastError()}")

    # Write the SED-ML file to disk
    sedml_file = os.path.join(os.path.dirname(yaml_file), "sedml_file.xml")
    with open(sedml_file, encoding="utf-8", mode="w") as file:
        file.write(sedml_output)

    # Use XML packages to parse and add a data generator section to the SED-ML
    sedml_output = build_data_generators(sedml_file, petab_files["observables"])

    # Add the data description to the SED-ML file
    sedml_output = build_data_descriptions(
        sedml_file, petab_files["measurements"], yaml_file
    )

    # Add the output elements to the SED-ML file
    sedml_output = build_output(petab_files["visualization"], sedml_file)

    print(f"SED-ML file written to {sedml_file}")
    return None


# -----------------------------end of script------------------------------------#

if __name__ == "__main__":
    args = parse_args()
    build_sedml_file(args.yaml_path)
