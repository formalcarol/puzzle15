from main import PuzzleSolver, AStar_h1, AStar_h2, BreadthFirst, Puzzle

def test_generate_end_position():           # 測試給混亂的拼圖，最後可以拼回正確位置
    puzzle_4x4 = Puzzle([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]])
    assert puzzle_4x4.PUZZLE_END_POSITION == [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]], '4x4'

    puzzle_3x3 = Puzzle([[0, 2, 1], [3, 5, 4], [6, 7, 8], [9, 10, 11]])
    assert puzzle_3x3.PUZZLE_END_POSITION == [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11]], '3x3'

def test_swap():                            # 測試拼圖任兩個位置可以互相交換
    puzzle = Puzzle([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]])
    new_position = puzzle._swap(0, 0, 0, 1)     # (0,0)和(0,1)交換
    assert new_position == [[2, 1, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]

def test_get_coordinates():                 # 給某一數值，尋找該數值在拼圖的位置(i, j)
    puzzle = Puzzle([[1, 2, 6, 3], [4, 9, 5, 7], [8, 13, 11, 15], [12, 14, 0, 10]])
    i, j = puzzle._get_coordinates(0)
    assert i == 3
    assert j == 2

    i, j = puzzle._get_coordinates(10)
    assert i == 3
    assert j == 3

def test_all_possible_moves():              # 測試拼圖往上下左右交換的正確性
    puzzle = Puzzle([[1, 2, 3, 4], [5, 6, 0, 7], [8, 9, 10, 11], [12, 13, 14, 15]])
    output = puzzle.get_moves()

    assert output[0].position == [[1, 2, 0, 4], [5, 6, 3, 7], [8, 9, 10, 11], [12, 13, 14, 15]], 'up'
    assert output[1].position == [[1, 2, 3, 4], [5, 6, 7, 0], [8, 9, 10, 11], [12, 13, 14, 15]], 'right'
    assert output[2].position == [[1, 2, 3, 4], [5, 0, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]], 'left'
    assert output[3].position == [[1, 2, 3, 4], [5, 6, 10, 7], [8, 9, 0, 11], [12, 13, 14, 15]], 'down'

def test_heuristic_misplaced():             # 測試h1的總共有多少個錯位的拼圖
    puzzle = Puzzle([[1, 2, 0, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]])
    misplaced = puzzle.heuristic_misplaced()
    assert misplaced == 3

def test_heuristic_manhattan_distance():    # 測試h2的sum(所有錯位的拼圖拼還正確位置的格數)
    puzzle = Puzzle([[1, 2, 6, 3], [4, 9, 5, 7], [8, 13, 11, 15], [12, 14, 0, 10]])
    distance = puzzle.heuristic_manhattan_distance()
    assert distance == 16   # 5(0)+1(1)+1(2)+1(5)+1(6)+1(9)+2(10)+1(11)+1(13)+1(14)+1(15)=16

def test_performance():                     # 測試3個不同策略的expanded_nodes是否正確
    puzzle_start = Puzzle([[4, 1, 2, 3], [5, 6, 7, 0], [8, 9, 10, 11], [12, 13, 14, 15]])

    s1 = PuzzleSolver(BreadthFirst(puzzle_start))
    s1.run()
    assert s1._strategy.num_expanded_nodes == 35

    s2 = PuzzleSolver(AStar_h1(puzzle_start))
    s2.run()
    assert s2._strategy.num_expanded_nodes == 4

    s3 = PuzzleSolver(AStar_h2(puzzle_start))
    s3.run()
    assert s3._strategy.num_expanded_nodes == 4

if __name__ == "__main__":
    test_generate_end_position()
    test_swap()
    test_get_coordinates()
    test_all_possible_moves()
    test_heuristic_misplaced()
    test_heuristic_manhattan_distance()
    test_performance()
    print("Everything passed")
