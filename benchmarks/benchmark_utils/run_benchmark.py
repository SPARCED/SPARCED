import os
import sys
import pickle
import importlib
from benchmark_utils.job_organization import Organizer as org
from benchmark_utils.arguements import parse_args
from benchmark_utils.utils import Utils
from benchmark_utils.sparced_simulation import Simulation
from benchmark_utils.observable_calc import ObservableCalculator
from benchmark_utils.visualization import Visualizer
args = parse_args()

# Append utilities and model directories to the path
sys.path.append(args.model)

Utils._add_amici_path(args.model) 

sparced = Utils._swig_interface_path(args.model)
sys.path.append(sparced)
SPARCED = importlib.import_module(sparced.split('/')[-1].split('.')[0])


class RunBenchmark:
    """Input the PEtab files and broadcast them to all processes. Then, load 
        the SBML model and create a list of unique conditions. Assign tasks 
        to ranks based on the number of jobs and the number of ranks. Send 
        the results to the root rank and save the results. If applicable, 
        iterate through the observable calculator and save any experimental 
        data with the observable-results.
    input:
        yaml_file: str - path to the YAML file
        observable: int - 1 for run with observable, 
                    0 for run without observable
        name: str - name of the file to save the results
        model_path: str - path to the model directory
        benchmark: str - benchmark to evaluate the model against
    
    output:
        returns the results of the SPARCED model unit test simulation
    """


    def __init__(self):
        
        wd = os.path.dirname(os.path.abspath(__file__))

        sparced_root = ('/'.join(wd.split(os.path.sep)[:wd.split(os.path.sep)
                                              .index('SPARCED')+1]))

        try: 
            args.benchmark = args.benchmark.split('/')[0]
            if args.benchmark != 'benchmark_utils':
                yaml_path = os.path.join(sparced_root, 
                        f'benchmarks/{args.benchmark}/{args.benchmark}.yml') 
                
                assert os.path.exists(yaml_path)

        except AssertionError:
            raise FileNotFoundError(f'{args.benchmark} is not a valid benchmark')
        try:
            assert os.path.exists(args.model)
        except AssertionError:
            raise FileNotFoundError(f'{args.model} is not a valid model path')

        self.yaml_file = yaml_path
        self.model_path = args.model
        self.benchmark = args.benchmark
        self.observable = args.observable
        self.name = args.name

        self.communicator, self.rank, self.size = org.mpi_communicator()

 
    def run(self):
        """Run the SPARCED model unit test simulation

        Arguements:
            self: object - the RunBenchmark object

        Returns:
            results: dict - the results of the SPARCED model unit test simulation
        """

        # (s)bml_file, (c)onditions_df, (m)easurement_df, 
        # (o)bservable_df, (p)arameters_df, (v)isualization_df 
        # abbreviated notation for brevity
        sbml_file, c, m, o, p, v = org.broadcast_petab_files(self.rank, 
                                                     self.communicator, 
                                                     self.yaml_file, 
                                                     self.model_path
                                                     )

        self.sbm_file = sbml_file # SBML file
        self.conditions_df = c # Conditions dataframe
        self.measurement_df = m # Measurement dataframe
        self.observable_df = o # Observable dataframe
        self.parameters_df = p # Parameters dataframe
        self.visualization_df = v # Visualization dataframe

        # Pause placement to ensure all ranks receive the broadcasted files:
        self.communicator.Barrier()

        # Create an instance of the AMICI model. 
        self.model = SPARCED.getModel()
        solver = self.model.getSolver()
        solver.setMaxSteps = 1e10

        # Gene regulation and OmicsData files are used for stochastic gene
        # expression. 
        genereg, omicsdata = Utils._extract_simulation_files(args.model)

        # Catalogue each rank's list of tasks at root (rank 0)
        if self.rank == 0:
            
            # Results dictionary is initialized prior to simulation for convenience
            self.results_dictionary = Utils._results_dictionary(self.conditions_df, 
                                                                self.measurement_df
                                                                )
        
        # Determine the number of rounds and the directory of tasks for each rank
        rounds_to_complete, rank_jobs_directory = org.task_organization(self.rank, 
                                                                        self.size, 
                                                                        self.communicator, 
                                                                        self.conditions_df,
                                                                        self. measurement_df
                                                                        )
        # For every cell and condition, run the simulation based on the number of rounds
        for round_i in range(rounds_to_complete):
            
            if self.rank == 0:
                print(f'Round {round_i+1} of {rounds_to_complete}')

            task = org.task_assignment(rank = self.rank, 
                                       size = self.size,
                                       communicator = self.communicator, 
                                       rank_jobs_directory = rank_jobs_directory, 
                                       round_i = round_i, 
                                       conditions_df = self.conditions_df, 
                                       measurement_df = self.measurement_df)

            if task is None:
                print(f'Rank {self.rank} has no tasks to complete')
                continue

            condition, cell, condition_id = Utils._condition_cell_id(task, 
                                                            self.conditions_df, 
                                                           self.measurement_df)
            
            print(f"Rank {self.rank} is running {condition_id} for cell {cell}")

            # Run the simulation for the given condition
            xoutS, toutS, xoutG = Simulation(model_path=self.model_path,
                                             yaml_file=self.yaml_file, 
                                             model=self.model, 
                                             conditions_df=self.conditions_df, 
                                             measurement_df=self.measurement_df, 
                                             parameters_df=self.parameters_df, 
                                             sbml_file=sbml_file,
                                             f_genereg=genereg,
                                             f_omics=omicsdata
                                            )._run_condition_simulation(condition)

            # Results are packaged into a single object to reduce the number of items sent via MPI
            parcel = org.package_results(xoutS = xoutS, toutS= toutS, xoutG= xoutG,
                                         condition_id=condition_id, cell=cell
                                         )

            if self.rank == 0:
                
                # Store rank 0's results prior to storing other ranks
                self.results_dictionary = org.results_storage(results_dict = self.results_dictionary, 
                                                              results_catalogue = parcel
                                                             )               
              
                # Define the total number of jobs for the results aggregation stage
                total_jobs = Utils._total_tasks(self.conditions_df, self.measurement_df)

                # Collect results from other ranks and store in results dictionary            
                self.results_dictionary = org.results_aggregation(size = self.size, 
                                                                  communicator = self.communicator, 
                                                                  results_dict = self.results_dictionary, 
                                                                  round_i = round_i, 
                                                                  total_jobs = len(total_jobs)
                                                                 )
            else:
                # All non-root ranks send results to rank 0
                self.communicator.send(parcel, dest=0, tag=round_i)

            print(f"Rank {self.rank} has completed {condition_id} for cell {cell}")

        return self
    

    def save_results(self):
        """Save the results of the simulation to a file
        input:
            results: dict - the results of the simulation
            name: str - the name of the file to save the results
        output:
            returns the saved results as a nested dictionary within
            a pickle file
        """

        # Benchmark results are stored within the specified model directory
        yaml_name = os.path.basename(self.yaml_file).split('.')[0]

        results_directory = os.path.join(self.model_path, 'results')
            
        if not os.path.exists(results_directory): 
            os.makedirs(results_directory)

        # Final output is saved in pickle format
        results_path = os.path.join(results_directory, f"{yaml_name}.pkl")

        if self.name is not None:
            results_path = os.path.join(results_directory, 
                                        f"{self.name}.pkl"
                                        )

        with open(results_path, 'wb') as f:
            pickle.dump(self.results_dictionary, f)                 


    def observable_calculation(self) -> dict:
        """Calculate the observables and compare to the experimental data.
        input:
            results: dict - results of the SPARCED model unit test simulation
        output:
            returns the results of the SPARCED model unit test simulation
        """
        if self.rank == 0 and self.observable == 1:

            observable_calculator = ObservableCalculator(yaml_file=self.yaml_file, 
                                                        model=self.model, 
                                                        measurement_df=self.measurement_df, 
                                                        observable_df=self.observable_df,  
                                                        results_dict=self.results_dictionary)

            observable_dict = observable_calculator.__call__()

            self.results_dictionary = observable_calculator._add_experimental_data(observable_dict)

            RunBenchmark.save_results(self)

        elif self.rank != 0:
            return None

    
    def run_visualizer(self):
        """Generate a unit test plot from the visualization dataframe
        input:
            petab_files_data: dict - dictionary of PEtab files
            
        output:
            returns a unit test plot generated by matplotlib
        """
        
        if self.rank == 0 and self.visualization_df is not None:

            print('Generating Benchmark Plot')

            results_directory = os.path.join(self.model_path, 'results')

            fig = Visualizer(yaml_file=self.yaml_file, 
                             results_dict=self.results_dictionary, 
                             visualization_df=self.visualization_df, 
                             observable_df=self.observable_df, 
                             measurement_df=self.measurement_df
                             ).dynamic_plot()
        
            fig.savefig(os.path.join(results_directory, f"{self.name}.png"))
