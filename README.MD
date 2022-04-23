[![PyTest](https://github.com/janedoesrepo/GRASP-Metaheuristic/actions/workflows/tests.yml/badge.svg)](https://github.com/janedoesrepo/GRASP-Metaheuristic/actions/workflows/tests.yml)

# SUABLPS Solver

A solver package for the sequence-dependent assembly line balancing and scheduling problem.

Available solvers are:
- Station Oriented Strategy (Heuristic with four possible ordering rules)
- Task Oriented Strategy (Heuristic with four possible ordering rules)
- Greed Randomized Adaptive Search Procedure (GRASP)

## Usage 

`python -m main.py` 

In main.py the experiment is created, including all **320 instances of the assembly line balancing problem with setups 
(SUALBSP)**. For each instance ten solutions will be computed, one with each of the eight heuristics and two
 with the Greedy-Randomized-Adaptive-Search-Procedure (GRASP). GRASP runs once with five (GRASP-5) and once with 10 
 (GRASP-10) iterations. Afterwards the Average Relative Deviation (ARD) of each solution from the correspondend best solution is computed.
 
The following results will be saved:
 - one file for each instance of the form  <instance_name>.csv
 - a compilation of all results in the file „all_results.xlsx"

## Problem Definition

The sequence-dependent assembly line balancing and scheduling problem (SUALBSP) is an extension of SALBP-1. It additionally considers setup times between tasks. For example, such sequence-dependent setup times are:

- walking times of the worker to a material box, to the next mounting position on the same workpiece or to the next workpiece
- time for tool changes
- material handling times for unpacking, withdrawal from a box etc.

The problem was origonally introduced by Andrés et al. (2008) and modified by differentiating between forward setup times (walking concerning the same workpiece) and backward setup times (walking to the next workpiece at the end of each cycle) by Scholl et al. (2013).

Source: https://assembly-line-balancing.de/sualbsp/