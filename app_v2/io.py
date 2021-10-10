import csv
import pathlib
from typing import Dict, List


def export_results(solutions: List[Dict], filename: str) -> None:
    """Writes all solutions to a single csv file"""

    
    # Export results to csv
    with open(f'app_v2/results/{filename}.csv', 'w', newline='') as csvfile:
        
        fieldnames = ['Instance', 'Heuristic', 'Num_Stations', 'Min_Stations', 'ARD', 'Runtime']       
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for solution in solutions:
            writer.writerow(solution)


def export_instance_result(instance_solutions: List[Dict], filename: str) -> None:
        
        print(f"Writing results to {filename}.csv")
        
        # Set result dir and create it, if it does not exist
        graph_name = filename.split('_')[0]
        result_dir = pathlib.Path(f"app_v2/results/{graph_name}/")
        result_dir.mkdir(parents=True, exist_ok=True)

        # Export results to csv
        with open(result_dir/f'{filename}.csv', 'w', newline='') as csvfile:
            
            fieldnames = ['Instance', 'Heuristic', 'Num_Stations', 'Min_Stations', 'ARD', 'Runtime']       
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for solution in instance_solutions:
                writer.writerow(solution)
