from config import read_config
from exporter import Exporter
from experiment import Experiment
from graph import Graph
from optimizer import create_optimizers, OptimizationProcedure
from time import perf_counter
from typing import Dict, List, Generator

def run_experiments(instances: Generator[Graph, None, None], optimizers: List[OptimizationProcedure]) -> List[Dict]:

    run_start = perf_counter()
    
    solutions = []
    for instance in instances:

        experiment = Experiment()
        experiment_start_time = perf_counter()
        experiment.run(instance, optimizers)
        
        solutions.extend(experiment.solutions)
        
        Exporter.export_instance_result(experiment.solutions, filename=f"{instance}")    

        print("Experiment Runtime:", perf_counter() - experiment_start_time)
        print("=" * 50, "\n")
        
    print(f"Full runtime: {perf_counter() - run_start}")

    return solutions

def main():
    
    # read the configuration settings from a JSON file
    config = read_config("./config.json")

    # Create instances and optimization procedures
    instances = Graph.from_IN2(config)
    optimizers = create_optimizers()

    # run experiments
    results = run_experiments(instances, optimizers)

    # save experiments to disc
    Exporter.export_results(results, file_path=config.all_results_file)

if __name__ == "__main__":
    main()
