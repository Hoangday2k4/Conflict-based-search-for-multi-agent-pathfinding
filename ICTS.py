from CBS import HighLevelCBS
from CBSData import Path
from LowLevel import LowLevelCBS
from CBS_h import ICTSNode


class HighLevelICTS(HighLevelCBS):
    """Triển khai thuật toán ICTS để tìm đường đi tối ưu cho nhiều tác nhân."""
    def __init__(self):
        self._lowLevelSolver = LowLevelCBS()  # Bộ giải cấp thấp
        self._agents = []  # Danh sách các tác nhân
        self._open = []  # Danh sách các nút trong cây ICTS

    def run(self) -> list[Path]:
        """Chạy thuật toán ICTS."""
        debug_index = 0
        root = ICTSNode()
        root.debugIndex = debug_index
        debug_index += 1

        # Tìm đường đi ban đầu với chi phí tối thiểu
        root.set_solution(self.find_paths_for_all_agents(root))
        root.cost = self.get_sic(root.get_solution())
        self._open.append(root)

        while self._open:
            node = self.retrieve_and_pop_node_with_lowest_cost()
            if node is None:
                print("Không có nút nào để xử lý!")
                break
            self.print_solution(node)

            # Kiểm tra nếu tất cả các tác nhân có thể đạt đích với tổng chi phí hiện tại
            if self.validate_paths_in_icts_node(node):
                return node.get_solution()

            # Nếu chưa tìm thấy giải pháp, mở rộng nút bằng cách tăng chi phí
            new_cost_node = ICTSNode()
            new_cost_node.set_solution(node.get_solution())
            new_cost_node.cost = node.cost + 1
            new_cost_node.debugIndex = debug_index
            debug_index += 1
            self._open.append(new_cost_node)

        return None

    def find_paths_for_all_agents(self, node: ICTSNode) -> list[Path]:
        """Tìm đường đi cho tất cả các tác nhân với chi phí ban đầu."""
        paths = []
        for agent in self._agents:
            start = self._lowLevelSolver.map[agent.StartStateX][agent.StartStateY]
            goal = self._lowLevelSolver.map[agent.GoalStateX][agent.GoalStateY]
            if not self._lowLevelSolver.a_star(start, goal, agent.path, []):  # Không dùng ràng buộc
                print(f"Không tìm thấy đường đi cho agent {agent.Index}")
                return None
            agent.path.agentIndex = agent.Index
            paths.append(agent.path)

        return paths

    def validate_paths_in_icts_node(self, node: ICTSNode) -> bool:
        """Kiểm tra xem tất cả các tác nhân có thể đạt đến đích với tổng chi phí đã cho không."""
        solution = node.get_solution()
        total_cost = sum(path.get_cost() for path in solution)

        return total_cost <= node.cost  # Nếu tổng chi phí không vượt mức hiện tại, giải pháp hợp lệ

    def retrieve_and_pop_node_with_lowest_cost(self) -> ICTSNode:
        """Chọn nút có tổng chi phí thấp nhất để mở rộng trong ICTS."""
        if not self._open:
            print("Không có nút nào để xử lý!")
            return None

        min_cost_index = min(range(len(self._open)), key=lambda i: self._open[i].cost)
        return self._open.pop(min_cost_index)

    def get_sic(self, solution: list[Path]) -> int:
        """Tính tổng chi phí của giải pháp hiện tại."""
        return sum(path.get_cost() for path in solution)
    
    def print_solution(self, node: ICTSNode):
        solution = node.get_solution()

        for k, path in enumerate(solution):
            print(f"Agent {k}:")
            for i, row in enumerate(self._lowLevelSolver.map):
                for j, cell in enumerate(row):
                    agent_found_in_cell = False
                    for m, node in enumerate(path.Nodes):
                        if node == cell:
                            agent_found_in_cell = True
                            print(f"|{path.agentIndex},{m}| ", end="")
                            break

                    if not agent_found_in_cell:
                        if cell.Obstacle:
                            print("|_X_| ", end="")
                        else:
                            print("|___| ", end="")
                print()