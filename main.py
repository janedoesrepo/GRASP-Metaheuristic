from exporter import Exporter
from experiment import Experiment
from graph import Graph
from optimizer import create_optimizers, OptimizationProcedure
from time import perf_counter
from typing import Dict, List, Generator


def create_instances(quantity: int = 10) -> Generator[Graph, None, None]:
    """Creates up to 10 instances of all possible combinations of graph and variant"""
    
    assert (1 <= quantity <= 10), f"The maximum number of instances per Graph and variation is 10, got {quantity}."
    
    graphs = [
        # "ARC83.IN2", "BARTHOLD.IN2", "HESKIA.IN2", "LUTZ2.IN2",
        "MITCHELL.IN2",
        # "ROSZIEG.IN2", "SAWYER30.IN2", "WEE-MAG.IN2"
    ]
    variants = ["TS0.25", "TS0.25-med", "TS0.75", "TS0.75-med"]
    instances = (
        Graph.parse_instance(f"data/Instances/{graph}_{variant}_EJ{ident}.txt")
        for graph in graphs
        for variant in variants
        for ident in range(1, quantity + 1)
    )

    return instances



def run_experiments(instances: Generator[Graph, None, None], optimizers: List[OptimizationProcedure]) -> List[Dict]:

    run_start = perf_counter()
    
    solutions = []
    for instance in instances:

        experiment = Experiment()
        experiment.run(instance, optimizers)
        
        solutions.extend(experiment.solutions)
        
        Exporter.export_instance_result(experiment.solutions, filename=f"{instance}")    

        print("Experiment Runtime:", perf_counter() - experiment.start_time)
        print("=" * 50, "\n")
        
    print(f"Full runtime: {perf_counter() - run_start}")

    return solutions


def main():
    
    # Define the number of instances per Graph in range(1,11)
    num_instances = 1

    # Create instances and optimization procedures
    instances = create_instances(quantity=num_instances)
    optimizers = create_optimizers()

    # run experiments
    results = run_experiments(instances, optimizers)

    # save experiments to disc
    Exporter.export_results(results, filename='all_results')


if __name__ == "__main__":
    main()
