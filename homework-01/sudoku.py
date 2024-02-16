import pathlib
import typing as tp
import random

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    """ Прочитать Судоку из указанного файла """
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    """Вывод Судоку """
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    return [values[i:i+n] for i in range(0, len(values), n)]


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    row, _ = pos
    return grid[row]


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    _, col = pos
    return [row[col] for row in grid]


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    row, col = pos
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    block = []
    for i in range(3):
        for j in range(3):
            block.append(grid[start_row + i][start_col + j])
    return block


def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]]:
    n = len(grid)
    for row in range(n):
        for col in range(n):
            if grid[row][col] == '.':
                return (row, col)
    return None


def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    row_values = set(get_row(grid, pos))
    col_values = set(get_col(grid, pos))
    block_values = set(get_block(grid, pos))
    return {'1', '2', '3', '4', '5', '6', '7', '8', '9'} - row_values - col_values - block_values


def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    empty_pos = find_empty_positions(grid)
    if not empty_pos:
        return grid
    row, col = empty_pos
    possible_values = find_possible_values(grid, (row, col))
    for value in possible_values:
        grid[row][col] = value
        if solve(grid):
            return grid
        grid[row][col] = '.'
    return None


def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    """ Если решение solution верно, то вернуть True, в противном случае False """
    for row in solution:
        if sorted(row) != ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
            return False
    for col in range(9):
        if sorted(get_col(solution, (0, col))) != ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
            return False
    for row in range(0, 9, 3):
        for col in range(0, 9, 3):
            if sorted(get_block(solution, (row, col))) != ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                return False
    return True


def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    grid = [['.' for _ in range(9)] for _ in range(9)]
    solve(grid)
    positions = [(row, col) for row in range(9) for col in range(9)]
    random.shuffle(positions)
    for _ in range(81 - N):
        row, col = positions.pop()
        grid[row][col] = '.'
    return grid

if __name__ == "__main__":
    print("Выберите действие:")
    print("1. Решить судоку из файла")
    print("2. Сгенерировать и решить новый судоку")
    choice = input("Ваш выбор (1 или 2): ")
    if choice == "1":
        fname = input("Введите имя файла с судоку: ")
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Судоку из файла {fname} не может быть решен")
        else:
            display(solution)

    elif choice == "2":
        N = int(input("Введите количество заполненных клеток в новом судоку: "))
        grid = generate_sudoku(N)
        with open('generated_sudoku.txt', 'w') as f:
            for row in grid:
                f.write(''.join(row) + '\\n')
        print("Сгенерированный судоку сохранен в файл 'generated_sudoku.txt'")
        display(grid)
        solution = solve(grid)
        if not solution:
            print("Сгенерированный судоку не может быть решен")
        else:
            display(solution)

    else:
        print("Выбор не был сделан")