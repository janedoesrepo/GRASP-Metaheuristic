from __future__ import annotations
from typing import Generator, List
from task import Task


class Graph:

    def __init__(self, tasks: List[Task], cycle_time: int, name: str = "") -> None:
        self.tasks = tasks
        self.cycle_time = cycle_time
        self.name = name

    def __str__(self) -> str:
        return f"{self.name}"

    @staticmethod
    def parse_instance(filepath: str) -> Graph:
        """Import-function for the data set of Martino and Pastor (2010)
        The data is available at https://www.assembly-line-balancing.de/sualbsp

        line 1:                     n; number of tasks
        line 2:                     p; number of direct precedence relations
        line 3:                     c; cycle time
        lines 4 to 4+n-1:           cl, t; id task, processing time
        lines 4+n to 4+n+p-1:       relations; direct precedence relations in form i,j
        lines 4+n+p to 4+2n+p-1:    tsu; setup times
        """

        with open(filepath, "r") as file:

            # read first three lines
            num_tasks = int(file.readline())
            num_relations = int(file.readline())
            cycle_time = int(file.readline())

            # Create Tasks with id and processing times
            tasks: List[Task] = []
            for _ in range(num_tasks):
                task_id, processing_time = file.readline().split(',')
                tasks.append(Task(int(task_id), int(processing_time)))

            # Add the ids of the predecessor to each Task
            for _ in range(num_relations):
                predecessor_id, successor_id = file.readline().split(',')
                tasks[int(successor_id)].predecessors.append(int(predecessor_id))

            # Add the setup times from one Task to all other Tasks
            for i in range(num_tasks):
                setup_times_i = file.readline().split(',')
                tasks[i].setup_times = list(map(int, setup_times_i))
        
        print(f"*Import of {filepath} successful!*")
        
        name = filepath.split('/')[-1][:-4]

        return Graph(tasks, cycle_time, name)
    
    @staticmethod
    def from_IN2(data_dir: str, graphs: List[str] = None, variants: List[str] = None, quantity: int = 10) -> Generator[Graph, None, None]:
        """Creates up to 10 instances of all possible combinations of graph and variant"""
        assert (1 <= quantity <= 10), f"The maximum number of instances per Graph and variation is 10, got {quantity}."
        
        if graphs is None:
            graphs = ["ARC83.IN2", "BARTHOLD.IN2", "HESKIA.IN2", "LUTZ2.IN2", "MITCHELL.IN2", "ROSZIEG.IN2", "SAWYER30.IN2", "WEE-MAG.IN2"]
            
        if variants is None:
            variants = ["TS0.25", "TS0.25-med", "TS0.75", "TS0.75-med"]
            
        instances = (
            Graph.parse_instance(f"{data_dir}/{graph}_{variant}_EJ{ident}.txt")
            for graph in graphs
            for variant in variants
            for ident in range(1, quantity + 1)
        )

        return instances
