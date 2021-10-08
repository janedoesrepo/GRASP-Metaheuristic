import xlsxwriter


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
