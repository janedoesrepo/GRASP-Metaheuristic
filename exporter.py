import csv
import pathlib
from typing import Dict, List

class Exporter:
    
    @staticmethod
    def _write_csv(filepath, solutions: List[Dict]) -> None:
        """Exports solutions to csv"""
        
        with open(filepath, 'w', newline='') as csvfile:
            
            fieldnames = ['Instance', 'Strategy', 'Num_Stations', 'Min_Stations', 'ARD', 'Runtime']       
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for solution in solutions:
                writer.writerow(solution)
            
    @classmethod
    def export_results(cls, solutions: List[Dict], filename: str) -> None:
        """Export all results to a single csv-file"""
        
        # Set filepath
        filepath = f'results/{filename}.csv'
        
        cls._write_csv(filepath, solutions)

    @classmethod
    def export_instance_result(cls, instance_solutions: List[Dict], filename: str) -> None:
        """Export the results of solving an instance to a separate csv-file"""
        
        print(f"Writing results to {filename}.csv")
        
        # Set result dir and create it, if it does not exist
        graph_name = filename.split('_')[0]
        result_dir = pathlib.Path(f"results/{graph_name}/")
        result_dir.mkdir(parents=True, exist_ok=True)
    
        # Set filepath
        filepath = result_dir/f'{filename}.csv'

        cls._write_csv(filepath, instance_solutions)
