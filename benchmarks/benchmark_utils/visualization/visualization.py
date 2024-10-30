#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class Visualizer:
    def __init__(self, yaml_file: str, results_dict: dict, 
                 visualization_df: pd.DataFrame, observable_df: pd.DataFrame,
                   measurement_df: pd.DataFrame):
        """This class is designed to plot and save the visualization data.
        input:
            yaml_file: str - path to the YAML file
            result_dict: dict - dictionary containing the simulation results
            visualization_df: str - path to the visualization dataframe
            observable_df: str - path to the observable dataframe
            model: str - path to the SBML model
            measurement_df: str - path to the measurement dataframe
        """
        self.yaml_file = yaml_file
        self.results_dict = results_dict
        self.visualization_df = visualization_df
        self.observable_df = observable_df
        self.measurement_df = measurement_df

    def dynamic_plot(self):
        """Parses the information within the visualization dataframe and 
        plots simulation data accordingly. Information within the 
        visualization dataframe must conform to PEtab standards.

        output: plots the simulation data according to the visualization dataframe
        """
        unique_plots = self.visualization_df['plotId'].unique()

        num_rows, num_cols, plot_position_matrix = generate_position_matrix(len(unique_plots))
        unique_plt_positions = {}

        for i, plotId in enumerate(unique_plots):
            # Find the position from the matrix
            row, col = np.where(plot_position_matrix == i)
            row, col = row[0], col[0]
            unique_plt_positions[plotId] = (row, col)

        # Set global plot parameters
        plt.rcParams['axes.labelsize'] = 14
        plt.rcParams['xtick.labelsize'] = 12    
        plt.rcParams['ytick.labelsize'] = 12
        plt.rcParams['legend.fontsize'] = 12
        plt.rcParams['font.weight'] = 'bold' 

        # Create a subplot figure with the determined grid size
        fig, axes = plt.subplots(num_rows, num_cols, figsize=(num_cols * 4, num_rows * 4))

        # Ensure axes is always a 2D array
        if num_rows == 1 and num_cols == 1:
            axes = np.array([[axes]])
        elif num_rows == 1 or num_cols == 1:
            axes = axes.reshape((max(num_rows, num_cols),1))

        for i, plotId in enumerate(self.visualization_df['plotId']):

            plot_type = self.visualization_df['plotTypeSimulation'][i]
            yValue = self.visualization_df['yValues'][i]
            xValue = self.visualization_df['xValues'][i]

            xScale, yScale = (self.visualization_df['xScale'][i], 
                              self.visualization_df['yScale'][i])
            
            xLabel, yLabel = (self.visualization_df['xLabel'][i], 
                              self.visualization_df['yLabel'][i])
            
            # Find the position from the matrix
            row, col = unique_plt_positions[plotId]

            condition = self.visualization_df['datasetId'][i]

            identifier = ([self.results_dict[identifier][self.results_dict[identifier]
                                                    ['conditionId']==condition]]
                                                    )

            if plot_type == 'ScatterPlot':

                axes = Visualizer.scatter_plot(xValue, yValue,
                                         self.visualization_df['legendEntry'][i],
                                         self.visualization_df['Color'][i], 
                                         identifier)  

            elif plot_type == 'LinePlot':

                axes = Visualizer.line_plot(xValue, yValue,
                                         self.visualization_df['legendEntry'][i],
                                         self.visualization_df['Color'][i], 
                                         identifier)  

            elif plot_type == 'BarPlot':

                axes = Visualizer.bar_plot(xValue, yValue,
                                         self.visualization_df['legendEntry'][i],
                                         self.visualization_df['Color'][i], 
                                         identifier)             


            axes[row, col].set_xlabel(xLabel, weight='bold')
            axes[row, col].set_ylabel(yLabel, weight='bold')
            axes[row, col].set_xscale(xScale)
            axes[row, col].set_yscale(yScale)
            axes[row, col].set_title(self.visualization_df['plotName'][i], weight='bold')

        # Remove unused subplots
        for i in range(len(unique_plots), num_rows * num_cols):
            row, col = np.where(plot_position_matrix == i)
            row, col = row[0], col[0]
                
            fig.delaxes(axes[row, col])

        # Get unique handles and labels for the legend
        lines_labels = [ax.get_legend_handles_labels() for ax in fig.axes]
        unique_lines = []
        unique_labels = set()
        for lines, labels in lines_labels:
            for line, label in zip(lines, labels):
                if label not in unique_labels:
                    unique_lines.append(line)
                    unique_labels.add(label)
                else:
                    idx = list(unique_labels).index(label)
                    if unique_lines[idx] != line:
                        unique_lines[idx] = line

        # Create a legend using unique handles and labels
        fig.legend(unique_lines, unique_labels, frameon=False)

        # # Adjust layout
        plt.tight_layout()

        return fig


    def replicate_plot_settings(ax, replicate: int)-> plt.axis:
        """Provided a replicate, reassigns the specific attributes of the plot
        to have a lower alpha value, and a smaller linewidth.
        
        Parameters:
            ax: plt.axis - axis object
            replicate: int - replicate number
        
        Returns:
            ax: plt.axis - axis object with updated settings
        """
        ax.lines[replicate].set_alpha(0.5)
        ax.lines[replicate].set_linewidth(1)
    
        return ax
        

    def scatter_plot(self, xValue: str, yValue: str, legendEntry: str, 
                     Color: str, identifier: str):
        """Generates a scatter plot based on the provided parameters
        
        Parameters:
            xValue: str - x-axis value
            yValue: str - y-axis value
            legendEntry: str - legend entry
            Color: str - color
            identifier: str - identifier
        
        Returns:
            ax: plt.axis - axis object
        """
        if len(identifier) > 1:
            for replicate in range(len(identifier)):
                yvals = self.results_dict[identifier][replicate][yValue]
                if xValue == 'time':
                    xvals = self.results_dict[identifier][replicate]['toutS']/3600
                else:
                    xvals = self.results_dict[identifier][replicate][xValue]
                ax.scatter(xvals, yvals, 
                                    label=legendEntry, 
                                    color=Color, 
                                    linewidth=3)
                
                ax = Visualizer.replicate_plot_settings(ax, replicate)

        else:
            yvals = self.results_dict[identifier][yValue]
            if xValue == 'time':
                xvals = self.results_dict[identifier]['toutS']/3600
            else:
                xvals = self.results_dict[identifier][xValue]
            ax.scatter(xvals, yvals, 
                                label=legendEntry, 
                                color=Color, 
                                linewidth=3)
    
        return ax

    def line_plot(self, xValue: str, yValue: str, xScale: str, yScale: str,
                     xLabel: str, yLabel: str, plotName: str, legendEntry: str, 
                     Color: str, datasetId: str, plotId: str, identifier: str) -> plt.axis:
        """Generates a line plot based on the provided parameters
        
        Parameters:
            xValue: str - x-axis value
            yValue: str - y-axis value
            legendEntry: str - legend entry
            Color: str - color
            identifier: str - identifier
        
        Returns:
            ax: plt.axis - axis object
        """
        if len(identifier) > 1:
            for replicate in range(len(identifier)):
                yvals = self.results_dict[identifier][replicate][yValue]['xoutS']
                if xValue == 'time':
                    xvals = self.results_dict[identifier][replicate][yValue]['toutS']/3600
                else:
                    xvals = self.results_dict[identifier][replicate][xValue]['xoutS']
                ax.plot(xvals, yvals, 
                                label=legendEntry, 
                                color=Color, 
                                linewidth=3)
                
                ax = Visualizer.replicate_plot_settings(ax, replicate)

        else:
            yvals = self.results_dict[identifier][yValue]['xoutS']
            if xValue == 'time':
                xvals = self.results_dict[identifier][yValue]['toutS']/3600
            else:
                xvals = self.results_dict[identifier][xValue]['xoutS']
            ax.plot(xvals, yvals, 
                            label=legendEntry, 
                            color=Color, 
                            linewidth=3)
            
        return ax

    def bar_plot(self, xValue: str, yValue: str, xScale: str, yScale: str,
                        xLabel: str, yLabel: str, plotName: str, legendEntry: str, 
                        Color: str, datasetId: str, plotId: str, identifier: str) -> plt.axis:
            """Generates a bar plot based on the provided parameters
            
            Parameters:
            xValue: str - x-axis value
            yValue: str - y-axis value
            legendEntry: str - legend entry
            Color: str - color
            identifier: str - identifier
            
            Returns:
                ax: plt.axis - axis object
            """
            if len(identifier) > 1:
                for replicate in range(len(identifier)):
                    yvals = self.results_dict[identifier][replicate][yValue]['xoutS']
                    if xValue == 'time':
                        xvals = self.results_dict[identifier][replicate][yValue]['toutS']/3600
                    else:
                        xvals = self.results_dict[identifier][replicate][xValue]['xoutS']
                    ax.bar(xvals, yvals, 
                                    label=legendEntry, 
                                    color=Color, 
                                    linewidth=3)
                    
                    ax = Visualizer.replicate_plot_settings(ax, replicate)
    
            else:
                yvals = self.results_dict[identifier][yValue]['xoutS']
                if xValue == 'time':
                    xvals = self.results_dict[identifier][yValue]['toutS']/3600
                else:
                    xvals = self.results_dict[identifier][xValue]['xoutS']
                ax.bar(xvals, yvals, 
                                label=legendEntry, 
                                color=Color, 
                                linewidth=3)

            return ax
    

@staticmethod
def generate_position_matrix(num_plots):
    """Generates a position matrix based on the number of plots to be generated
    input:
        num_plots: int - number of plots to be generated

    output:
        num_rows: int - number of rows in the plot grid
        num_cols: int - number of columns in the plot grid
        position_matrix: np.array - matrix containing the position of each plot
            in the grid
    """

    side_length = int(np.ceil(np.sqrt(num_plots)))
    
    position_matrix = np.arange(side_length ** 2).reshape((side_length,
                                                            side_length)).T
    
    num_rows, num_cols = position_matrix.shape

    return num_rows, num_cols, position_matrix

