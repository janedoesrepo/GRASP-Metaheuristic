from pathlib import Path
from time import perf_counter
from typing import Dict, Generator, List

from sualbsp_solver.data_model import Graph
from sualbsp_solver.experiment import Experiment
from sualbsp_solver.exporter import Exporter
from sualbsp_solver.martino_pastor_experiment import MartinoPastor2010Experiment
from sualbsp_solver.solver import OptimizationProcedure

# def run_experiments(
#     instances: Generator[Graph, None, None], optimizers: List[OptimizationProcedure]
# ) -> List[Dict]:

#     run_start = perf_counter()

#     solutions = []
#     for instance in instances:

#         experiment = Experiment()
#         experiment_start_time = perf_counter()  # Could be added to experiment
#         experiment.run(instance, optimizers)

#         solutions.extend(experiment.solutions)

#         Exporter.export_instance_result(experiment.solutions, filename=f"{instance}")

#         print("Experiment Runtime:", perf_counter() - experiment_start_time)
#         print("=" * 50, "\n")

#     print(f"Full runtime: {perf_counter() - run_start}")

#     return solutions


def main(
    data_dir: Path = Path("./data/"), results_dir: Path = Path("./results/")
) -> None:

    full_experiment = MartinoPastor2010Experiment(data_dir)
    full_experiment.run(results_dir)


if __name__ == "__main__":
    main()
