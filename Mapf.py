from CBS import HighLevelCBS
from CBSData import Agent, Path
from LowLevel import LowLevelCBS


class MAPF:
    def __init__(self, input_file):
        self.input_file = input_file
        self.grid_width = 0
        self.grid_height = 0
        self.obstacles = []
        self.agents = []
        self.initial_paths = []

        # Khởi tạo CBS
        self.cbs_solver = HighLevelCBS()
        self.low_level_solver = LowLevelCBS()

    def initialize_from_cbs(self):
        """Khởi tạo thông tin bản đồ và tác nhân từ CBS."""
        # Đọc input và chạy CBS
        self.cbs_solver.read_input(self.input_file)
        cbs_solution = self.cbs_solver.run_cbs()

        if cbs_solution is None:
            raise ValueError("CBS không thể tìm được giải pháp ban đầu!")

        # Trích xuất thông tin từ CBS
        self.grid_width = self.cbs_solver._lowLevelSolver._gridWidth
        self.grid_height = self.cbs_solver._lowLevelSolver._gridHeight
        self.obstacles = [(v.x, v.y) for row in self.cbs_solver._lowLevelSolver.map for v in row if v.Obstacle]
        self.agents = self.cbs_solver._agents
        self.initial_paths = cbs_solution

        # Khởi tạo bản đồ
        self.low_level_solver.initialize_map(self.grid_height, self.grid_width)
        for x, y in self.obstacles:
            self.low_level_solver.map[x][y].Obstacle = True

    def resolve_conflict(self, paths):
        """Giải quyết xung đột dựa trên các lộ trình ban đầu."""
        collisions = self.cbs_solver.detect_collisions(paths)
        if not collisions:
            return paths  # Không có xung đột

        for collision in collisions:
            constraints = self.cbs_solver.standard_splitting(collision)
            for constraint in constraints:
                agent = constraint['agent']
                updated_paths = paths.copy()

                # Tính lại đường đi cho tác nhân gây xung đột
                start = self.low_level_solver.map[self.agents[agent].StartStateX][self.agents[agent].StartStateY]
                goal = self.low_level_solver.map[self.agents[agent].GoalStateX][self.agents[agent].GoalStateY]
                new_path = Path(agent)

                if self.low_level_solver.a_star(start, goal, new_path, [constraint]):
                    updated_paths[agent] = new_path.Nodes
                else:
                    print(f"Không thể tìm đường đi mới cho tác nhân {agent}.")
                    return None

                # Kiểm tra lại xung đột
                updated_collisions = self.cbs_solver.detect_collisions(updated_paths)
                if not updated_collisions:
                    return updated_paths  # Không còn xung đột, trả về đường đi mới.

        print("Không thể giải quyết xung đột hoàn toàn.")
        return None

    def find_paths(self):
        """Tìm đường đi cuối cùng sau khi giải quyết xung đột."""
        final_paths = self.resolve_conflict(self.initial_paths)
        return final_paths
