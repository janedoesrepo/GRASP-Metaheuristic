import pathlib
from typing import Dict
import xlsxwriter
import csv


def export_results(solutions, best_solutions) -> None:
    """Writes the solutions to an excel workbook"""

    print("Writing combined results to results.xlsx")
    # create a workbook and a worksheet
    workbook = xlsxwriter.Workbook("app_v2/results/all_results.xlsx")
    worksheet = workbook.add_worksheet()

    # write headers in bold
    bold = workbook.add_format({"bold": 1})
    worksheet.write("A1", "Instance", bold)
    worksheet.write("B1", "Heuristic", bold)
    worksheet.write("C1", "Stations", bold)
    worksheet.write("D1", "BS", bold)
    worksheet.write("E1", "ARD", bold)
    worksheet.write("F1", "Runtime", bold)

    row = 1
    for instance, apply_heuristic in solutions.items():
        for heuristic, solution in apply_heuristic.items():
            worksheet.write_string(row, 0, instance.__str__())
            worksheet.write_string(row, 1, heuristic.__str__())
            worksheet.write_number(row, 2, solution["m"])
            worksheet.write_number(row, 3, best_solutions[instance])
            worksheet.write_number(row, 4, solution["ARD"])
            worksheet.write_number(row, 5, solution["rt"])
            row += 1

    workbook.close()


def export_instance_result(instance_name: str, instance_solutions: Dict) -> None:
        
        print(f"Writing results to {instance_name}.csv")
        
        # Set result dir and create it, if it does not exist
        graph_name = instance_name.split('_')[0]
        result_dir = pathlib.Path(f"app_v2/results/{graph_name}/")
        result_dir.mkdir(parents=True, exist_ok=True)

        # Export results to csv
        with open(result_dir/f'{instance_name}.csv', 'w', newline='') as csvfile:
            
            fieldnames = ['Instance', 'Heuristic', 'Num_Stations', 'Min_Stations', 'ARD', 'Runtime']       
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for _, result in instance_solutions.items():
                writer.writerow(result)
