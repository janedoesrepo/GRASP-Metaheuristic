Usage: `python -m main.py`

In main.py the experiment is created, including all **320 instances of the assembly line balancing problem with setups 
(SUALBSP)**. For each instance ten solutions will be computed, one with each of the eight heuristics and two
 with the Greedy-Randomized-Adaptive-Search-Procedure (GRASP). GRASP runs once with five (GRASP-5) and once with 10 
 (GRASP-10) iterations. Afterwards the Average Relative Deviation (ARD) of each solution from the correspondend best solution is computed
 
The following results will be saved:
 - one file for each instance of the form  <instance_name>.csv
 - a compilation of all results in the file „all_results.xlsx

Data Source: https://assembly-line-balancing.de/sualbsp/data-set-of-andres-et-al-2008/
