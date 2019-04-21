# load system packages
from time import perf_counter
from copy import deepcopy
import xlsxwriter


# load own packages
from dataimport import getData
from grasp import grasp
from heuristics import heuristics

print('-'*25)

""" Create Instances """
names = ["ARC83.IN2", "BARTHOLD.IN2", "HESKIA.IN2", "LUTZ2.IN2", "MITCHELL.IN2", "ROSZIEG.IN2", "SAWYER30.IN2", "WEE-MAG.IN2"]
names = ["ARC83.IN2"]
variants = ["_TS0.25_EJ", "_TS0.25-med_EJ", "_TS0.75_EJ", "_TS0.75-med_EJ"]
variants = ["_TS0.25_EJ"]
instances = []
for name in names:
    for variant in variants:
        for i in range(1, 5):
            instance = name + variant + str(i)
            instances.append(instance)

""" Define Heuristic Procedures """
strategies = ['SH', 'TH']
rules = ['max_ts', 'min_ts', 'max_s', 'min_s']

procedures = []
for strategy in strategies:
    for rule in rules:
        procedure = strategy + '-' + rule
        procedures.append(procedure)

solutions = {}
best_solutions = {}
for instance in instances:

    instance_solutions = {}

    t0 = perf_counter()
    n, c, cl, t, relations, tsu = getData(instance + '.txt')    # get data

    """ Apply heuristic rules """
    for procedure in procedures:
        print("Applying %s to %s" % (procedure, instance))
        t1 = perf_counter()
        solution = heuristics(cl[:], deepcopy(relations), t, tsu, c, procedure)     # apply heuristic rule
        t2 = perf_counter()
        runtime = t2-t1
        instance_solutions[procedure] = dict(m=len(solution), rt=runtime, sol=solution)

    """ Apply GRASP """
    alpha = 0.3

    # Run GRASP-5
    print("Applying GRASP-5 meta heuristic to " + instance)
    num_iter = 5
    t3 = perf_counter()
    _, _, solution = grasp(cl, relations, t, tsu, c, num_iter, alpha)   # apply GRASP
    t4 = perf_counter()
    runtime = t4-t3
    instance_solutions['GRASP-5'] = dict(m=len(solution), rt=runtime, sol=solution)

    # Run GRASP-10
    print("Applying GRASP-10 meta heuristic to " + instance)
    num_iter = 10
    t5 = perf_counter()
    _, _, solution = grasp(cl, relations, t, tsu, c, num_iter, alpha)
    t6 = perf_counter()
    runtime = t6-t5
    instance_solutions['GRASP-10'] = dict(m=len(solution), rt=runtime, sol=solution)

    """ Postprocessing """
    t7 = perf_counter()
    runtime = t7 - t0

    # find best solution BS for each instance
    BS = []
    for procedure, solution in instance_solutions.items():
        BS.append(solution['m'])
    BS = min(BS)
    best_solutions[instance] = BS

    # compute Average Relative Deviation for each solution
    for _, solution in instance_solutions.items():
        ARD = 100 * ((solution['m'] - BS) / BS)
        solution['ARD'] = ARD

    # save solutions for later use
    solutions[instance] = instance_solutions

    """ Write data to a xlsx-file """
    print("Writing results to " + instance + '.xlsx')

    # create a workbook and a worksheet
    workbook = xlsxwriter.Workbook('../results/' + instance + '.xlsx')
    worksheet = workbook.add_worksheet()

    # write headers in bold
    bold = workbook.add_format({'bold': 1})
    worksheet.write('A1', 'Instanz', bold)
    worksheet.write('B1', 'Prozedur', bold)
    worksheet.write('C1', 'Stationszahl', bold)
    worksheet.write('D1', 'BS', bold)
    worksheet.write('E1', 'ARD', bold)
    worksheet.write('F1', 'Laufzeit', bold)

    # write data
    row = 1
    for procedure, solution in instance_solutions.items():
        worksheet.write_string(row, 0, instance)
        worksheet.write_string(row, 1, procedure)
        worksheet.write_number(row, 2, solution['m'])
        worksheet.write_number(row, 3, best_solutions[instance])
        worksheet.write_number(row, 4, solution['ARD'])
        worksheet.write_number(row, 5, solution['rt'])

        row += 1

    # close workbook
    workbook.close()

    print("Gesamtdauer:", runtime)
    print("-" * 25, "\n")


""" Write all solutions to a single xlsx-file """
print("Writing results to results.xlsx")

# create a workbook and a worksheet
workbook = xlsxwriter.Workbook('../results/' + 'results.xlsx')
worksheet = workbook.add_worksheet()

# write headers in bold
bold = workbook.add_format({'bold': 1})
worksheet.write('A1', 'Instanz', bold)
worksheet.write('B1', 'Prozedur', bold)
worksheet.write('C1', 'Stationszahl', bold)
worksheet.write('D1', 'BS', bold)
worksheet.write('E1', 'ARD', bold)
worksheet.write('F1', 'Laufzeit', bold)

# write data
row = 1
for instance, procedures in solutions.items():
    for procedure, solution in procedures.items():
        worksheet.write_string(row, 0, instance)
        worksheet.write_string(row, 1, procedure)
        worksheet.write_number(row, 2, solution['m'])
        worksheet.write_number(row, 3, best_solutions[instance])
        worksheet.write_number(row, 4, solution['ARD'])
        worksheet.write_number(row, 5, solution['rt'])

        row += 1

# close workbook
workbook.close()

print("Computations successful")
