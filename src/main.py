from time import perf_counter
from typing import Dict, Generator, List

from sualbsp_solver.config import GraphConfig
from sualbsp_solver.data_model import Graph
from sualbsp_solver.experiment import Experiment
from sualbsp_solver.exporter import Exporter
from sualbsp_solver.solver import OptimizationProcedure, create_optimizers


def run_experiments(instances: Generator[Graph, None, None], optimizers: List[OptimizationProcedure]) -> List[Dict]:

    run_start = perf_counter()
    
    solutions = []
    for instance in instances:

        experiment = Experiment()
        experiment_start_time = perf_counter() # Could be added to experiment
        experiment.run(instance, optimizers)
        
        solutions.extend(experiment.solutions)
        
        Exporter.export_instance_result(experiment.solutions, filename=f"{instance}")    

        print("Experiment Runtime:", perf_counter() - experiment_start_time)
        print("=" * 50, "\n")
        
    print(f"Full runtime: {perf_counter() - run_start}")

    return solutions

def main(config_path: str) -> None:
    
    # read the configuration settings from a JSON file
    config = GraphConfig.read(config_path)

    # Create instances and optimization procedures
    instances = Graph.from_IN2(config)
    optimizers = create_optimizers()

    # run experiments
    results = run_experiments(instances, optimizers)

    # save experiments to disc
    Exporter.export_results(results, config.all_results_file)

if __name__ == "__main__":
    main(config_path="./src/sualbsp_solver/config/config.json")
