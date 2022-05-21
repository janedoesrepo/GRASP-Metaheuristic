import csv
from pathlib import Path
from typing import Dict, List


def write_csv(filepath: Path, solutions: list[dict]) -> None:
    """Exports solutions to csv."""

    with filepath.open("w", newline="") as csvfile:

        fieldnames = [
            "Instance",
            "Strategy",
            "Num_Stations",
            "Min_Stations",
            "ARD",
            "Runtime",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for solution in solutions:
            writer.writerow(solution)


class Exporter:
    @staticmethod
    def export_results(solutions: list[dict], destination: Path) -> None:
        """Export all results to a single csv-file."""
        write_csv(destination, solutions)

    @staticmethod
    def export_instance_result(
        instance_solutions: list[dict], destination: Path
    ) -> None:
        """Export the results of solving an instance to a separate csv-file."""

        print(f"Writing results to {destination}")

        # Set result dir and create it, if it does not exist
        destination.parent.mkdir(parents=True, exist_ok=True)

        write_csv(destination, instance_solutions)
