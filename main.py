import exporter
from experiment import Experiment
from graph import Graph
from optimizer import create_optimizers, OptimizationProcedure
from time import perf_counter
from typing import Dict, List


def create_instances(quantity: int = 10) -> List[Graph]:
    """Creates up to 10 instances of all possible combinations of graph and variant"""

    graphs = [
        # "ARC83.IN2", "BARTHOLD.IN2", "HESKIA.IN2", "LUTZ2.IN2",
        "MITCHELL.IN2",
        # "ROSZIEG.IN2", "SAWYER30.IN2", "WEE-MAG.IN2"
    ]
    variants = ["TS0.25", "TS0.25-med", "TS0.75", "TS0.75-med"]
    instances = [
        Graph(graph, variant, ident)
        for graph in graphs
        for variant in variants
        for ident in range(1, quantity + 1)
    ]

    return instances



def run_experiments(instances: List[Graph], optimizers: List[OptimizationProcedure]) -> List[Dict]:

    run_start = perf_counter()
    
    solutions = []
    for instance in instances:
        instance.parse_instance()

        experiment = Experiment()
        experiment.run(instance, optimizers)
        exporter.export_instance_result(experiment.solutions, filename=f"{instance}")    
        
        solutions.extend(experiment.solutions)

        print("Experiment Runtime:", perf_counter() - experiment.start_time)
        print("=" * 50, "\n")
        
    print(f"Full Runtime: {perf_counter() - run_start}")

    return solutions


def main(num_instances: int):

    # Create instances and optimization procedures
    instances = create_instances(quantity=num_instances)
    optimizers = create_optimizers()

    # run experiments
    results = run_experiments(instances, optimizers)

    # save experiments to disc
    exporter.export_results(results, filename='all_results')


if __name__ == "__main__":
    main(1)
