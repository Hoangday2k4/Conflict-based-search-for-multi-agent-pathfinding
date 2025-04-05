from LowLevel import LowLevelCBS
from CBSData import *

# CTNode sử dụng cho CBS
class CTNode:
    def __init__(self):
        self.debugIndex = 0
        self.cost = 0
        self._constraints = []
        self._solution = []
        self._conflicts = []

    def get_solution(self) -> list:
        return self._solution

    def get_first_conflict(self):
        return self._conflicts[0]

    def add_conflict(self, new_conflict):
        self._conflicts.append(new_conflict)

    def clear_conflicts(self):
        self._conflicts.clear()

    def add_constraints(self, old_constraint_list: list, new_constraint):
        self._constraints.clear()
        for constraint in old_constraint_list:
            self._constraints.append(Constraint(constraint.Agent, constraint.Vertex, constraint.TimeStep))
        self._constraints.append(new_constraint)

    def get_constraints(self) -> list:
        return self._constraints

    def set_solution(self, new_solution: list):
        self._solution.clear()
        for path in new_solution:
            new_path = Path(path.agentIndex)
            new_path.Nodes = list(path.Nodes)

            for constraint in path.Constraints:
                new_path.Constraints.append(Constraint(constraint.Agent, constraint.Vertex, constraint.TimeStep))
            
            self._solution.append(new_path)

    def set_solution_for_agent(self, agent):
        self._solution[agent.Index] = Path(agent.Index)
        self._solution[agent.Index].Nodes = list(agent.path.Nodes)

# ICTSNode sử dụng cho ICTS
class ICTSNode:
    def __init__(self):
        self.debugIndex = 0
        self.cost = 0  # Tổng chi phí của nút
        self.solution = []  # Giải pháp đường đi của các tác nhân

    def get_solution(self) -> list:
        return self.solution

    def set_solution(self, new_solution: list):
        self.solution.clear()
        for path in new_solution:
            new_path = Path(path.agentIndex)
            new_path.Nodes = list(path.Nodes)
            self.solution.append(new_path)

class HighLevelCBS:
    def __init__(self):
        self._lowLevelSolver = LowLevelCBS()
        self._agents = []
        self._open = []

    def run(self) -> list:
        # Placeholder for Running logic
        pass

    def get_sic(self, solution: list) -> int:
        # Placeholder for SIC logic
        pass

    def read_input(self, file_path: str):
        reading_obstacles = False
        reading_agents = False

        try:
            with open(file_path, "r") as file:
                for line in file:
                    print(line.strip())
                    if line.startswith("GridGraph"):
                        tokens = LowLevelCBS.split_string_by_whitespace(line)
                        grid_width = int(tokens[1])
                        grid_height = int(tokens[2])
                        self._lowLevelSolver.initialize_map(grid_height, grid_width)

                    elif line.strip() == "Obstacles":
                        reading_obstacles = True

                    elif line.strip() == "Agents":
                        reading_obstacles = False
                        reading_agents = True

                    elif reading_obstacles:
                        tokens = LowLevelCBS.split_string_by_whitespace(line)
                        for token in tokens:
                            index = int(token)
                            self._lowLevelSolver.map[index // self._lowLevelSolver.get_width()][index % self._lowLevelSolver.get_width()].Obstacle = True

                    elif reading_agents:
                        tokens = LowLevelCBS.split_string_by_whitespace(line)
                        start_index = int(tokens[0])
                        goal_index = int(tokens[1])
                        self._agents.append(
                            Agent(
                                len(self._agents),
                                start_index // self._lowLevelSolver.get_width(),
                                start_index % self._lowLevelSolver.get_width(),
                                goal_index // self._lowLevelSolver.get_width(),
                                goal_index % self._lowLevelSolver.get_width()
                            )
                        )
        except FileNotFoundError:
            print("Unable to open file")

    def validate_paths_in_node(self, node: CTNode) -> bool:
        # Placeholder for validation logic
        pass

    def find_paths_for_all_agents(self, node: CTNode) -> list:
        # Placeholder for pathfinding logic
        pass

    def update_solution_by_invoking_low_level(self, node: CTNode, agent_index: int) -> bool:
        # Placeholder for updating the solution
        pass

    def retrieve_and_pop_node_with_lowest_cost(self) -> CTNode:
        min_cost_index = None
        min_cost = float("inf")

        for i, ct_node in enumerate(self._open):
            if ct_node.cost < min_cost:
                min_cost = ct_node.cost
                min_cost_index = i

        if min_cost_index is not None:
            node = self._open.pop(min_cost_index)
            return node

        return None

    def print_solution(self, node: CTNode):
        # Placeholder for printing solution
        pass
