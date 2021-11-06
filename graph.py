from __future__ import annotations
from typing import List
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

            # Create tasks with id and processing times
            tasks = []
            for _ in range(num_tasks):
                task_id, time = file.readline().split(",")
                tasks.append(Task(int(task_id), int(time)))

            # Add the ids of its predecessor to each task
            for _ in range(num_relations):
                predecessor, task_id = file.readline().split(",")
                tasks[int(task_id)].predecessors.append(int(predecessor))

            # Setup times is a matrice of dim num_tasks x num_tasks
            for i in range(num_tasks):
                setup_times_i = file.readline().split(",")
                tasks[i].setup_times = list(map(int, setup_times_i))
        
        print(f"*Import of {filepath} successful!*")
        
        name = filepath.split('/')[-1][:-4]

        return Graph(tasks, cycle_time, name)
