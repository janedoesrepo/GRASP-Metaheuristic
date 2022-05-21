from io import BytesIO
from pathlib import Path
from time import perf_counter
from zipfile import ZipFile

import requests

from sualbsp_solver.exporter import Exporter

from .experiment import Experiment


def get_dataset(dataset_dir: Path, url: str):
    """Download and unzip the Dataset at `url`."""

    dataset = requests.get(url)
    print(">>> Download Completed")

    zipfile = ZipFile(BytesIO(dataset.content))
    zipfile.extractall(dataset_dir)


class MartinoPastor2010Experiment:
    """The full Martino and Pastor experiment."""

    def __init__(self, data_dir: Path) -> None:
        self.dataset_name = "Martino_and_Pastor_2010"
        self.dataset_url = "https://assembly-line-balancing.de/wp-content/uploads/2017/01/SUALBSP-Instances_Capacho-and-Pastor_2008.zip"
        self.graphs = self._load_data(data_dir)

    def _load_data(self, data_dir: Path) -> list[Path]:
        dataset_path = data_dir / self.dataset_name

        if not dataset_path.exists():
            print(
                f">>> Dataset {self.dataset_name} not found. Downloading from {self.dataset_url}..."
            )
            get_dataset(dataset_path, self.dataset_url)

        return list(dataset_path.rglob("*.txt"))

    def run(self, results_dir: Path) -> None:

        run_start = perf_counter()

        solutions = []
        for graph in self.graphs:

            experiment = Experiment(graph)
            results = experiment.run()

            solutions.extend(results)

            results_file = results_dir / f"{graph.name}.csv"
            Exporter.export_instance_result(results, destination=results_file)

            print("Experiment Runtime:", perf_counter() - experiment.start_time)
            print("=" * 50, "\n")

        print(f"Full runtime: {perf_counter() - run_start}")

        all_results_file = results_dir / f"{self.dataset_name}.csv"
        Exporter.export_results(solutions, all_results_file)
