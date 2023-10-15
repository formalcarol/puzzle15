class PuzzleSolver:
    def __init__(self, strategy):   # param strategy是 BreadthFirst或AStar
        self._strategy = strategy

    def print_performance(self):
        print(f'{self._strategy} - Expanded Nodes: {self._strategy.num_expanded_nodes}')

    def print_solution(self):
        print('Solution:')
        for p in self._strategy.solution:
            print(p)

    def run(self):
        self._strategy.do_algorithm()

class Strategy:
    num_expanded_nodes = 0
    solution = None

    def do_algorithm(self):
        raise NotImplemented

class BreadthFirst(Strategy):
    def __init__(self, initial_puzzle):
        self.start = initial_puzzle

    def __str__(self):
        return 'Breadth First'

    def do_algorithm(self):
        queue = [[self.start]]  # 原本混亂的puzzle(二維陣列)，加2個[]分解為元素
        expanded = []           # 每次拼圖的狀態都會儲存([二維]=三維)，以防止移動回相同的拼圖
        num_expanded_nodes = 0
        path = None

        while queue:    
            path = queue[0]
            queue.pop(0)                    # dequeue(FIFO)
            end_node = path[-1]
            if end_node.position in expanded:
                continue
            for move in end_node.get_moves():
                if move.position in expanded:
                    continue
                queue.append(path + [move])  # add new path at the end of the queue
            expanded.append(end_node.position)
            num_expanded_nodes += 1
            if end_node.position == end_node.PUZZLE_END_POSITION:  
                break
        self.num_expanded_nodes = num_expanded_nodes
        self.solution = path

class AStar(Strategy):
    def __init__(self, initial_puzzle):
        self.start = initial_puzzle

    def __str__(self):
        return 'A*'

    @staticmethod
    def _calculate_new_heuristic(move, end_node):   # 因為move是根據當下的end_node延伸的，成本=上次成本+變動成本。若move成本低，則易被選中，此函數易為負
        return move.heuristic_manhattan_distance() - end_node.heuristic_manhattan_distance()

    def do_algorithm(self):
        # self.start.heuristic_manhattan_distance()=sum(所有元素到其正確位置的格數)
        queue = [[self.start.heuristic_manhattan_distance(), self.start]] 
        expanded = []
        num_expanded_nodes = 0
        path = None

        while queue:
            i = 0
            for j in range(1, len(queue)):      # len(queue)每次path後下一步move的選擇數量
                if queue[i][0] > queue[j][0]:   # 挑選成本最小的
                    i = j
            path = queue[i]                     # 確定要移動的
            queue = queue[:i] + queue[i + 1:]   # 將除了path以外的move加入queue，下一次要一起參加成本最小的比較
            end_node = path[-1]
            if end_node.position == end_node.PUZZLE_END_POSITION:
                break
            if end_node.position in expanded:
                continue

            for move in end_node.get_moves():   # 最新的path的下一步所有的move
                if move.position in expanded:
                    continue
                new_path = [path[0] + self._calculate_new_heuristic(move, end_node)] + path[1:] + [move]
                queue.append(new_path)          # 將除了path以外的move加入queue，再加入path後的所有move，要一起參加成本最小的比較
                expanded.append(end_node.position)
            num_expanded_nodes += 1
        self.num_expanded_nodes = num_expanded_nodes
        self.solution = path[1:]

class Puzzle:
    def __init__(self, position):   # param position是未排序好的puzzle [[4, 1, 2, 3], [5, 6, 7, 11], [8, 9, 10, 15], [12, 13, 14, 0]]
        self.position = position
        self.PUZZLE_NUM_ROWS = len(position)
        self.PUZZLE_NUM_COLUMNS = len(position[0])
        self.PUZZLE_END_POSITION = self._generate_end_position() 

    def __str__(self):  #將puzzle的數列 表現成 4*4的矩陣
        puzzle_string = ""
        for i in range(self.PUZZLE_NUM_ROWS):
            for j in range(self.PUZZLE_NUM_COLUMNS):
                puzzle_string += '│{0: >2}'.format(str(self.position[i][j]))    # '│{0: >2}'.format(內容)是以2格並向右對齊的方式輸出內容
                if j == self.PUZZLE_NUM_COLUMNS - 1:    # 每一行的最後一個數字
                    puzzle_string += '│\n'
        return puzzle_string

    def _generate_end_position(self):   # 目的地 [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]
        end_position = []
        new_row = []
        for i in range(self.PUZZLE_NUM_ROWS * self.PUZZLE_NUM_COLUMNS): # 直接根據row和col生成遞增的數字
            new_row.append(i)
            if len(new_row) == self.PUZZLE_NUM_COLUMNS: # 換行
                end_position.append(new_row)
                new_row = []
        return end_position

    def _swap(self, x1, y1, x2, y2):    # (x1, y1)和(x2, y2)交換位置
        puzzle_copy = [list(row) for row in self.position]  # copy the puzzle why??
        puzzle_copy[x1][y1], puzzle_copy[x2][y2] = puzzle_copy[x2][y2], puzzle_copy[x1][y1]
        return puzzle_copy

    def _get_coordinates(self, tile, position=None):    # 此元素title在正確拼圖position的位置(i, j)
        if not position:                        # 若_get_coordinates(0)，則取得現在位置
            position = self.position
        for i in range(self.PUZZLE_NUM_ROWS):
            for j in range(self.PUZZLE_NUM_COLUMNS):
                if position[i][j] == tile:
                    return i, j
        return RuntimeError('Invalid tile value')

    def get_moves(self):    # 以(i, j)為準移動
        moves = []
        i, j = self._get_coordinates(0)                     # 取得呼叫此函數的點的所在位置(i, j)
        if i > 0:
            moves.append(Puzzle(self._swap(i, j, i-1, j)))  # 往上走1格
        if j < self.PUZZLE_NUM_COLUMNS - 1:
            moves.append(Puzzle(self._swap(i, j, i, j+1)))  # 往右走1格
        if j > 0:
            moves.append(Puzzle(self._swap(i, j, i, j-1)))  # 往左走1格
        if i < self.PUZZLE_NUM_ROWS - 1:
            moves.append(Puzzle(self._swap(i, j, i+1, j)))  # 往下走1格
        return moves

    def heuristic_misplaced(self):          # 現在位置和正確位置的格數(路徑)
        misplaced = 0
        for i in range(self.PUZZLE_NUM_ROWS):
            for j in range(self.PUZZLE_NUM_COLUMNS):
                if self.position[i][j] != self.PUZZLE_END_POSITION[i][j]:
                    misplaced += 1
        return misplaced

    def heuristic_manhattan_distance(self): # 現在位置和正確位置的直線距離(位移)
        distance = 0
        for i in range(self.PUZZLE_NUM_ROWS):
            for j in range(self.PUZZLE_NUM_COLUMNS):
                i1, j1 = self._get_coordinates(self.position[i][j], self.PUZZLE_END_POSITION)
                distance += abs(i - i1) + abs(j - j1)
        return distance

if __name__ == '__main__':
    puzzle = Puzzle([[4, 1, 2, 3], [5, 6, 7, 11], [8, 9, 10, 15], [12, 13, 14, 0]])
    for strategy in [BreadthFirst, AStar]:  # 分別使用BreadthFirst和AStar方法
        p = PuzzleSolver(strategy(puzzle))
        p.run()
        p.print_performance()
        p.print_solution()
    